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
    assert "msc-conf.com/history-of-metrology/" in content, f"Fonte de imagem egípcia ausente: {post}"
    for name in local_assets:
        assert content.count(name) == 1, f"Imagem não referenciada uma vez: {post}, {name}"
        assert str(name.replace(".avif",".webp")) not in content
    assert content.count("::: {.metrology-history-figure}") == 4, f"Figuras sem classe de centralização: {post}"
    assert content.count("fig-cap=") >= 4, f"Legendas ausentes: {post}"
    assert "1738087115334.jpeg" not in content, f"Imagem remota quebrada: {post}"
    if lang == "pt":
        assert "O côvado mestre real, com 52,9 cm, era o padrão primário esculpido em granito." in content
        assert "Cartaz da Revolta do Quebra-Quilos." in content
        assert "O relógio atômico do Instituto Nacional de Metrologia da Alemanha" in content
    else:
        assert "The royal master cubit, measuring 52.9 cm" in content
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert ".metrology-history-figure figcaption" in css
    assert re.search(r"!\[[^\]]+\]\(images/", content) if lang == "pt" else "../../../../blog/posts/" in content
print("OK: quatro imagens locais com legendas centralizadas, capas preservadas em PT e EN.")
