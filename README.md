# Site acadêmico — Ruan Mayworm

Código-fonte do site pessoal em Quarto Website, com Blog e E-books.

## Estrutura

- `index.qmd`: página inicial, pesquisa e destaques científicos.
- `about.qmd`, `research.qmd`, `publications.qmd`, `software.qmd`, `contact.qmd`: conteúdo acadêmico.
- `blog/index.qmd`: listagem automática de postagens; `blog/posts/modelo-de-post/index.qmd` é um rascunho com `draft: true` e não aparece no site publicado.
- `ebooks.qmd`: catálogo com acesso ao livro online gratuito e edição PDF comercial.
- `_quarto.yml` e `styles.css`: navegação, metadados e aparência.
- `.github/workflows/pages.yml`: validação, renderização e publicação automática em GitHub Pages.
- `scripts/validate_site.py`: verificações estáticas do código-fonte.

## Idiomas (PT-BR / EN-GB)

- O conteúdo original permanece na raiz: `/index.html`, `/about.html`, `/blog/` e `/blog/posts/<slug>/`.
- A versão inglesa usa URLs paralelas: `/en/index.html`, `/en/about.html`, `/en/blog/` e `/en/blog/posts/<slug>/`.
- `en/_metadata.yml` define `lang: en-GB` para as páginas em inglês.
- `_quarto.yml` apresenta 🇧🇷 Português / 🇬🇧 English na barra superior. `language-switch.html` mapeia os links para a **mesma página** no idioma selecionado e localiza a navegação inglesa.
- As imagens e os scripts de pesquisa são compartilhados sempre que possível. Posts ingleses referenciam os mesmos arquivos de figuras e o código Python original.
- Cada artigo novo publicado em português requer uma versão em `en/blog/posts/<slug>/index.qmd` antes de ser considerado bilíngue. A automação **não traduz** o texto.
- Títulos, resumos, legendas e texto acadêmico em inglês devem passar por revisão editorial humana; preservar equações, unidades, resultados, citações e links.
- O livro Quarto em `livro-analise-certificados/` permanece **somente em português**. A página inglesa `en/ebooks.qmd` informa essa limitação e mantém os links originais.

### Teste sem publicação

A branch de testes usa `.github/workflows/validate-bilingual.yml` para executar:

```sh
python -m pip install PyYAML
python scripts/validate_site.py
python scripts/validate_bilingual.py
quarto render
python scripts/validate_rendered_carousel.py
python scripts/validate_rendered_bilingual.py
```

Esse workflow **não faz deploy**. Apenas a branch `main` aciona o workflow de publicação atual. A versão anterior está preservada em `backup/site-antes-bilingue-2026-11-05`.

## Publicação

1. Em **Settings → Pages → Build and deployment → Source**, selecionar **GitHub Actions**.
2. Verificar o workflow em **Actions**; a publicação concluída será indicada com sucesso do job `deploy`.
3. Conferir https://rcmayworm.github.io/ e as páginas internas em computadores e dispositivos móveis.

O procedimento não requer tokens pessoais. O `GITHUB_TOKEN` padrão das Actions é suficiente no fluxo de publicação por artefato, sujeito às permissões e configurações da conta.

## Desenvolvimento local

```sh
quarto preview
python -m pip install PyYAML
python scripts/validate_site.py
quarto render
```

O HTML é gerado em `_site/`. A validação de conteúdo e links deve ocorrer antes da publicação.

## Atualização de conteúdo

- Novo post: crie `blog/posts/<slug>/index.qmd` com título, data, categorias, texto e referências. Use `draft: true` enquanto estiver em revisão.
- E-books: cada livro deve ser publicado em projeto Quarto Book independente; edite `ebooks.qmd` somente após haver URL/arquivos reais.
- Mudanças no branch `main` são publicadas automaticamente pelo workflow, depois que o GitHub Pages estiver configurado.

## Restrições editoriais

- Não adicionar dados sensíveis, imagens de laboratório não autorizadas ou resultados inéditos ao repositório público.
- O livro **Análise Crítica de Certificados de Calibração** é gratuito para leitura HTML, e a edição PDF é comercializada separadamente pela Hotmart.
- Nenhuma licença explícita foi definida para o projeto.

## Quarto Book — Análise Crítica de Certificados de Calibração

- Fontes em `livro-analise-certificados/` (capítulos, imagens e bibliografia).
- Renderizar localmente: `quarto render livro-analise-certificados --to html`.
- O workflow integra `_book/` ao caminho `_site/livro-analise-certificados/` antes do deploy.
- A edição comercial em PDF não é versionada nem publicada no GitHub Pages.
- Notas editoriais na página `livro-analise-certificados/revisao-editorial.qmd`.
