"""Validação do HTML Reveal.js após renderização Quarto no GitHub Actions.

Exige exatamente dez slides, incluindo capa, referências e obrigado, sem
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
if len(slides) != 10:
    errors.append(f"Esperados 10 slides, encontrados {len(slides)}")
if not slides or "slide-capa" not in slides[0]["class"]:
    errors.append("Primeiro slide não é a capa.")
if slides and "slide-fecho" not in slides[-1]["class"]:
    errors.append("Último slide não é o encerramento.")
if len(slides) >= 10:
    reference_text = " ".join(slides[-2]["text"]).lower()
    final_text = " ".join(slides[-1]["text"]).lower()
    if "referências" not in reference_text or "jcgm 100:2008" not in reference_text:
        errors.append("Penúltimo slide não contém referências.")
    for marker in ["obrigado!", "link da apresentação", "contato", "rcmayworm@gmail.com",
                   "site pessoal", "lattes", "linkedin"]:
        if marker not in final_text:
            errors.append(f"Slide final não contém: {marker}.")
    if "github.com/rcmayworm" in final_text or "github:" in final_text:
        errors.append("Slide final ainda contém GitHub.")
    if "encerramento" in final_text:
        errors.append("Slide final ainda contém o rótulo ENCERRAMENTO.")
    if final_text.count("e-mail") != 1 or final_text.count("site pessoal") != 1:
        errors.append("Os contatos não foram apresentados uma única vez.")
    for label in ["E-mail:", "Site pessoal:", "Currículo Lattes:", "LinkedIn:"]:
        if label.lower() not in final_text:
            errors.append(f"Contato sem rótulo e dois-pontos: {label}")
    for link in ["mailto:rcmayworm@gmail.com", "https://www.linkedin.com/in/ruanmayworm/",
                 "http://lattes.cnpq.br/5951712664292058", "https://rcmayworm.github.io/"]:
        if link not in html:
            errors.append(f"Link de contato ausente: {link}.")
if len(slides) >= 6:
    code_text = " ".join(slides[5]["text"]).lower()
    if "código python" not in code_text or "leituras_mm" not in code_text:
        errors.append("Slide de código Python ausente da sexta posição.")
if "sourceCode" not in html or "python" not in html:
    errors.append("Realce de sintaxe Python ausente.")
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
theme_css = theme_path.read_text(encoding="utf-8") if theme_path.is_file() else ""
if "grid-template-columns: minmax(0, 1fr);" not in theme_css or "width: 62%;" not in theme_css or "row-gap: 0.12em;" not in theme_css:
    errors.append("Contatos não configurados em coluna única à esquerda.")
if ".reveal .titulo-contato" not in theme_css or "margin-top: 1.75em;" not in theme_css:
    errors.append("Destaque do título CONTATO ausente.")
if not (html_path.parent / "template_files").is_dir():
    errors.append("Pasta template_files de recursos não gerada.")

if errors:
    for error in errors:
        print("FALHA:", error)
    sys.exit(1)
print("OK: 10 slides com Python, referências e contatos compactos.")
