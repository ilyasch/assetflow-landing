#!/usr/bin/env python3
"""Render the localized product documentation hub and core guides."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("en", "it", "de", "es", "fr", "ar")
SITE = "https://myassetsflow.com"
LANG_NAMES = {"en": "English", "it": "Italiano", "de": "Deutsch", "es": "Español", "fr": "Français", "ar": "العربية"}

# Each guide has a title, short introduction, and three practical steps.
DATA = {
"en": {
"ui": ["Product guides", "Clear guides to adding assets, organizing records, and planning maintenance in AssetFlow Home.", "Read guide", "All product guides", "In this guide", "Home", "Blog", "Start free", "Skip to content", "Product guide", "Language"],
"guides": [
["Add an asset", "Create a useful starting record for something you own.", [["Choose a category", "Select the category that fits the asset, such as a vehicle, appliance, or home. The category shapes the details you can record."], ["Add known details", "Enter the name and the details you have, such as model, year, mileage, or purchase date. Leave unknown information out rather than guessing."], ["Keep its context together", "Add relevant documents and notes to the asset so its history is easier to understand and maintain over time."]]],
["Organize records", "Keep source documents and service history connected to the asset they explain.", [["Add the source", "Save manuals, receipts, warranties, and other useful files with the related asset. Keep the original document as the source of truth."], ["Record completed work", "Add service or maintenance as a dated record, with the details and documents that support it. Keep suggestions separate from completed work."], ["Review the evidence", "When you revisit an asset, use its documents and history to see what is known and what still needs checking."]]],
["Plan maintenance", "Use asset details and records to prepare a plan you can review and adjust.", [["Start with reliable context", "Check the asset details, current condition, documents, and service history. For vehicles and equipment, consult the exact manufacturer guidance."], ["Review suggestions", "AssetFlow can prepare a maintenance draft from the information available. Suggestions are a starting point and may need correction or professional advice."], ["Choose what to do", "Adjust tasks and dates before confirming them. Record completed work afterward so the history stays clear. AI suggestions require your review."]]]
]},
"it": {
"ui": ["Guide del prodotto", "Guide chiare per aggiungere beni, organizzare documenti e pianificare la manutenzione con AssetFlow Home.", "Leggi la guida", "Tutte le guide", "In questa guida", "Home", "Blog", "Inizia gratis", "Vai al contenuto", "Guida del prodotto", "Lingua"],
"guides": [
["Aggiungere un bene", "Crea una scheda iniziale utile per un bene che possiedi.", [["Scegli una categoria", "Seleziona la categoria adatta, come veicolo, elettrodomestico o abitazione. La categoria determina i dettagli che puoi registrare."], ["Aggiungi i dati noti", "Inserisci nome e dati disponibili, come modello, anno, chilometraggio o data di acquisto. Non indovinare le informazioni che non conosci."], ["Raccogli il contesto", "Aggiungi documenti e note pertinenti al bene per comprenderne meglio la storia e la manutenzione nel tempo."]]],
["Organizzare i documenti", "Collega documenti di origine e storico degli interventi al bene a cui si riferiscono.", [["Aggiungi la fonte", "Salva manuali, ricevute, garanzie e altri file utili con il bene corretto. Conserva il documento originale come fonte attendibile."], ["Registra gli interventi svolti", "Aggiungi manutenzioni o riparazioni completate come registrazioni datate con i relativi dettagli e documenti. Separa le proposte dai lavori conclusi."], ["Rivedi le prove", "Quando consulti di nuovo un bene, usa documenti e storico per capire cosa è noto e cosa va ancora verificato."]]],
["Pianificare la manutenzione", "Usa i dettagli del bene e i documenti per preparare un piano da rivedere e modificare.", [["Parti da informazioni affidabili", "Controlla i dettagli, le condizioni attuali, i documenti e lo storico. Per veicoli e attrezzature, consulta le indicazioni del produttore per il modello esatto."], ["Rivedi i suggerimenti", "AssetFlow può preparare una bozza in base alle informazioni disponibili. I suggerimenti sono un punto di partenza e possono richiedere correzioni o un parere professionale."], ["Decidi cosa fare", "Modifica attività e date prima di confermarle. Registra poi i lavori completati. I suggerimenti AI richiedono sempre la tua revisione."]]]
]},
"de": {
"ui": ["Produktleitfäden", "Klare Anleitungen zum Erfassen von Assets, Ordnen von Unterlagen und Planen der Wartung mit AssetFlow Home.", "Anleitung lesen", "Alle Produktleitfäden", "In diesem Leitfaden", "Home", "Blog", "Kostenlos starten", "Zum Inhalt", "Produktleitfaden", "Sprache"],
"guides": [
["Ein Asset hinzufügen", "Erstelle einen hilfreichen Ausgangsdatensatz für einen Gegenstand, den du besitzt.", [["Kategorie auswählen", "Wähle die passende Kategorie, etwa Fahrzeug, Haushaltsgerät oder Immobilie. Sie bestimmt, welche Angaben du erfassen kannst."], ["Bekannte Angaben ergänzen", "Trage Name und bekannte Details ein, zum Beispiel Modell, Baujahr, Kilometerstand oder Kaufdatum. Rate keine unbekannten Angaben."], ["Zusammenhang festhalten", "Füge relevante Dokumente und Notizen zum Asset hinzu, damit seine Historie und Wartung nachvollziehbar bleiben."]]],
["Unterlagen ordnen", "Verbinde Quelldokumente und Wartungshistorie mit dem Asset, das sie erklären.", [["Quelle hinzufügen", "Speichere Handbücher, Belege, Garantien und weitere nützliche Dateien beim passenden Asset. Das Originaldokument bleibt die maßgebliche Quelle."], ["Erledigte Arbeiten erfassen", "Lege Wartungen oder Reparaturen als datierte Einträge mit Details und Belegen an. Trenne Vorschläge klar von erledigten Arbeiten."], ["Belege prüfen", "Nutze Dokumente und Historie, um später zu erkennen, was bekannt ist und was noch geprüft werden muss."]]],
["Wartung planen", "Nutze Assetangaben und Unterlagen für einen Plan, den du prüfen und anpassen kannst.", [["Mit verlässlichem Kontext beginnen", "Prüfe Angaben, Zustand, Unterlagen und Historie. Beachte bei Fahrzeugen und Geräten die Herstellerangaben für das genaue Modell."], ["Vorschläge prüfen", "AssetFlow kann anhand verfügbarer Informationen einen Wartungsentwurf erstellen. Vorschläge sind ein Ausgangspunkt und können Korrekturen oder fachlichen Rat erfordern."], ["Maßnahmen auswählen", "Passe Aufgaben und Termine vor der Bestätigung an. Erfasse erledigte Arbeiten anschließend. KI-Vorschläge müssen von dir geprüft werden."]]]
]},
"es": {
"ui": ["Guías del producto", "Guías claras para añadir bienes, organizar documentos y planificar el mantenimiento con AssetFlow Home.", "Leer guía", "Todas las guías", "En esta guía", "Home", "Blog", "Empieza gratis", "Ir al contenido", "Guía del producto", "Idioma"],
"guides": [
["Añadir un bien", "Crea un registro inicial útil de algo que posees.", [["Elige una categoría", "Selecciona la categoría adecuada, como vehículo, electrodoméstico o vivienda. La categoría determina qué detalles puedes registrar."], ["Añade los datos conocidos", "Introduce el nombre y los detalles disponibles, como modelo, año, kilometraje o fecha de compra. No adivines los datos que desconoces."], ["Reúne el contexto", "Añade documentos y notas pertinentes al bien para comprender mejor su historial y mantenimiento con el tiempo."]]],
["Organizar documentos", "Conecta documentos de origen e historial de mantenimiento con el bien al que se refieren.", [["Añade la fuente", "Guarda manuales, recibos, garantías y otros archivos útiles con el bien correspondiente. Conserva el documento original como fuente de referencia."], ["Registra el trabajo realizado", "Añade mantenimientos o reparaciones terminados como registros con fecha, detalles y documentos. Separa las propuestas del trabajo completado."], ["Revisa las pruebas", "Al volver a consultar un bien, usa sus documentos e historial para ver qué se sabe y qué queda por comprobar."]]],
["Planificar el mantenimiento", "Usa los datos del bien y sus registros para preparar un plan que puedas revisar y ajustar.", [["Empieza con contexto fiable", "Comprueba los datos, el estado actual, los documentos y el historial. Para vehículos y equipos, consulta las indicaciones del fabricante para el modelo exacto."], ["Revisa las sugerencias", "AssetFlow puede preparar un borrador de mantenimiento con la información disponible. Las sugerencias son un punto de partida y pueden requerir correcciones o asesoramiento profesional."], ["Decide qué hacer", "Ajusta las tareas y fechas antes de confirmarlas. Después registra el trabajo realizado. Las sugerencias de IA requieren tu revisión."]]]
]},
"fr": {
"ui": ["Guides du produit", "Des guides clairs pour ajouter des biens, organiser les documents et planifier l’entretien avec AssetFlow Home.", "Lire le guide", "Tous les guides", "Dans ce guide", "Home", "Blog", "Commencer gratuitement", "Aller au contenu", "Guide produit", "Langue"],
"guides": [
["Ajouter un bien", "Créez une fiche de départ utile pour un bien que vous possédez.", [["Choisir une catégorie", "Sélectionnez la catégorie adaptée, comme un véhicule, un appareil ou un logement. Elle détermine les informations que vous pouvez enregistrer."], ["Ajouter les informations connues", "Saisissez le nom et les informations disponibles, comme le modèle, l’année, le kilométrage ou la date d’achat. Ne devinez pas les informations inconnues."], ["Rassembler le contexte", "Ajoutez au bien les documents et notes utiles pour mieux comprendre son historique et son entretien au fil du temps."]]],
["Organiser les documents", "Reliez les documents sources et l’historique d’entretien au bien qu’ils décrivent.", [["Ajouter la source", "Enregistrez manuels, reçus, garanties et autres fichiers utiles avec le bien concerné. Le document original reste la référence."], ["Consigner les travaux terminés", "Ajoutez les entretiens ou réparations effectués sous forme d’entrées datées avec leurs détails et justificatifs. Distinguez les propositions des travaux réalisés."], ["Examiner les justificatifs", "Lorsque vous consultez de nouveau un bien, utilisez ses documents et son historique pour voir ce qui est connu et ce qui reste à vérifier."]]],
["Planifier l’entretien", "Utilisez les informations du bien et ses documents pour préparer un plan à examiner et ajuster.", [["Partir d’un contexte fiable", "Vérifiez les informations, l’état actuel, les documents et l’historique. Pour les véhicules et équipements, consultez les recommandations du fabricant pour le modèle exact."], ["Examiner les suggestions", "AssetFlow peut préparer un brouillon d’entretien à partir des informations disponibles. Les suggestions sont un point de départ et peuvent nécessiter des corrections ou un avis professionnel."], ["Choisir la suite", "Ajustez les tâches et les dates avant de les confirmer. Consignez ensuite les travaux terminés. Les suggestions de l’IA doivent être examinées par vos soins."]]]
]},
"ar": {
"ui": ["أدلة المنتج", "أدلة واضحة لإضافة الأصول وتنظيم السجلات وتخطيط الصيانة باستخدام AssetFlow Home.", "اقرأ الدليل", "كل أدلة المنتج", "في هذا الدليل", "Home", "المدونة", "ابدأ مجانًا", "انتقل إلى المحتوى", "دليل المنتج", "اللغة"],
"guides": [
["إضافة أصل", "أنشئ سجلًا أوليًا مفيدًا لشيء تملكه.", [["اختر فئة", "اختر الفئة المناسبة مثل مركبة أو جهاز منزلي أو منزل. تساعد الفئة في تحديد التفاصيل التي يمكنك تسجيلها."], ["أضف المعلومات المعروفة", "أدخل الاسم والتفاصيل المتاحة مثل الطراز أو السنة أو المسافة أو تاريخ الشراء. لا تخمّن المعلومات غير المعروفة."], ["اجمع السياق", "أضف المستندات والملاحظات ذات الصلة بالأصل لتسهيل فهم تاريخه وصيانته بمرور الوقت."]]],
["تنظيم السجلات", "اربط المستندات الأصلية وسجل الصيانة بالأصل الذي توضحه.", [["أضف المصدر", "احفظ الكتيبات والإيصالات والضمانات والملفات المفيدة مع الأصل المعني. احتفظ بالمستند الأصلي بوصفه المرجع."], ["سجّل الأعمال المنجزة", "أضف الصيانة أو الإصلاحات المكتملة كسجلات مؤرخة مع التفاصيل والمستندات الداعمة. افصل المقترحات عن الأعمال المنجزة."], ["راجع الأدلة", "عند العودة إلى الأصل، استخدم المستندات والسجل لمعرفة المعلومات المتاحة وما يحتاج إلى تحقق إضافي."]]],
["تخطيط الصيانة", "استخدم تفاصيل الأصل وسجلاته لإعداد خطة يمكنك مراجعتها وتعديلها.", [["ابدأ بسياق موثوق", "راجع التفاصيل والحالة الحالية والمستندات وسجل الصيانة. للمركبات والمعدات، استعن بإرشادات الشركة المصنّعة للطراز المحدد."], ["راجع المقترحات", "يمكن لـ AssetFlow إعداد مسودة صيانة استنادًا إلى المعلومات المتاحة. المقترحات نقطة بداية وقد تحتاج إلى تصحيح أو استشارة مختص."], ["اختر ما ستفعله", "عدّل المهام والتواريخ قبل تأكيدها. سجّل الأعمال المكتملة لاحقًا. تتطلب اقتراحات الذكاء الاصطناعي مراجعتك."]]]
]}}


def esc(value):
    return html.escape(value, quote=True)


def render(locale, data):
    ui = data["ui"]
    guides = data["guides"]
    rtl = locale == "ar"
    home = f"/?lang={locale}"
    links = "".join(f'<li><a href="/docs/{locale}/{slug}/">{esc(guide[0])}</a><p>{esc(guide[1])}</p></li>' for slug, guide in zip(("add-an-asset", "organize-records", "plan-maintenance"), guides))
    def language_menu(slug=""):
        options = "".join(f'<a href="/docs/{other}/{slug}" lang="{other}" hreflang="{other}"{" aria-current=page" if other == locale else ""}>{name}</a>' for other, name in LANG_NAMES.items())
        return f'<details class="article-language"><summary>{LANG_NAMES[locale]}</summary><nav aria-label="{esc(ui[10])}">{options}</nav></details>'
    def language_alternates(slug=""):
        return "".join(f'<link rel="alternate" hreflang="{other}" href="{SITE}/docs/{other}/{slug}">' for other in LANG_NAMES)
    pages = []
    for slug, guide in zip(("add-an-asset", "organize-records", "plan-maintenance"), guides):
        steps = "".join(f'<section><h2>{esc(step[0])}</h2><p>{esc(step[1])}</p></section>' for step in guide[2])
        pages.append((slug, f'''<!doctype html><html lang="{locale}" dir="{'rtl' if rtl else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(guide[0])} | AssetFlow</title><meta name="description" content="{esc(guide[1])}"><link rel="canonical" href="{SITE}/docs/{locale}/{slug}/">{language_alternates(slug + "/")}<link rel="stylesheet" href="/styles.css?v=10"><link rel="stylesheet" href="/blog.css?v=1"></head><body class="article-page"><a class="skip-link" href="#main">{esc(ui[8])}</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{home}"><img class="brand-wordmark" src="/assets/assetflow-wordmark-217.webp" width="217" height="72" alt="AssetFlow"></a><a class="article-back" href="/docs/{locale}/">{esc(ui[3])}</a><a class="article-back" href="/blog/{locale}/">{esc(ui[6])}</a>{language_menu(slug + "/")}<a class="btn btn-primary" href="https://myassetsflow.app">{esc(ui[7])}</a></div></header><main id="main"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{home}">AssetFlow</a><span aria-hidden="true">/</span><a href="/docs/{locale}/">{esc(ui[0])}</a><span aria-hidden="true">/</span><span>{esc(guide[0])}</span></nav><header class="article-hero"><h1>{esc(guide[0])}</h1><p class="article-deck">{esc(guide[1])}</p><p class="article-status">AssetFlow {esc(ui[5])} · {esc(ui[9])}</p></header><div class="article-layout"><aside class="article-toc"><details open><summary>{esc(ui[4])}</summary><nav aria-label="{esc(ui[4])}"><ol>{''.join(f'<li><a href="#step-{i+1}">{esc(step[0])}</a></li>' for i,step in enumerate(guide[2]))}</ol></nav></details></aside><article class="article-body">{''.join(f'<section id="step-{i+1}"><h2>{esc(step[0])}</h2><p>{esc(step[1])}</p></section>' for i,step in enumerate(guide[2]))}<nav class="article-related"><h2>{esc(ui[3])}</h2><ul>{''.join(f'<li><a href="/docs/{locale}/{other_slug}/">{esc(other[0])}</a></li>' for other_slug,other in zip(("add-an-asset","organize-records","plan-maintenance"),guides) if other[0] != guide[0])}</ul><a href="/docs/{locale}/">{esc(ui[3])}</a></nav></article></div></div></main><footer class="site-footer"><div class="wrap footer-inner"><p>© AssetFlow</p><p class="legal-links"><a href="/blog/{locale}/">{esc(ui[6])}</a></p></div></footer></body></html>'''))
    index = f'''<!doctype html><html lang="{locale}" dir="{'rtl' if rtl else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(ui[0])} | AssetFlow</title><meta name="description" content="{esc(ui[1])}"><link rel="canonical" href="{SITE}/docs/{locale}/">{language_alternates()}<link rel="stylesheet" href="/styles.css?v=10"><link rel="stylesheet" href="/blog.css?v=1"></head><body class="article-page blog-index"><a class="skip-link" href="#main">{esc(ui[8])}</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{home}"><img class="brand-wordmark" src="/assets/assetflow-wordmark-217.webp" width="217" height="72" alt="AssetFlow"></a><a class="article-back" href="/blog/{locale}/">{esc(ui[6])}</a>{language_menu()}<a class="btn btn-primary" href="https://myassetsflow.app">{esc(ui[7])}</a></div></header><main id="main"><section class="section blogs" aria-labelledby="docs-title"><div class="wrap"><div class="blog-section-intro"><h1 id="docs-title">{esc(ui[0])}</h1><p class="section-lead">{esc(ui[1])}</p></div><ol class="docs-list">{links}</ol></div></section></main><footer class="site-footer"><div class="wrap footer-inner"><p>© AssetFlow</p><p class="legal-links"><a href="/blog/{locale}/">{esc(ui[6])}</a></p></div></footer></body></html>'''
    return index, pages


def build(output, sitemap_only=False):
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    import xml.etree.ElementTree as ET
    ET.register_namespace("", namespace)
    sitemap = output / "sitemap.xml"
    tree = ET.parse(sitemap) if sitemap.exists() else ET.ElementTree(ET.Element(f"{{{namespace}}}urlset"))
    root = tree.getroot()
    existing = {node.find(f"{{{namespace}}}loc").text for node in root.findall(f"{{{namespace}}}url")}
    for locale in LOCALES:
        data = DATA[locale]
        slugs = ("add-an-asset", "organize-records", "plan-maintenance")
        urls = [f"{SITE}/docs/{locale}/"] + [f"{SITE}/docs/{locale}/{slug}/" for slug in slugs]
        if not sitemap_only:
            index, pages = render(locale, data)
            index_dir = output / "docs" / locale
            index_dir.mkdir(parents=True, exist_ok=True)
            (index_dir / "index.html").write_text(index)
            for slug, page in pages:
                directory = index_dir / slug
                directory.mkdir(parents=True, exist_ok=True)
                (directory / "index.html").write_text(page)
        for url in urls:
            if url not in existing:
                node = ET.SubElement(root, f"{{{namespace}}}url")
                ET.SubElement(node, f"{{{namespace}}}loc").text = url
    ET.indent(tree)
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)
    print("Updated localized product guide sitemap." if sitemap_only else "Rendered localized product guides and updated sitemap.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT)
    parser.add_argument("--sitemap-only", action="store_true")
    args = parser.parse_args()
    build(args.output, args.sitemap_only)
