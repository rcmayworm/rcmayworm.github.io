"""Verifica convenções editoriais nos artigos publicados do blog bilíngue."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SLUGS = [
    "a-fascinante-jornada-da-metrologia",
    "analise-critica-certificados-calibracao",
    "exatidao-e-precisao",
    "incerteza-regressao-linear-python",
    "intervalos-entre-calibracoes",
]
errors = []
reference_bodies = {"pt": {}, "en": {}}
for locale in ("pt", "en"):
    prefix = "en/" if locale == "en" else ""
    references = "## References and Sources" if locale == "en" else "## Referências e fontes"
    further = "## Further Reading" if locale == "en" else "## Leia mais"
    titles = {}
    for slug in SLUGS:
        path = ROOT / prefix / "blog/posts" / slug / "index.qmd"
        if not path.is_file():
            errors.append(f"Artigo não encontrado: {path}")
            continue
        content = path.read_text(encoding="utf-8")
        meta = yaml.safe_load(content.split("---", 2)[1])
        titles[slug] = meta.get("title", "")
        if meta.get("draft") is not False:
            errors.append(f"Artigo publicado está em draft: {path}")
        if content.count(references) != 1 or content.count(further) != 1:
            errors.append(f"Seções editoriais ausentes/repetidas: {path}")
            continue
        bib_start = content.index(references)
        read_start = content.index(further)
        if bib_start >= read_start:
            errors.append(f"Ordem incorreta das seções: {path}")
        reference_bodies[locale][slug] = content[bib_start:read_start]
        reading = content[read_start:]
        for title_slug in SLUGS:
            if title_slug == slug:
                expected = "(this article)" if locale == "en" else "(este artigo)"
                if expected not in reading:
                    errors.append(f"Autorreferência não identificada: {path}")
            elif f"../{title_slug}/index.qmd" not in reading:
                errors.append(f"Artigo ausente em leituras complementares: {path} -> {title_slug}")
        # Distinguish latex decimal-comma notation from comma-separated lists,
        # bibliographic author names and English thousands separators.
        if locale == "en" and re.search(r"\d\{,\}\d", content):
            errors.append(f"Vírgula decimal em expressão matemática inglesa: {path}")
        if locale == "en" and re.search(r"\$[^\n$]*\d,\d[^\n$]*\$", content):
            errors.append(f"Vírgula decimal em matemática inline inglesa: {path}")
        if locale == "pt" and slug == "exatidao-e-precisao":
            if r"E=99{,}98-100{,}00=-0{,}02" not in content:
                errors.append("Expressão original em português alterada.")
        if locale == "en" and slug == "exatidao-e-precisao":
            if r"E=99.98-100.00=-0.02" not in content:
                errors.append("Expressão do erro não está em notação inglesa.")
        if locale == "en" and slug == "incerteza-regressao-linear-python":
            for expected in (r"5.0423\,V - 0.4863", r"k\approx2.262",
                             r"s=0.7062", r"0.6388"):
                if expected not in content:
                    errors.append(f"Resultado numérico inglês ausente: {expected}")

    for slug in SLUGS:
        path = ROOT / prefix / "blog/posts" / slug / "index.qmd"
        if path.is_file() and path.read_text(encoding="utf-8").count("## ") < 3:
            errors.append(f"Estrutura de artigo suspeita: {path}")

    # Repeated bibliographic references must have identical canonical entries.
    shared_refs = (
        ("JCGM 100:2008(E)", [
            "analise-critica-certificados-calibracao",
            "exatidao-e-precisao",
            "incerteza-regressao-linear-python",
        ], "10.59161/JCGM100-2008E"),
        ("JCGM 200:2012", [
            "a-fascinante-jornada-da-metrologia",
            "analise-critica-certificados-calibracao",
            "exatidao-e-precisao",
        ], "10.59161/JCGM200-2012"),
        ("BIPM", [
            "a-fascinante-jornada-da-metrologia",
            "exatidao-e-precisao",
        ], "10.59161/AUEZ1291"),
        ("Mendes, A.; Rosário, P. P.", [
            "analise-critica-certificados-calibracao",
            "exatidao-e-precisao",
        ], "9788521636755"),
    )
    for name, used_by, identifier in shared_refs:
        entries = []
        for slug in used_by:
            bib = reference_bodies[locale].get(slug, "")
            line = next((l for l in bib.splitlines() if l.startswith(f"- **{name}.")), "")
            if not line or identifier not in line:
                errors.append(f"Referência recorrente sem identificador: {locale}/{slug} {name}")
            else:
                # Additional item-specific definition links may follow a complete citation.
                # DOI links end the canonical citation; any topical definitions are optional.
                match = re.match(r"^(.*?\]\(https://doi\.org/10\.59161/[^)]+\)\.)", line)
                entries.append(match.group(1) if match else line)
        if len(entries) > 1 and len(set(entries)) != 1:
            errors.append(f"Referência com forma divergente: {locale} {name}")

if errors:
    for e in errors:
        print("FALHA:", e)
    sys.exit(1)
print("OK: 10 artigos, títulos de referência, 5 leituras por artigo, decimais e citações compartilhadas.")
