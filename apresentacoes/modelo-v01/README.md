# Apresentações científicas — versão de avaliação v0.3

Modelo original Quarto + Reveal.js, com identidade visual própria do site acadêmico.
A referência visual do professor Jodavid Ferreira foi utilizada como inspiração; nenhum SCSS, gráfico ou ativo de terceiros foi copiado.

## Prévia pública

https://rcmayworm.github.io/previas/modelo-apresentacoes-v01/

Esta é uma prévia de trabalho, não uma publicação incorporada ao catálogo de palestras.
Todos os dados e sinais usados nos slides são demonstrativos e sintéticos.

## Uso

- **Setas**: anterior/próximo slide.
- **M**: menu de slides.
- **S**: notas do apresentador.
- **C**: desenhar sobre o slide atual.
- **B**: abrir ou fechar o quadro branco.
- **D**: exportar desenhos em JSON.
- **Del**: apagar os desenhos do slide.

Para gerar a apresentação, executar `quarto render template.qmd` dentro desta pasta.

## Offline: atenção à diferença entre formatos

O plugin nativo Chalkboard do Quarto **não é compatível** com `embed-resources: true`.
Portanto, a versão com quadro branco usa HTML **mais pasta de recursos**
(`template_files/` e `assets/`), incluídos no pacote ZIP gerado pelo GitHub Actions.

Baixe o ZIP `apresentacao-offline.zip`, extraia a pasta e abra o arquivo
`index.html`. **Não leve somente o HTML isolado**, pois ele perderá
recursos necessários à navegação e às anotações.

É possível gerar posteriormente outra versão HTML autocontida sem Chalkboard,
caso o requisito seja entregar um único arquivo.

## Revisões

v0.3: amplia as linhas de capa e encerramento, aumenta o afastamento do nome,
usa transições concave/convex e exibe o título em rodapé discreto.

v0.2: remove slides em branco gerados pelo conteúdo anterior à capa, fixa
`slide-level: 2`, elimina subtítulos interpretados como slides extras, identifica capa e encerramento e ajusta a largura da capa
e adiciona ferramentas de anotação e quadro branco.

O repositório não recebeu uma licença de distribuição de software.
