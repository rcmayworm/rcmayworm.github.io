"""Confere a estrutura gerada pelo Quarto para o carrossel na home.

Executado após `quarto render`, antes do deploy. Verificações de interação
em navegador permanecem testes separados.
"""
from html.parser import HTMLParser
from pathlib import Path

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.classes = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if attrs.get('class'):
            self.classes.append(set(attrs['class'].split()))
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])

home = Path('_site/index.html')
assert home.is_file(), 'HTML principal do site não encontrado'
text = home.read_text(encoding='utf-8')
parser = Tags()
parser.feed(text)
assert {'blog-prev', 'blog-next'}.issubset(parser.ids), 'Botões do carrossel não existem'
assert any(i in parser.ids for i in ('listing-home-blog-listing', 'home-blog-listing')), 'Identificador da listagem diferente do esperado'
assert any({'list', 'grid'}.issubset(cs) or 'quarto-listing-grid' in cs for cs in parser.classes), 'Grid do Quarto não encontrado'
blog_links = {href for href in parser.links if 'blog/posts/' in href}
assert len(blog_links) >= 5, f'Esperados ao menos cinco artigos; encontrados {len(blog_links)}'
assert 'home-blog.js' in text and 'home-enhancements.css' in text, 'Recursos do carrossel não vinculados'
assert Path('_site/home-blog.js').is_file(), 'JavaScript do carrossel não publicado'
assert Path('_site/home-enhancements.css').is_file(), 'CSS do carrossel não publicado'
print(f'OK: HTML do Quarto, listagem com {len(blog_links)} artigos e recursos do carrossel.')


# Regressão: somente os cinco artigos da língua correspondente em cada home.
# O glob anterior "blog/posts/*/index.qmd" selecionava também "en/blog/posts"
# no Quarto 1.x. Os links são verificados no HTML efetivamente renderizado.
from urllib.parse import urljoin, urlsplit

SLUGS = {
    "a-fascinante-jornada-da-metrologia",
    "analise-critica-certificados-calibracao",
    "exatidao-e-precisao",
    "incerteza-regressao-linear-python",
    "intervalos-entre-calibracoes",
}

class HomeListingLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.found = False
        self.links = []
        self.cards = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'div':
            if self.depth:
                self.depth += 1
            elif attributes.get('id') == 'listing-home-blog-listing':
                self.depth = 1
                self.found = True
            if self.depth and 'quarto-grid-item' in attributes.get('class', '').split():
                self.cards += 1
        if self.depth and tag == 'a':
            href = attributes.get('href', '')
            if '/blog/posts/' in href or 'blog/posts/' in href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == 'div' and self.depth:
            self.depth -= 1

for lang, location in (('pt', 'index.html'), ('en', 'en/index.html')):
    path = Path('_site') / location
    assert path.is_file(), f'Home {lang} não renderizada: {path}'
    listing = HomeListingLinks()
    listing.feed(path.read_text(encoding='utf-8'))
    assert listing.found, f'Listagem de blog ausente da home {lang}'
    base_url = f'https://rcmayworm.github.io/{"en/" if lang == "en" else ""}'
    urls = [urlsplit(urljoin(base_url, href)).path for href in listing.links]
    expected = {f'/{"en/" if lang == "en" else ""}blog/posts/{slug}/index.html' for slug in SLUGS}
    assert listing.cards == len(SLUGS), (
        f'Home {lang}: esperado {len(SLUGS)} cartões e encontrados {listing.cards}'
    )
    assert len(urls) == len(SLUGS) and set(urls) == expected, (
        f'Home {lang}: lista incorreta de artigos: {urls}'
    )
    print(f'OK: home {lang} contém exatamente cinco artigos do idioma correto.')
