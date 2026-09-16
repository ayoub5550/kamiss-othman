import re
import markdown
from pathlib import Path
from weasyprint import HTML

REPO = Path("/work/repos/kamiss-othman")
OUT = Path("/work/temp/kamiss-othman.pdf")

CHAPTER_FILES = [
    "01-sykes-picot-balfour.md",
    "03-harb-1948-alnakba.md",
    "04-azmat-alsuways-1956.md",
    "05-8-mai-1945-harb-aljazair.md",
    "06-harb-1967-alnaksa.md",
    "07-harb-october-1973.md",
    "08-harb-lubnan-alahliya.md",
    "09-harb-iraq-iran.md",
    "10-harb-alkhalij-althania-1991.md",
    "11-ghazw-aliraq-2003.md",
    "12-harb-lubnan-2006.md",
    "13-althawrat-alarabiya-tadakhulat.md",
    "14-alharb-ala-daesh.md",
    "15-harb-alyaman.md",
    "16-harb-ghaza-2023.md",
    "17-harb-iran-israel-2025.md",
]

md_ext = ["extra", "sane_lists"]

def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=md_ext)

def load_chapter(fname):
    text = (REPO / "chapters" / fname).read_text(encoding="utf-8")
    lines = text.split("\n")
    title = lines[0].lstrip("# ").strip()
    body = "\n".join(lines[1:]).strip()
    return title, md_to_html(body)

def build():
    intro_text = (REPO / "00-muqaddima.md").read_text(encoding="utf-8")
    intro_lines = intro_text.split("\n")
    intro_html = md_to_html("\n".join(intro_lines[1:]).strip())

    chapters_html = []
    toc_entries = []
    for i, fname in enumerate(CHAPTER_FILES, start=1):
        title, body_html = load_chapter(fname)
        anchor = f"ch{i}"
        toc_entries.append((title, anchor))
        chapters_html.append(f'''
        <section class="chapter" id="{anchor}">
          <div class="chapter-eyebrow">الفصل {ar_num(i)}</div>
          <h1 class="chapter-title">{title}</h1>
          {body_html}
        </section>
        ''')

    toc_html = "\n".join(
        f'<li><a href="#{anchor}"><span class="toc-title">{title}</span></a></li>'
        for title, anchor in toc_entries
    )

    html = f"""
    <html dir="rtl" lang="ar">
    <head><meta charset="utf-8"/>
    <style>{CSS}</style>
    </head>
    <body>
      <section class="cover">
        <div class="cover-eyebrow">موسوعة الذرائع — 1900 – 2026</div>
        <h1 class="cover-title">قميص عثمان</h1>
        <div class="cover-subtitle">كيف بُنيت سرديات الحروب في الشرق الأوسط وشمال إفريقيا</div>
        <div class="cover-credit">تأليف وإشراف: أيوب — طالب من الجزائر<br/>بمساعدة نموذج الذكاء الاصطناعي Claude عبر منصة Viktor</div>
      </section>

      <section class="toc-page">
        <div class="toc-eyebrow">فهرس المحتويات</div>
        <ol class="toc-list">
          <li><a href="#intro"><span class="toc-title">المقدمة</span></a></li>
          {toc_html}
        </ol>
      </section>

      <section class="chapter" id="intro">
        <div class="chapter-eyebrow">المقدمة</div>
        <h1 class="chapter-title">قصة القميص ومنهج الكتاب</h1>
        {intro_html}
      </section>

      {"".join(chapters_html)}
    </body>
    </html>
    """
    HTML(string=html).write_pdf(str(OUT))
    print("wrote", OUT)

def ar_num(n):
    mapping = {1:"الأول",3:"الثاني",4:"الثالث",5:"الرابع",6:"الخامس",7:"السادس",
               8:"السابع",9:"الثامن",10:"التاسع",11:"العاشر",12:"الحادي عشر",
               13:"الثاني عشر",14:"الثالث عشر",15:"الرابع عشر",16:"الخامس عشر",17:"السادس عشر"}
    return mapping.get(n, str(n))

CSS = """
@page {
  size: letter;
  margin: 0.9in 0.85in;
  @bottom-center { content: counter(page); font-family: 'Roboto Mono', monospace; font-size: 10pt; color: #666; }
}
@page cover { margin: 0; }

* { box-sizing: border-box; }

body {
  font-family: 'Noto Naskh Arabic', 'Noto Sans Arabic', serif;
  direction: rtl;
  color: #111;
  font-size: 12.5pt;
  line-height: 1.9;
}

.cover {
  page: cover;
  width: 8.5in; height: 11in;
  background: #0b0b0b;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
  text-align: right;
  padding: 1.4in 1in;
  break-after: page;
}
.cover-eyebrow {
  font-family: 'Roboto Mono', monospace;
  font-size: 12pt;
  letter-spacing: 0.16em;
  color: rgba(255,255,255,0.55);
  margin-bottom: 0.6in;
  width: 100%;
}
.cover-title {
  font-size: 58pt;
  font-weight: 700;
  margin: 0 0 0.3in 0;
  line-height: 1.15;
  width: 100%;
}
.cover-subtitle {
  font-size: 17pt;
  color: rgba(255,255,255,0.75);
  width: 100%;
  text-align: right;
  line-height: 1.6;
  margin-bottom: 1.6in;
}
.cover-credit {
  font-size: 11pt;
  color: rgba(255,255,255,0.5);
  line-height: 1.7;
  width: 100%;
}

.toc-page {
  break-after: page;
  padding-top: 0.3in;
}
.toc-eyebrow {
  font-family: 'Roboto Mono', monospace;
  font-size: 11pt;
  letter-spacing: 0.14em;
  color: rgba(0,0,0,0.5);
  margin-bottom: 0.35in;
  text-transform: uppercase;
}
.toc-list {
  list-style: none;
  padding: 0; margin: 0;
}
.toc-list li {
  padding: 0.14in 0;
  border-bottom: 0.5pt solid rgba(0,0,0,0.15);
}
.toc-list a {
  text-decoration: none;
  color: #111;
}
.toc-title {
  font-size: 13pt;
}

.chapter {
  break-before: page;
}
.chapter-eyebrow {
  font-family: 'Roboto Mono', monospace;
  font-size: 10.5pt;
  letter-spacing: 0.14em;
  color: rgba(0,0,0,0.5);
  margin-bottom: 0.15in;
  text-transform: uppercase;
}
.chapter-title {
  font-size: 26pt;
  line-height: 1.25;
  margin: 0 0 0.35in 0;
  font-weight: 700;
}

.chapter h2 {
  font-size: 16pt;
  margin-top: 0.4in;
  margin-bottom: 0.15in;
  border-bottom: 1pt solid rgba(0,0,0,0.25);
  padding-bottom: 0.06in;
}
.chapter p { text-align: justify; margin: 0 0 0.16in 0; }
.chapter blockquote {
  border-right: 3pt solid #111;
  border-left: none;
  padding: 0.1in 0.25in 0.1in 0;
  margin: 0.25in 0;
  font-style: italic;
  color: rgba(0,0,0,0.75);
  font-size: 13.5pt;
}
.chapter ul, .chapter ol { margin: 0 0 0.16in 0; padding-right: 0.3in; padding-left: 0; }
.chapter li { margin-bottom: 0.08in; text-align: justify; }
.chapter strong { font-weight: 700; }
.chapter table { width: 100%; border-collapse: collapse; margin: 0.2in 0; font-size: 11pt; }
.chapter th, .chapter td { border: 0.5pt solid rgba(0,0,0,0.3); padding: 0.06in 0.1in; text-align: right; }
h1, h2, h3, h4 { break-after: avoid; }
p { orphans: 3; widows: 3; }
"""

if __name__ == "__main__":
    build()
