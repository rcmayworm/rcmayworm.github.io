# Site acadêmico — Ruan Mayworm

Código-fonte do site pessoal em Quarto Website, com Blog e E-books.

## Estrutura

- `index.qmd`: página inicial, pesquisa e destaques científicos.
- `about.qmd`, `research.qmd`, `publications.qmd`, `software.qmd`, `contact.qmd`: conteúdo acadêmico.
- `blog/index.qmd`: listagem automática de postagens; `blog/posts/modelo-de-post/index.qmd` é um rascunho com `draft: true` e não aparece no site publicado.
- `ebooks.qmd`: catálogo de livros, ainda sem downloads ou livros publicados.
- `_quarto.yml` e `styles.css`: navegação, metadados e aparência.
- `.github/workflows/pages.yml`: validação, renderização e publicação automática em GitHub Pages.
- `scripts/validate_site.py`: verificações estáticas do código-fonte.

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
- O primeiro livro é apenas uma proposta editorial; não há downloads disponíveis.
- Nenhuma licença explícita foi definida para o projeto.
