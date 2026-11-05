"""Verificação estática da versão bilíngue do site Quarto (sem alterar o deploy)."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []
pages = (
    "index.qmd", "about.qmd", "research.qmd", "publications.qmd",
    "ebooks.qmd", "books.qmd", "software.qmd", "presentations.qmd",
    "contact.qmd", "blog/index.qmd",
)
posts_dir = ROOT / "blog/posts"
published_posts = [
    p.parent.name for p in posts_dir.glob("*/index.qmd")
    if not yaml.safe_load(p.read_text(encoding="utf-8").split("---", 2)[1]).get("draft", False)
]
cfg = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
navbar = cfg["website"]["navbar"]["right"]
if not any(item.get("text") == "PT" and item.get("href") == "/" for item in navbar):
    errors.append("Missing Portuguese language switch")
if not any(item.get("text") == "English" and item.get("href") == "/en/" for item in navbar):
    errors.append("Missing English language switch")
for flag in ("br.svg", "england.svg"):
    if not (ROOT / "assets/flags" / flag).is_file():
        errors.append(f"Missing local flag image: {flag}")
for hero_file in (ROOT / "index.qmd", ROOT / "en/index.qmd"):
    if '.academic-hero--profile' not in hero_file.read_text(encoding="utf-8"):
        errors.append(f"Shared home hero missing: {hero_file}")
if cfg["format"]["html"].get("include-after-body") != "language-switch.html":
    errors.append("Language-switch script not configured globally")
if not (ROOT / "language-switch.html").is_file():
    errors.append("Language-switch HTML include missing")
if yaml.safe_load((ROOT / "en/_metadata.yml").read_text(encoding="utf-8")).get("lang") != "en-GB":
    errors.append("English locale missing")

for rel in pages + tuple(f"blog/posts/{slug}/index.qmd" for slug in published_posts):
    pt = ROOT / rel
    en = ROOT / "en" / rel
    if not pt.is_file() or not en.is_file():
        errors.append(f"Missing language counterpart: {rel}")
        continue
    body = en.read_text(encoding="utf-8")
    if not body.startswith("---\n"):
        errors.append(f"English front matter missing: en/{rel}")
        continue
    fm = yaml.safe_load(body.split("---", 2)[1])
    if not fm.get("title") or not fm.get("description"):
        errors.append(f"Title or description absent: en/{rel}")
    if rel.startswith("blog/posts/") and fm.get("draft") is not False:
        errors.append(f"Published post incorrectly marked as draft: en/{rel}")

    # QMD links, local Markdown images and direct HTML image sources.
    refs = re.findall(r"(?<!!)\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)|src=['\"]([^'\"]+)['\"]", body)
    for options in refs:
        target = next((v for v in options if v), "")
        target = target.split("#", 1)[0].split("?", 1)[0].strip()
        if not target or target.startswith(("https://", "http://", "mailto:", "#", "data:")):
            continue
        # Drop attributes after the URL in Markdown links (not used in source now).
        target = target.split()[0]
        file_path = (ROOT / target.lstrip("/")) if target.startswith("/") else (en.parent / target)
        if target.endswith("/") and (file_path / "index.qmd").is_file():
            continue
        if not file_path.is_file() and not (
            file_path.suffix == ".html" and file_path.with_suffix(".qmd").is_file()
        ):
            errors.append(f"Broken local content reference: en/{rel} -> {target}")

    if rel.startswith("blog/posts/"):
        pt_body = pt.read_text(encoding="utf-8")
        pt_math = len(re.findall(r"\$\$[\s\S]*?\$\$", pt_body))
        en_math = len(re.findall(r"\$\$[\s\S]*?\$\$", body))
        if pt_math != en_math:
            errors.append(f"Display equation mismatch: en/{rel} {pt_math} vs {en_math}")
        for tag in re.findall(r"\{#((?:fig|tbl)-[^ \}]+)", pt_body):
            if "{#" + tag not in body:
                errors.append(f"Lost cross-reference anchor: en/{rel} {tag}")

if len(published_posts) != 5:
    errors.append(f"Expected 5 published blog posts, got {len(published_posts)}")
if errors:
    print("FAILED bilingual validation:")
    print("\n".join("- " + e for e in errors))
    sys.exit(1)
print(f"OK: {len(pages)} English website pages, {len(published_posts)} translated posts, language switch, references and mathematical cross-links.")
