"""Confere imagens históricas e capa preservada no artigo de metrologia PT/EN."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
slug = "a-fascinante-jornada-da-metrologia"
local_assets = [
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
    assert "fig-cap=" in content, f"Legenda ausente: {post}"
    assert re.search(r"!\[[^\]]+\]\(images/", content) if lang == "pt" else "../../../../blog/posts/" in content
print("OK: quatro imagens no corpo (três locais e uma fonte externa), capas preservadas em PT e EN.")
