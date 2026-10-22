const DESTINATION = "contact@myassetsflow.com";
const DEFAULT_FROM = "AssetFlow <contact@myassetsflow.com>";
const EDITIONS = new Set(["Business", "Fleet", "Hospitality"]);
const attempts = new Map();

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[char]);
}

async function readJson(request) {
  const reader = request.body?.getReader();
  if (!reader) throw new Error("invalid body");
  const chunks = [];
  let size = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > 8192) {
      await reader.cancel();
      throw new RangeError("body too large");
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
  return JSON.parse(new TextDecoder().decode(bytes));
}

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  if (request.headers.get("Origin") !== url.origin) return json({ error: "invalid origin" }, 403);
  if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) {
    return json({ error: "unsupported content type" }, 415);
  }

  let body;
  try { body = await readJson(request); }
  catch (error) {
    if (error instanceof RangeError) return json({ error: "request too large" }, 413);
    return json({ error: "invalid request" }, 400);
  }
  if (!body || typeof body !== "object" || Array.isArray(body)) return json({ error: "invalid request" }, 400);
  if (typeof body.website === "string" && body.website.trim()) return json({ ok: true });

  const edition = typeof body.edition === "string" ? body.edition.trim() : "";
  const email = typeof body.email === "string" ? body.email.trim() : "";
  const message = typeof body.message === "string" ? body.message.trim() : "";
  if (!EDITIONS.has(edition) || email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !message || message.length > 4000) {
    return json({ error: "invalid fields" }, 400);
  }

  const now = Date.now();
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const recent = (attempts.get(ip) || []).filter((time) => now - time < 15 * 60 * 1000);
  if (recent.length >= 5) return json({ error: "rate limited" }, 429);
  recent.push(now);
  attempts.set(ip, recent);
  if (attempts.size > 500) attempts.delete(attempts.keys().next().value);

  if (!env.RESEND_API_KEY) return json({ error: "email service unavailable" }, 503);

  const text = `Edition: ${edition}\nReply to: ${email}\n\n${message}`;
  const html = `<p><strong>Edition:</strong> ${escapeHtml(edition)}</p><p><strong>Reply to:</strong> ${escapeHtml(email)}</p><p>${escapeHtml(message).replace(/\n/g, "<br>")}</p>`;
  const requestedKey = request.headers.get("Idempotency-Key") || "";
  const idempotencyKey = /^[a-f0-9-]{36}$/i.test(requestedKey) ? requestedKey : crypto.randomUUID();
  let response;
  try {
    response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
        "Idempotency-Key": idempotencyKey,
      },
      body: JSON.stringify({
        from: env.RESEND_FROM || DEFAULT_FROM,
        to: [DESTINATION],
        reply_to: email,
        subject: `AssetFlow ${edition} enquiry`,
        text,
        html,
      }),
      signal: AbortSignal.timeout(10000),
    });
  } catch { return json({ error: "email send failed" }, 502); }

  if (!response.ok) return json({ error: "email send failed" }, 502);
  const result = await response.json().catch(() => null);
  if (!result?.id) return json({ error: "email send failed" }, 502);
  return json({ ok: true });
}

export async function onRequest({ request, env }) {
  if (request.method !== "POST") return json({ error: "method not allowed" }, 405);
  return onRequestPost({ request, env });
}
