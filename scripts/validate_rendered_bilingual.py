"""Validação do HTML bilíngue após quarto render."""
from pathlib import Path
from html.parser import HTMLParser

SITE = Path("_site")
PAGES = ["index.html", "about.html", "research.html", "publications.html",
         "ebooks.html", "books.html", "software.html", "presentations.html",
         "contact.html", "blog/index.html"]
POSTS = [
    "a-fascinante-jornada-da-metrologia",
    "analise-critica-certificados-calibracao",
    "exatidao-e-precisao",
    "incerteza-regressao-linear-python",
    "intervalos-entre-calibracoes",
]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = ""
        self.links = []
        self.imgs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img" and attrs.get("src"):
            self.imgs.append(attrs["src"])

for rel in PAGES + [f"blog/posts/{slug}/index.html" for slug in POSTS]:
    path = SITE / "en" / rel
    assert path.exists(), f"Missing rendered English page: {path}"
    html = path.read_text(encoding="utf-8")
    p = Page()
    p.feed(html)
    assert p.lang.lower().startswith("en"), f"Incorrect HTML language in {path}: {p.lang!r}"
    assert "English" in html and "PT" in html, f"Language switch missing from {path}"
    assert "window.location.pathname" in html, f"Language navigation JS missing from {path}"
    for img in p.imgs:
        if img.startswith(("http:", "https:", "data:")):
            continue
        local = (path.parent / img.split("?", 1)[0]).resolve()
        assert local.is_file(), f"Broken image in {path}: {img}"

english_home = (SITE / "en/index.html").read_text(encoding="utf-8")
for slug in POSTS:
    assert slug in english_home, f"Post {slug} missing from English home listing"
assert (SITE / "index.html").is_file(), "Portuguese root page missing"
assert (SITE / "blog/index.html").is_file(), "Portuguese blog missing"
for flag in ("br.svg", "england.svg"):
    assert (SITE / "assets/flags" / flag).is_file(), f"Local flag resource missing: {flag}"
for home_path in (SITE / "index.html", SITE / "en/index.html"):
    home_html = home_path.read_text(encoding="utf-8")
    assert 'academic-hero--profile' in home_html, f"Home layout missing: {home_path}"
print("OK: English HTML, five translated blog posts, flags, language tags, images and original routes.")
