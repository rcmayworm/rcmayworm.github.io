"""Validação estática do site Quarto. Não substitui renderização ou teste visual."""
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.qmd", "about.qmd", "research.qmd", "publications.qmd", "books.qmd", "ebooks.qmd", "software.qmd", "contact.qmd", "blog/index.qmd"]
errors = []
config_text = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
if yaml:
    try:
        config = yaml.safe_load(config_text)
        assert config["project"]["type"] == "website"
        links = str(config["website"]["navbar"])
        for target in ["index.qmd", "research.qmd", "publications.qmd", "blog/index.qmd", "ebooks.qmd"]:
            if target not in links:
                errors.append(f"Navegação ausente: {target}")
    except Exception as ex:
        errors.append(f"Configuração YAML inválida: {ex}")
else:
    errors.append("PyYAML indisponível; validação do YAML não executada")

for relative in PAGES + ["blog/posts/modelo-de-post/index.qmd"]:
    p = ROOT / relative
    if not p.is_file():
        errors.append(f"Arquivo ausente: {relative}")
        continue
    content = p.read_text(encoding="utf-8")
    if not content.startswith("---\n") or "\n---\n" not in content:
        errors.append(f"Front matter ausente: {relative}")
    elif yaml:
        try:
            fm = content.split("---", 2)[1]
            yaml.safe_load(fm)
        except Exception as ex:
            errors.append(f"YAML inválido em {relative}: {ex}")
    for target in re.findall(r'\]\(([^)#]+?\.qmd)(?:#[^)]*)?\)', content):
        if not (p.parent / target).is_file():
            errors.append(f"Link interno inválido: {relative} -> {target}")
    for target in re.findall(r'href="([^"]+\.qmd)"', content):
        errors.append(f"Link HTML para .qmd (não reescrito automaticamente): {relative} -> {target}")
    for target in re.findall(r'href="([^"#:]+\.html)"', content):
        if not (p.parent / target.replace('.html', '.qmd')).is_file():
            errors.append(f"Link HTML sem fonte .qmd: {relative} -> {target}")

# Evita aplicar classes de título a uma <section> gerada pelo Quarto.
home = (ROOT / 'index.qmd').read_text(encoding='utf-8')
if '# Ruan Mayworm {.hero-title}' in home:
    errors.append('Título no hero não pode ser Markdown H1: Quarto cria section com a classe hero-title')
if '<h1 class="hero-title">Ruan Mayworm</h1>' not in home:
    errors.append('H1 semântico do hero não localizado')
css_text = (ROOT / 'styles.css').read_text(encoding='utf-8') if (ROOT / 'styles.css').is_file() else ''
if '.academic-hero h1.hero-title' not in css_text:
    errors.append('CSS do hero deve atingir apenas o título H1')

# A foto do bloco principal deve estar versionada, sem depender de hospedagem externa.
photo_match = re.search(r'<img class="hero-portrait" src="(assets/images/[^"]+)"', home)
if not photo_match:
    errors.append('Página inicial não referencia uma foto profissional local')
else:
    photo = ROOT / photo_match.group(1)
    if not photo.is_file():
        errors.append(f'Retrato referenciado não localizado: {photo_match.group(1)}')
if 'alt="Retrato de Ruan Mayworm' not in home:
    errors.append('Texto alternativo do retrato ausente')

# Post autoral publicado: conferir arquivos, referências e figuras independentes de terceiros.
article_dir = ROOT / 'blog/posts/a-fascinante-jornada-da-metrologia'
article = article_dir / 'index.qmd'
if not article.is_file():
    errors.append('Postagem histórica de metrologia ausente')
else:
    article_text = article.read_text(encoding='utf-8')
    if 'draft: false' not in article_text:
        errors.append('Artigo histórico ainda marcado como rascunho')
    if yaml:
        try:
            article_frontmatter = yaml.safe_load(article_text.split('---', 2)[1])
            assert article_frontmatter['author'] == 'Ruan Mayworm'
            assert article_frontmatter['image'] == 'images/capa-historia.svg'
        except Exception as ex:
            errors.append(f'Metadados do artigo histórico inválidos: {ex}')
    figures = ['capa-historia.svg', 'covado-real.svg', 'quebra-quilos.svg', 'padroes-si.svg']
    for figure in figures:
        asset = article_dir / 'images' / figure
        if not asset.is_file():
            errors.append(f'Ilustração ausente: {figure}')
        elif f'images/{figure}' not in article_text:
            errors.append(f'Ilustração não referenciada: {figure}')
        else:
            from xml.etree import ElementTree
            try:
                ElementTree.parse(asset)
            except Exception as ex:
                errors.append(f'SVG inválido {figure}: {ex}')

post = ROOT / 'blog/posts/modelo-de-post/index.qmd'
if post.is_file() and 'draft: true' not in post.read_text(encoding='utf-8'):
    errors.append('Postagem demonstrativa deve permanecer rascunho')
blog = ROOT / 'blog/index.qmd'
if blog.is_file():
    c=blog.read_text(encoding='utf-8')
    if 'contents: posts' not in c or 'categories: true' not in c:
        errors.append('Listagem automática do blog ausente')
pubs = (ROOT / 'publications.qmd').read_text(encoding='utf-8')
dois = re.findall(r'https://doi\.org/([^\s)]+)', pubs)
if len(dois) != 11 or len(set(dois)) != 11:
    errors.append(f'Bibliografia com {len(dois)} DOI, {len(set(dois))} únicos; esperado 11')
if not (ROOT / 'styles.css').is_file():
    errors.append('CSS do tema não localizado')
if (ROOT / 'LICENSE').exists():
    errors.append('Licença criada sem decisão editorial')
# Book: ensure all HTML chapters and local figures exist and PDF is not public.
BOOK = ROOT / 'livro-analise-certificados'
if not (BOOK / '_quarto.yml').is_file():
    errors.append('Livro online Quarto não encontrado')
elif yaml:
    try:
        book_config = yaml.safe_load((BOOK / '_quarto.yml').read_text(encoding='utf-8'))
        if book_config.get('project', {}).get('type') != 'book':
            errors.append('Subprojeto do livro deve ser Quarto Book')
        for chapter in book_config['book']['chapters'] + book_config['book'].get('appendices', []):
            if not (BOOK / chapter).is_file():
                errors.append(f'Capítulo ausente: {chapter}')
        for ch in BOOK.glob('*.qmd'):
            for pic in re.findall(r'assets/figuras/[A-Za-z0-9_-]+\\.webp', ch.read_text(encoding='utf-8')):
                if not (BOOK / pic).is_file():
                    errors.append(f'Figura ausente: {ch.name} -> {pic}')
    except Exception as ex:
        errors.append(f'Livro Quarto inválido: {ex}')
if not (BOOK / 'assets/capa.webp').is_file():
    errors.append('Capa do livro ausente')
if list(BOOK.rglob('*.pdf')):
    errors.append('PDF comercial não deve constar no repositório público')
if 'https://rcmayworm.github.io/livro-analise-certificados/' not in (ROOT / 'ebooks.qmd').read_text(encoding='utf-8'):
    errors.append('Catálogo não possui link de leitura online')

if errors:
    print('FALHA:')
    for msg in errors: print(' -', msg)
    sys.exit(1)
print('OK: páginas e navegação, YAML, links internos, blog em rascunho, 11 DOI, CSS e workflow presente.')
print('Pendente: quarto render, validação do HTML renderizado, visual em navegadores e revisão bibliográfica final.')
