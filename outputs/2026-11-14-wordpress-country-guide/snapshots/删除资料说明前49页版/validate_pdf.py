"""Check the generated PDF, research coverage, and distributable archive."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

import pdfplumber
from pypdf import PdfReader
from reportlab.pdfbase.ttfonts import TTFont

from build_pdf import FINAL, PACK, PDF_NAME, ROOT, WORK, ZIP_NAME, load_cases, load_pages, read_csv
from diagrams import FIGURES


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> None:
    pdf = FINAL / PDF_NAME
    reader = PdfReader(pdf)
    cases = load_cases()
    pages = load_pages(cases)
    texts = [page.extract_text() or "" for page in reader.pages]
    all_text = "\n".join(texts)
    dense_text = compact(all_text)
    assert len(reader.pages) == len(pages) == 49
    assert len(reader.outline) == 49
    assert len(cases) == 125

    missing_codes = [case.code for case in cases if case.code not in all_text]
    missing_names = [case.name for case in cases if compact(case.name) not in dense_text]
    assert not missing_codes and not missing_names, (missing_codes, missing_names)
    assert "三一重工" in all_text and "PDT R US" in all_text

    current_rows = list(csv.DictReader((PACK / "01_125组案例总表.csv").open(encoding="utf-8-sig")))
    previous_rows = list(csv.DictReader((ROOT / "outputs/2026-11-14-country-domain-visual-guide/领取资料包/01_125组案例总表.csv").open(encoding="utf-8-sig")))
    current_map = {row["编号"]: row["案例"] for row in current_rows}
    previous_map = {row["编号"]: row["案例"] for row in previous_rows}
    assert current_map == previous_map and len(current_map) == 125

    snapshot = WORK / "snapshots" / "方案能力改写前70页版"
    snapshot_rows = list(csv.DictReader((snapshot / "领取资料包" / "01_125组案例总表.csv").open(encoding="utf-8-sig")))
    link_columns = ["编号", "代表网址", "公开来源", "SEO项目原文"]
    preserved_case_sources = [[row[key] for key in link_columns] for row in current_rows] == [[row[key] for key in link_columns] for row in snapshot_rows]
    assert preserved_case_sources
    snapshot_manifest = json.loads((snapshot / "snapshot-manifest.json").read_text())
    snapshot_unchanged = all(digest(snapshot / relative) == expected for relative, expected in snapshot_manifest["files"].items())
    assert snapshot_unchanged
    research_tables_unchanged = all((PACK / name).read_bytes() == (snapshot / "领取资料包" / name).read_bytes()
                                    for name in ["01_125组案例总表.csv", "02_三一101对象分类表.csv", "03_包装60对象分类表.csv"])
    assert research_tables_unchanged
    previous_pdf_name = "AI外贸独立国家域名站群_WordPress运营版_125组案例与实操手册.pdf"
    prior_public_pdf_unchanged = digest(FINAL / previous_pdf_name) == digest(snapshot / "领取资料包" / previous_pdf_name)
    assert prior_public_pdf_unchanged
    narrative_snapshot = WORK / "snapshots" / "叙事重写前45页版"
    narrative_manifest = json.loads((narrative_snapshot / "snapshot-manifest.json").read_text())
    narrative_snapshot_unchanged = all(digest(narrative_snapshot / relative) == expected
                                      for relative, expected in narrative_manifest["files"].items())
    assert narrative_snapshot_unchanged

    packaging = read_csv("outputs/2026-11-05-site-network/站群域名与逐站证据.csv")
    sany = read_csv("outputs/2026-11-12-sany-global-network/三一全球站点与域名清单.csv")
    core_sany = [row["域名或子域"] for row in sany if row["分类"] == "集团与业务官网（高置信）"]
    missing_domains = [row["域名"] for row in packaging if row["域名"] not in dense_text]
    missing_domains += [domain for domain in core_sany if domain not in dense_text]
    assert len(packaging) == 47 and len(core_sany) == 25 and not missing_domains

    figure_keys = re.findall(r"\[diagram:([^\]]+)\]", (WORK / "book.md").read_text())
    assert len(figure_keys) == len(set(figure_keys)) == len(FIGURES) == 20
    assert set(figure_keys) == set(FIGURES)
    figures = []
    for number, page in enumerate(pages, 1):
        for key in re.findall(r"\[diagram:([^\]]+)\]", page.body):
            assert compact(FIGURES[key].label) in compact(texts[number - 1])
            figures.append({"page": number, "key": key, "label": FIGURES[key].label,
                            "description": FIGURES[key].description, "caption": FIGURES[key].caption})

    uris: list[str] = []
    toc_targets: list[int] = []
    page_references = {page.indirect_reference.idnum: i for i, page in enumerate(reader.pages, 1)
                       if page.indirect_reference is not None}
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            if "/A" in annotation and "/URI" in annotation["/A"]:
                uris.append(str(annotation["/A"]["/URI"]))
            elif "/Dest" in annotation:
                destination = annotation["/Dest"]
                assert len(destination) >= 2
                toc_targets.append(page_references[destination[0].idnum])
    toc_keys = ["history", "buyer_journey", "case_map", "old_cost", "solution_capabilities", "architectures", "methods"]
    expected_toc = [next(i for i, item in enumerate(pages, 1) if item.key == key) for key in toc_keys]
    assert toc_targets == expected_toc
    malformed = [uri for uri in uris if urlsplit(uri).scheme not in {"http", "https"}
                 or not urlsplit(uri).netloc or re.search(r"\s", uri)]
    assert not malformed, malformed

    tokens = ["/Users/", "/tmp/", "turn0view", "ZZLINK", "[diagram:", "<!--", "<font", "<link", "588f544d46ba8058582eccc2"]
    forbidden = [token for token in tokens if token in all_text]
    assert not forbidden, forbidden
    assert "2018下半年同比" in dense_text and "+100.53%" in all_text
    assert "145.53%" not in all_text
    required_sections = {"history", "mascus_results", "precision", "sany", "packaging", "seo_results", "old_cost",
                         "ai_economics", "solution_capabilities", "wordpress_value", "why_now"}
    assert required_sections <= {page.key for page in pages}
    assert "WordPressBuilderHarness" in dense_text and "B2BFastBuilder" in dense_text
    assert dense_text.count("WordPressAI建站课程") == 1
    assert all(label in dense_text for label in ["工厂老板", "SOHO", "外贸公司"])
    tutorial_terms = ["提示词", "实操", "保存重开", "首站启动表", "工作表", "验收表", "新增草稿", "后台栏目", "操作步骤"]
    assert not any(token in dense_text for token in tutorial_terms)
    solution_pages = [i for i, page in enumerate(pages, 1) if page.key in {"solution_capabilities", "wordpress_value", "why_now"}]
    assert len(solution_pages) == 3
    wordpress_pages = [i for i, text in enumerate(texts, 1) if "WordPress" in text]
    assert set(solution_pages) <= set(wordpress_pages), wordpress_pages
    assert all(token in dense_text for token in ["2011年", "32个国家域名", "25种语言", "+13.1%", "+38%", "专业翻译", "重复制作"])
    evidence_links = {
        "https://www.pressetext.com/news/na-20110302010.html",
        "https://www.europapress.es/economia/noticia-comunicado-onlineprinters-gmbh-abre-tienda-virtual-espana-20110727102414.html",
        "https://www.bluerank.com/wp-content/uploads/2021/05/Mascus-International_Bluerank_ESA2019_case-study_ENG_1.pdf",
        "https://www.inspiradigitalagency.com/case-studies/dextra-group/",
        "https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites",
    }
    assert evidence_links <= set(uris)

    glyph_maps = {name: TTFont(name, "/Library/Fonts/" + file).face.charToGlyph for name, file in
                  [("OPPOSans-R", "OPPOSans R.ttf"), ("OPPOSans-H", "OPPOSans H.ttf"), ("ArialMT", "Arial.ttf")]}
    missing_glyphs: list[tuple[int, str, str]] = []
    outside: list[tuple[int, str]] = []
    font_names: set[str] = set()
    with pdfplumber.open(pdf) as document:
        for number, page in enumerate(document.pages, 1):
            for char in page.chars:
                font = char["fontname"].split("+")[-1]
                font_names.add(font)
                assert font in glyph_maps, font
                for letter in char["text"]:
                    if letter.strip() and not glyph_maps[font].get(ord(letter)):
                        missing_glyphs.append((number, font, letter))
                if char["text"].strip() and (char["x0"] < 22 or char["x1"] > float(page.width) - 22
                                              or char["top"] < 20 or char["bottom"] > float(page.height) - 18):
                    outside.append((number, char["text"]))
    assert not missing_glyphs and not outside, (missing_glyphs, outside)

    csv_shapes: dict[str, dict[str, int]] = {}
    for path in PACK.glob("*.csv"):
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.reader(stream))
        assert len({len(row) for row in rows}) == 1, path.name
        csv_shapes[path.name] = {"data_rows": len(rows) - 1, "columns": len(rows[0])}
    assert csv_shapes["02_三一101对象分类表.csv"]["data_rows"] == 101
    assert csv_shapes["03_包装60对象分类表.csv"]["data_rows"] == 60
    assert len(csv_shapes) == 3
    public_text = "\n".join(path.read_text(encoding="utf-8-sig") for path in PACK.iterdir()
                            if path.suffix in {".csv", ".txt", ".md"})
    assert not any(token in public_text for token in tokens)

    with zipfile.ZipFile(FINAL / ZIP_NAME) as archive:
        bad_member = archive.testzip()
        members = archive.namelist()
        identical = archive.read(PDF_NAME) == pdf.read_bytes()
    assert bad_member is None and identical
    expected_members = {PDF_NAME, "01_125组案例总表.csv", "02_三一101对象分类表.csv", "03_包装60对象分类表.csv", "先读我.txt"}
    assert set(members) == expected_members
    assert not any(token in public_text for token in tutorial_terms)

    previous_hashes = json.loads((WORK / "previous-version-sha256.json").read_text())
    previous_unchanged = all(digest(ROOT / relative) == expected for relative, expected in previous_hashes.items())
    assert previous_unchanged
    groups = dict(Counter(case.group for case in cases))
    assert groups == {"主案例": 2, "中国制造": 21, "工业与 B2B": 71, "跨行业与架构参照": 31}
    report = {
        "checked_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "pages": len(reader.pages), "outline_entries": len(reader.outline), "figures": len(figures),
        "external_link_annotations": len(uris), "unique_external_uris": len(set(uris)),
        "toc_target_pages": toc_targets, "case_records": len(cases), "groups": groups,
        "case_number_name_map_preserved": current_map == previous_map,
        "all_case_urls_and_sources_preserved": preserved_case_sources,
        "reader_review_snapshot_unchanged": snapshot_unchanged,
        "three_research_tables_byte_identical": research_tables_unchanged,
        "prior_public_70_page_pdf_unchanged": prior_public_pdf_unchanged,
        "intermediate_45_page_snapshot_unchanged": narrative_snapshot_unchanged,
        "narrative_evidence_links_present": sorted(evidence_links),
        "solution_explanation_pages": solution_pages, "wordpress_mention_pages": wordpress_pages,
        "tutorial_material_excluded": True,
        "missing_names": missing_names, "missing_codes": missing_codes, "missing_domains": missing_domains,
        "packaging_core_domains": len(packaging), "sany_core_domains": len(core_sany),
        "fonts_checked": sorted(font_names), "missing_glyphs": missing_glyphs,
        "outside_page_safe_bounds": outside, "private_or_unrendered_text": forbidden,
        "malformed_uri_annotations": malformed, "csv_shapes": csv_shapes, "zip_members": members,
        "zip_bad_member": bad_member, "zip_contains_identical_pdf": identical,
        "previous_version_unchanged": previous_unchanged,
        "bytes": pdf.stat().st_size, "sha256": digest(pdf),
        "scope": "Text, glyph coverage, page bounds, links, catalog coverage and archive integrity checked. External sites were not all revisited; no Skill or website deployment was tested. Visual inspection is recorded separately.",
    }
    (WORK / "artifact-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    (WORK / "figure-inventory.json").write_text(json.dumps(figures, ensure_ascii=False, indent=2))
    (WORK / "extracted-text.txt").write_text(all_text)
    print(json.dumps({key: report[key] for key in ["checked_at", "pages", "figures", "case_records", "external_link_annotations", "unique_external_uris", "bytes", "sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
