# Análise Crítica de Certificados de Calibração — livro online

Versão online de Quarto Book, convertida a partir de `main.tex` e da primeira edição em PDF fornecidos pelo autor. A redação original foi preservada; a conversão não substitui revisão científica/editorial.

## Executar localmente

1. Instalar o [Quarto CLI](https://quarto.org/docs/get-started/).
2. Na raiz desta pasta, executar `quarto render --to html`.
3. Abrir `_book/index.html` ou executar `quarto preview`.

A configuração contém **apenas HTML**, sem target PDF ou EPUB. Não adicionar `downloads: [pdf]` ao livro: o PDF é um produto separado a ser vendido na Hotmart.

## Link da edição PDF (Hotmart)

O link fornecido pelo autor foi incluído na página `comprar-pdf.qmd` e na apresentação do livro em `index.qmd`:

https://go.hotmart.com/F105183714N

O destino final do redirecionamento e o funcionamento do checkout **não foram confirmados** neste ambiente. Antes da publicação, verificar manualmente se a página abre o produto correto e se a compra é disponibilizada normalmente.

O PDF original não é distribuído no repositório nem nos arquivos gerados para o site. O conteúdo HTML continua público e pode ser copiado ou impresso pelos visitantes; isso não constitui proteção anticópia.

## Publicar via GitHub Pages

Usar um repositório separado para o livro, integrado à página Livros do site principal. Confirmar primeiro conta GitHub, repositório, URL de publicação e autorização explícita do autor. Com acesso configurado, renderizar, verificar links e só depois executar o deploy usando mecanismos oficiais do Quarto.

## Pendências editoriais antes de publicação

- Conferir rigor metrológico de regras de decisão, riscos estatísticos e termos normativos; ver exemplos específicos em `NOTAS_DE_CONVERSAO.md`.
- Conferir as referências bibliográficas, regras de uso de marcas RBC e ILAC e licenças das demais figuras.
- Comparar cada seção com o PDF, especialmente a ordem dos 5 quadros e 6 figuras originais e as caixas laterais da classe Tufte.
- Definir termos de uso do conteúdo HTML e direitos da edição comercial em PDF.
- Link Hotmart recebido e incorporado; verificar redirecionamento final e checkout antes da publicação.

Status: **preparado para integração ao GitHub Pages do site acadêmico**, sujeito à conclusão do build e deploy.
