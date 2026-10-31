"""Validação do HTML Reveal.js após renderização Quarto no GitHub Actions.

Exige exatamente oito slides, incluindo capa inicial e encerramento, sem
slide vazio, além de checar os controles de anotações e os arquivos auxiliares.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


class RevealSlidesParser(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.stack = []
        self.sections = []
        self.in_slide_depth = None
        self.in_section_depth = None

    def handle_starttag(self, tag, attrs):
        att = dict(attrs)
        if tag == "div" and "slides" in att.get("class", "").split():
            self.in_slide_depth = len(self.stack)
        if tag == "section" and self.in_slide_depth is not None:
            self.sections.append({"id": att.get("id", ""),
                                  "class": att.get("class", ""),
                                  "text": []})
            self.in_section_depth = len(self.stack)
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                if self.in_section_depth is not None and i == self.in_section_depth:
                    self.in_section_depth = None
                if self.in_slide_depth is not None and i == self.in_slide_depth:
                    self.in_slide_depth = None
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        if self.in_section_depth is not None and self.sections:
            self.sections[-1]["text"].append(data.strip())


html_path = Path("apresentacoes/modelo-v01/template.html")
if not html_path.is_file():
    sys.exit(f"FALHA: HTML renderizado ausente: {html_path}")

html = html_path.read_text(encoding="utf-8")
parser = RevealSlidesParser()
parser.feed(html)
slides = parser.sections
report = [
    {"index": i+1, "id": slide["id"], "class": slide["class"],
     "characters": len(" ".join(slide["text"]).strip())}
    for i, slide in enumerate(slides)
]
print("Slides renderizados:")
for r in report:
    print("  {index}: id={id}, class={class}, chars={characters}".format(**r))

errors = []
if len(slides) != 8:
    errors.append(f"Esperados 8 slides, encontrados {len(slides)}")
if not slides or "slide-capa" not in slides[0]["class"]:
    errors.append("Primeiro slide não é a capa.")
if slides and "slide-fecho" not in slides[-1]["class"]:
    errors.append("Último slide não é o encerramento.")
if any(r["characters"] < 40 for r in report):
    errors.append("Existe slide vazio ou com conteúdo inesperadamente curto.")
if "chalkboard" not in html.lower():
    errors.append("Plugin de anotações/chalkboard ausente do HTML.")
if "menu" not in html.lower():
    errors.append("Menu Reveal.js ausente do HTML.")
if not re.search(r"""transition:\s*['"]concave['"]""", html):
    errors.append("Efeito de transição concave ausente.")
if not re.search(r"""backgroundTransition:\s*['"]convex['"]""", html):
    errors.append("Efeito de fundo convex ausente.")
if 'class="footer footer-default"' not in html or "Metrologia, dados e decisões confiáveis" not in html:
    errors.append("Título discreto no rodapé ausente.")
theme_path = html_path.parent / "tema.scss"
if not theme_path.is_file() or "width: 100%; max-width: 100%;" not in theme_path.read_text(encoding="utf-8"):
    errors.append("Linha horizontal de capa/encerramento não atualizada.")
if not (html_path.parent / "template_files").is_dir():
    errors.append("Pasta template_files de recursos não gerada.")

if errors:
    for error in errors:
        print("FALHA:", error)
    sys.exit(1)
print("OK: 8 slides completos, capa inicial, encerramento e recursos Reveal.js.")
