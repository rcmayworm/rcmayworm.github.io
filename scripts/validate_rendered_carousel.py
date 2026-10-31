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
