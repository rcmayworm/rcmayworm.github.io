"""Confere imagens históricas e capa preservada no artigo de metrologia PT/EN."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
slug = "a-fascinante-jornada-da-metrologia"
local_assets = [
    "papiro-egipcio.avif",
    "covado-egipcio.avif",
    "rotulo-quebra-quilos.avif",
    "relogio-atomico-ptb.avif",
]
asset_root = ROOT / "blog" / "posts" / slug / "images"
for name in local_assets:
    file = asset_root / name
    assert file.is_file(), f"Arquivo ausente: {file}"
    assert file.stat().st_size > 1000, f"Imagem inesperadamente pequena: {file}"
    assert file.read_bytes()[4:12] == b"ftypavif", f"Arquivo AVIF inválido: {file}"

for lang, prefix in (("pt", ""), ("en", "en/")):
    post = ROOT / prefix / "blog" / "posts" / slug / "index.qmd"
    content = post.read_text(encoding="utf-8")
    assert "capa-historia.webp" in content, f"Capa alterada: {post}"
    assert "https://commons.wikimedia.org/wiki/File:Egypt.Papyrus.01c.jpg" in content, f"Fonte atual da imagem egípcia ausente: {post}"
    for name in local_assets:
        assert content.count(name) == 1, f"Imagem não referenciada uma vez: {post}, {name}"
        assert str(name.replace(".avif",".webp")) not in content
    assert content.count("::: {.metrology-history-figure}") == 4, f"Figuras sem classe de centralização: {post}"
    assert content.count("<figcaption>") == 4, f"Legendas visíveis ausentes: {post}"
    assert content.count("<figure>") == 4, f"Estrutura semântica ausente: {post}"
    assert content.count(" loading=\"lazy\" decoding=\"async\"") == 4, f"Imagens sem otimização de carregamento: {post}"
    assert "1738087115334.jpeg" not in content, f"Imagem remota quebrada: {post}"
    # As duas legendas devem terminar exatamente após o link do Wikimedia Commons.
    capt = next((line for line in content.splitlines() if "<figcaption>" in line and "Wikimedia Commons</a>" in line), "")
    assert capt.endswith("Wikimedia Commons</a></figcaption>"), f"Legenda do papiro não encerra no link Wikimedia Commons: {post}"
    assert "Hajor (2002)" in capt, f"Créditos da imagem ausentes no atributo title: {post}"
    assert content.count("(Physikalisch-Technische Bundesanstalt - PTB)") == 1, f"Nome oficial do PTB ausente: {post}"
    assert "Physical Technical Federal Institution" not in content, f"Nome antigo do PTB persistente: {post}"
    if lang == "pt":
        assert "O côvado mestre real, com 52,9 cm, era o padrão primário esculpido em granito." in content
        assert "Cartaz da Revolta do Quebra-Quilos." in content
        assert "O relógio atômico do Instituto Nacional de Metrologia da Alemanha" in content
    else:
        assert "The royal master cubit, measuring 52.9 cm" in content
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert ".metrology-history-figure figcaption" in css
    if lang == "pt":
        assert 'src="images/papiro-egipcio.avif"' in content, f"Caminho local incorreto: {post}"
    else:
        assert 'src="../../../../blog/posts/a-fascinante-jornada-da-metrologia/images/papiro-egipcio.avif"' in content, f"Caminho inglês incorreto: {post}"
print("OK: quatro imagens locais com legendas centralizadas, capas preservadas em PT e EN.")
