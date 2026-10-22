const DESTINATION = "contact@myassetsflow.com";
const SENDERS = new Set(["Business", "Fleet", "Hospitality"]);
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

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  if (request.headers.get("Origin") !== url.origin) return json({ error: "invalid origin" }, 403);
  if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) {
    return json({ error: "unsupported content type" }, 415);
  }
  let body;
  try {
    const reader = request.body.getReader();
    const chunks = [];
    let size = 0;
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > 8192) {
        await reader.cancel();
        return json({ error: "request too large" }, 413);
      }
      chunks.push(value);
    }
    const bytes = new Uint8Array(size);
    let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    body = JSON.parse(new TextDecoder().decode(bytes));
  } catch { return json({ error: "invalid request" }, 400); }
  if (body.website) return json({ ok: true });
  const edition = typeof body.edition === "string" ? body.edition.trim() : "";
  const email = typeof body.email === "string" ? body.email.trim() : "";
  const message = typeof body.message === "string" ? body.message.trim() : "";
  if (!SENDERS.has(edition) || email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !message || message.length > 4000) {
    return json({ error: "invalid fields" }, 400);
  }

  const now = Date.now();
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const previous = (attempts.get(ip) || []).filter((time) => now - time < 15 * 60 * 1000);
  if (previous.length >= 5) return json({ error: "rate limited" }, 429);
  previous.push(now);
  attempts.set(ip, previous);
  if (attempts.size > 500) attempts.delete(attempts.keys().next().value);

  if (!env.CF_ACCOUNT_ID || !env.CF_EMAIL_API_TOKEN || !env.CF_EMAIL_FROM) {
    return json({ error: "email service unavailable" }, 503);
  }
  const text = `Edition: ${edition}\nReply to: ${email}\n\n${message}`;
  const result = await fetch(`https://api.cloudflare.com/client/v4/accounts/${encodeURIComponent(env.CF_ACCOUNT_ID)}/email/sending/send`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.CF_EMAIL_API_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      to: DESTINATION,
      from: env.CF_EMAIL_FROM,
      subject: `AssetFlow ${edition} enquiry`,
      text,
      html: `<p><strong>Edition:</strong> ${escapeHtml(edition)}</p><p><strong>Reply to:</strong> ${escapeHtml(email)}</p><p>${escapeHtml(message).replace(/\n/g, "<br>")}</p>`,
    }),
  });
  if (!result.ok) return json({ error: "email send failed" }, 502);
  const response = await result.json().catch(() => null);
  if (!response?.success) return json({ error: "email send failed" }, 502);
  return json({ ok: true });
}

export async function onRequest(context) {
  if (context.request.method !== "POST") return json({ error: "method not allowed" }, 405);
  return onRequestPost(context);
}
