from __future__ import annotations

import csv
import html
import json
import math
import re
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, TypedDict
from urllib.parse import urlsplit

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable, Paragraph, Spacer, Table, TableStyle

from diagrams import FIGURES, Diagram


ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
FINAL = ROOT / "output" / "pdf"
PACK = WORK / "案例研究资料包"
TEMP = ROOT / "tmp" / "pdfs" / "case-capabilities-1114"
PDF_NAME = "AI外贸独立国家域名站群_125组案例与方案解读.pdf"
ZIP_NAME = "AI外贸独立国家域名站群_案例研究资料包.zip"
W, H = A4
MARGIN = 44.0
WIDTH = W - 2 * MARGIN
INK = colors.HexColor("#142F39")
TEAL = colors.HexColor("#087F84")
MINT = colors.HexColor("#E9F5F2")
PAPER = colors.HexColor("#FCFBF7")
MUTED = colors.HexColor("#577079")
LINE = colors.HexColor("#D8E3E3")
GOLD = colors.HexColor("#D7A64F")


@dataclass
class Case:
    name: str
    group: str
    industry: str
    kind: str
    urls: list[str]
    refs: list[str]
    seo: list[str]
    lesson: str
    boundary: str
    origins: list[str]
    code: str = ""


@dataclass
class Page:
    key: str
    eyebrow: str
    title: str
    body: str = ""
    cases: list[Case] | None = None
    mode: str = "text"


class LayoutEntry(TypedDict):
    page: int
    key: str
    title: str
    bottom: float
    body_scale: float


def read_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def unique(items: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(item.strip() for item in items if item.strip()))


def split_urls(value: str) -> list[str]:
    return unique(value.split(" | "))


def clean(text: str) -> str:
    substitutions = {
        "本轮": "原研究",
        "当前国家站结构": "国家站结构样本",
        "当前": "观察时",
        "实测": "抽样观察",
        "网页工具": "公开页面",
        "同日早轮": "此前",
        "同日跨行业报告中的代表域名": "公开国家站结构样本",
        "同日跨行业报告所核欧洲网络": "公开欧洲语言站网络",
        "同日跨行业报告所核产品词域名网络": "产品词域名组成的多语言网络",
        "，按市场见核验表": "，需跟随入口确认最终页面",
        "；按域名见核验表": "；需逐域确认最终页面",
        "，见核验表": "，需逐个入口核对",
        "–": "-",
        "—": "-",
        "公开公开页面": "公开页面",
    }
    for old, new in substitutions.items():
        text = text.replace(old, new)
    return text


def load_cases() -> list[Case]:
    aliases = {"Jongen Werkzeugtechnik": "Jongen", "XCMG": "徐工", "LiuGong": "柳工"}
    cases: dict[str, Case] = {}
    for row in read_csv("outputs/2026-11-12-multilingual-seo/案例总表.csv"):
        name = aliases.get(row["案例"], row["案例"])
        cases[name] = Case(
            name, "跨行业与架构参照", row["行业"], clean(row["证据类型"]),
            split_urls(row["样本域名"]), split_urls(row["品牌或运营证据"]),
            split_urls(row["SEO原文"]), clean(row["可核对的做法"]),
            clean(row["口径与边界"]), ["跨行业 41 组研究"],
        )
    for row in read_csv("outputs/2026-11-12-b2b-multilingual-seo/B2B案例总表.csv"):
        name = aliases.get(row["企业或项目"], row["企业或项目"])
        old = cases.get(name)
        cases[name] = Case(
            name, "工业与 B2B", row["行业与业务"], clean(row["证据类型"]),
            unique(split_urls(row["代表网址（A与B为当前国家站；C与D含对照）"]) + (old.urls if old else [])),
            unique(split_urls(row["运营来源"]) + (old.refs if old else [])),
            unique(split_urls(row["SEO项目或分析原文"]) + (old.seo if old else [])),
            old.lesson if old else clean(row["证据内容及边界"]),
            clean(row["证据内容及边界"]),
            (old.origins if old else []) + ["工业与 B2B 73 组研究"],
        )
    china_order: list[str] = []
    for row in read_csv("outputs/2026-11-12-china-b2b-country-networks/中国制造多语言站群案例总表.csv"):
        name = row["品牌"]
        old = cases.get(name)
        china_order.append(name)
        cases[name] = Case(
            name, "中国制造", row["行业"], "中国制造 / " + row["案例层级"],
            split_urls(row["代表网址（含结构对照）"]), split_urls(row["厂家或运营来源"]), [],
            clean(row["证据与边界"]), "含集团、区域与渠道入口；具体经营主体按市场分别判断。",
            (old.origins if old else []) + ["中国制造 21 组补充研究"],
        )
    main = [
        Case("三一重工 / SANY", "主案例", "工程机械与商用设备", "集团与业务网络",
             ["https://www.sanyglobal.com/", "https://www.sany.in/", "https://www.sanyeurope.com/"],
             ["https://www.sanygroup.com/", "https://www.sanyglobal.com/press_releases/1104/"], [],
             "sany.in 展示独立国家域名；其他入口提供集团与当地业务分工参考。", "25 个高置信集团及业务根域，含全球、区域与产品线，不能全部计作国家后缀。", ["三一专项研究"]),
        Case("PDT R US / Design Media Service", "主案例", "包装与印刷", "高置信运营关联",
             ["https://pdtrus.com/", "https://www.custompaperbagsco.co.uk/", "https://www.labelprintingco.co.uk/"],
             ["https://www.pdtrus.co.uk/contact/", "https://www.labelprintingco.co.uk/contact-us/"], [],
             "英国 .co.uk 与澳洲 .com.au 按国家和产品承接需求；联系能力存在集中复用线索。", "47 个核心根域含其他后缀；不等同法律所有权；没有确认该网络的小语种运营站。", ["包装专项研究与小语种复核"]),
    ]
    ordered = main + [cases.pop(name) for name in china_order]
    ordered += [case for case in cases.values() if case.group == "工业与 B2B"]
    ordered += [case for case in cases.values() if case.group != "工业与 B2B"]
    for case in ordered:
        if case.name == "Skyscanner":
            case.boundary = "当地正文由公开网页来源核实；结构样本与历史项目范围分别记录"
        elif case.name == "Hilti":
            case.boundary = "跨域共用产品类目编号；首页与分类页的版本声明需分别检查"
        elif case.name == "Mascus":
            case.lesson = "32 个地区域名、25 种语言；协调当地内容、技术与产品生命周期。"
            case.boundary = "欧洲项目：2018 下半年同比自然搜索会话 +21%、联系请求 +13.1%。"
        elif case.name == "Quick-Step":
            case.lesson = "六市场项目结合当地关键词、内容、内链与外部引用。"
            case.boundary = "优化内容页跨市场平均点击 +100.53%；原文标注项目 1 年，未明确比较起止日期。"
    assert len(ordered) == 125
    assert len({case.name for case in ordered}) == 125
    for index, case in enumerate(ordered, 1):
        case.code = f"C{index:03}"
    return ordered


def reading_role(case: Case) -> str:
    """Classify reading use from the researched evidence, never from suffix alone."""
    if case.group == "主案例":
        return "国家域名与业务分工"
    if "对照" in case.kind:
        return "架构对照"
    if case.group == "中国制造":
        return "中国制造与渠道"
    if "国家站" in case.kind:
        return "国家域名样本"
    if case.kind == "其他公开SEO项目":
        return "SEO 方法参照"
    return "跨行业参照"


def write_csv(path: Path, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def public_files(cases: list[Case]) -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    write_csv(PACK / "01_125组案例总表.csv",
              ["编号", "案例", "分组", "行业", "本册阅读用途", "证据类型", "可学习的结构或做法", "适用范围", "代表网址", "公开来源", "SEO项目原文", "资料观察日期"],
              [[c.code, c.name, c.group, c.industry, reading_role(c), c.kind, c.lesson, c.boundary,
                " | ".join(c.urls), " | ".join(c.refs), " | ".join(c.seo), "2026-11-05 至 2026-11-12"] for c in cases])
    sany = read_csv("outputs/2026-11-12-sany-global-network/三一全球站点与域名清单.csv")
    write_csv(PACK / "02_三一101对象分类表.csv",
              ["分类", "域名或子域", "市场或职责", "内容语言或状态", "代表网址", "公开运营证据", "归属与状态说明", "观察日期"],
              [[r[k] for k in ["分类", "域名或子域", "市场或职责", "内容语言或状态", "代表网址", "公开运营证据", "归属与状态说明"]] + ["2026-11-12"] for r in sany])
    packaging = read_csv("outputs/2026-11-05-site-network/全部核验对象总表.csv")
    write_csv(PACK / "03_包装60对象分类表.csv",
              ["域名", "分类", "计入核心", "公开页面状态", "公开来源", "适用范围", "证据日期"],
              [[r["域名"], r["分类"], r["计入当前核心"], r["当前状态"], r["主要来源"], r["限制"], r["核验日期"]] for r in packaging])
    (PACK / "先读我.txt").write_text(
        "AI 外贸独立国家域名站群｜125 组案例与方案解读\n版本：2026-11-14 案例研究版\n\n"
        "本包聚焦站群案例、业务启发，以及 AI 建站方案能做什么。\n\n"
        "PDF：代表案例图解、SEO 项目、两页方案能力说明、完整案例与域名清单。\n"
        "01_125组案例总表.csv：全部案例编号、行业、做法、网址和公开来源。\n"
        "02_三一101对象分类表.csv：集团业务、渠道、历史、跳转及待核对象。\n"
        "03_包装60对象分类表.csv：核心关联域名、历史、待核和排除对象。\n\n"
        "三一 25 个高置信集团与业务根域、包装 47 个核心关联根域，分别是完整研究对象中的已确认部分。请保留分类列，不能把全部对象算作官网。\n\n"
        "案例观察主要为 2026-11-05 至 2026-11-12，相关原理和方案说明于 11 月 13 至 14 日补核。网站和服务会变化，请结合来源日期阅读。\n"
        "图解是公开结构或业务关系的重绘。项目数字采用发布方披露范围，未取得完整后台经营数据。第三方案例不代表使用本册工具，也不构成排名或询盘保证。\n\n"
        "免费建站工具另行配发。\n",
        encoding="utf-8",
    )


def sany_pages() -> list[Page]:
    rows = [r for r in read_csv("outputs/2026-11-12-sany-global-network/三一全球站点与域名清单.csv") if r["分类"] == "集团与业务官网（高置信）"]
    assert len(rows) == 25
    result: list[Page] = []
    for i, subset in enumerate((rows[:13], rows[13:]), 1):
        body = "以下是集团及业务根域的完整清单，含国家后缀、区域 .com 与产品线入口。国家域名示例重点看 sany.in；25 个根域不能全部算作独立国家域名。观察日期为 2026 年 11 月 12 日。\n\n"
        body += "| 业务域名 | 市场与职责 | 页面语言样本 |\n| --- | --- | --- |\n"
        for row in subset:
            language = row["内容语言或状态"]
            if row["域名或子域"] == "sanyglobal.com":
                language = "12 语：含英、中、西、法、德等"
            body += f"| [{row['域名或子域']}]({row['代表网址']}) | {row['市场或职责']} | {language} |\n"
        body += "\n### 阅读提示\n\n每个根域代表一个观察入口，不代表全部产品、语言与功能已经验证。集团、上市主体与当地公司的关系，以公开公司说明为准。\n\n"
        body += "来源：[集团入口](https://www.sanygroup.com/) · [全球入口](https://www.sanyglobal.com/) · [全球站点地图](https://www.sanyglobal.com/sitemap/)\n"
        result.append(Page(f"sany_domains_{i}", "06 / 完整域名清单", f"三一：25 个集团与业务根域 · {i}/2", body))
    return result


def packaging_pages() -> list[Page]:
    path = ROOT / "outputs/2026-11-05-site-network/企业独立站站群深度研究报告.md"
    raw = path.read_text()
    start = raw.index("| 品牌／入口 |")
    end = raw.index("\n\n", start)
    lines = raw[start:end].replace("★ ", "").replace("，第二轮升级", "").replace("—", "未确认").splitlines()
    rows = lines[2:]
    assert len(rows) == 20
    result: list[Page] = []
    for i, subset in enumerate((rows[:10], rows[10:]), 1):
        body = "优先看英国 .co.uk 与澳洲 .com.au 两列，观察产品如何分配到国家域名。每行代表同一品牌或对应地区品牌；美国 / 全球列补全网络。“未确认”表示没有建立对应关系。\n\n"
        body += "\n".join(lines[:2] + subset)
        body += "\n\n### 从矩阵看分工\n\n"
        body += "前 10 行集中展示纸盒、纸袋、标签和贴纸等产品入口。" if i == 1 else "本页同时包含产品站与公司门户。美国吊牌使用 Hang Tags，英国和澳洲使用 Swing Tags。"
        body += "各市场有不同联系信息，体现了产品与市场入口之间的分工。\n\n"
        body += "> 两页合计 47 个核心根域。另有 1 个已确认历史关联对象，不计入核心。与这些站相似的欧洲语言站，需要单独核对经营关系。\n"
        result.append(Page(f"pack_matrix_{i}", "06 / 完整域名清单", f"包装：47 个核心根域 · {i}/2", body))
    return result


def load_pages(cases: list[Case]) -> list[Page]:
    raw = (WORK / "book.md").read_text()
    chunks = re.split(r"(<!-- (?:page|auto):.*?-->)", raw)
    pages = [Page("cover", "", "", mode="cover"), Page("contents", "阅读导航", "案例与方案阅读导航", mode="toc")]
    for index in range(1, len(chunks), 2):
        tag, body = chunks[index], chunks[index + 1].strip()
        if tag.startswith("<!-- page:"):
            match = re.fullmatch(r"<!-- page: (.*?) \| (.*?) \| (.*?) -->", tag)
            assert match is not None
            pages.append(Page(match[1], match[2], match[3], body))
        elif "sany_domains" in tag:
            pages += sany_pages()
        elif "packaging_matrix" in tag:
            pages += packaging_pages()
        elif "catalog" in tag:
            groups = ["中国制造", "工业与 B2B", "跨行业与架构参照"]
            for group_index, group in enumerate(groups, 1):
                group_cases = [case for case in cases[2:] if case.group == group]
                for offset in range(0, len(group_cases), 8):
                    pages.append(Page(f"catalog_{group_index}_{offset // 8}", "06 / 125 组案例索引", f"{group} · {offset // 8 + 1}/{math.ceil(len(group_cases) / 8)}", cases=group_cases[offset:offset + 8], mode="catalog"))
    return pages


def markdown_inline(value: str) -> str:
    links: list[str] = []

    def link(match: re.Match[str]) -> str:
        url = html.escape(match[2], quote=True)
        label = html.escape(match[1])
        links.append(f'<link href="{url}" color="#087F84">{label}</link>')
        return f"ZZLINK{len(links) - 1}ZZ"

    value = re.sub(r"\[([^\]]+)\]\(([^\s]+?)\)", link, value)
    value = html.escape(value)
    value = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", value)
    value = value.replace("`", "")
    for index, rendered in enumerate(links):
        value = value.replace(f"ZZLINK{index}ZZ", rendered)
    value = value.replace("→", '<font name="Symbols">→</font>')
    return value


def style(size: float = 11.5, leading: float | None = None, color: colors.Color = INK, bold: bool = False) -> ParagraphStyle:
    return ParagraphStyle(
        "p", fontName="CNB" if bold else "CN", fontSize=size, leading=leading or size * 1.65,
        textColor=color, wordWrap="CJK", splitLongWords=True, alignment=TA_LEFT,
        spaceAfter=0, allowWidows=0, allowOrphans=0,
    )


def p(text: str, size: float = 11.5, leading: float | None = None, color: colors.Color = INK, bold: bool = False) -> Paragraph:
    return Paragraph(markdown_inline(text), style(size, leading=leading, color=color, bold=bold))


def table_flow(lines: list[str], width: float, scale: float) -> Table:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    rows = [rows[0]] + rows[2:]
    count = len(rows[0])
    if count == 4:
        ratios = [0.18, 0.273, 0.273, 0.274]
    elif count == 3:
        if "业务域名" in rows[0][0]:
            ratios = [0.40, 0.27, 0.33]
        else:
            ratios = [0.20, 0.42, 0.38]
    elif count == 2 and rows[0][0] == "术语":
        ratios = [0.30, 0.70]
    else:
        ratios = [1 / count] * count
    size = 10.3 * scale
    if count == 4 and "品牌" in rows[0][0]:
        size = 8.7 * scale
    cells: list[list[Paragraph]] = []
    for index, row in enumerate(rows):
        paragraphs: list[Paragraph] = []
        for column, cell in enumerate(row):
            cell_style = style(size, leading=size * 1.55, color=colors.white if index == 0 else INK, bold=index == 0)
            rendered = markdown_inline(cell)
            if index > 0 and column == 0 and rows[0][0] == "检查项":
                rendered = rendered.replace(" canonical", "<br/>canonical").replace(" hreflang", "<br/>hreflang")
            if count == 4 and "品牌" in rows[0][0] and index > 0:
                if column == 0 and not re.search(r"[\u4e00-\u9fff]", cell):
                    cell_style.wordWrap = "LTR"
                elif column > 0:
                    match = re.fullmatch(r"\[([^\]]+)\]\(([^\s]+?)\)", cell)
                    if match and len(match[1]) >= 26:
                        host = match[1]
                        suffix = next((s for s in (".co.uk", ".com.au", ".com") if host.endswith(s)), "")
                        if suffix:
                            label = html.escape(host[:-len(suffix)]) + "<br/>" + html.escape(suffix)
                            rendered = f'<link href="{html.escape(match[2], quote=True)}" color="#087F84">{label}</link>'
            paragraphs.append(Paragraph(rendered, cell_style))
        cells.append(paragraphs)
    table = Table(cells, colWidths=[width * ratio for ratio in ratios], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6F5")]),
        ("LINEBELOW", (0, 0), (-1, 0), 1, TEAL),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8 * scale),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8 * scale),
    ]))
    return table



def flows(body: str, width: float, scale: float = 1.0) -> list[Flowable]:
    lines = body.strip().splitlines()
    result: list[Flowable] = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("|"):
            table_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            result.extend([table_flow(table_lines, width, scale), Spacer(1, 13 * scale)])
            continue
        if line.startswith("[diagram:"):
            result.extend([Diagram(line[9:-1], width), Spacer(1, 7)])
        elif line.startswith("### "):
            result.extend([Spacer(1, 6 * scale), p(line[4:], 13 * scale, bold=True), Spacer(1, 6 * scale)])
        elif line.startswith("> "):
            para = p(line[2:], 10.3 * scale, leading=16 * scale, color=INK)
            callout = Table([[para]], colWidths=[width])
            callout.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), MINT),
                ("LINEBEFORE", (0, 0), (0, -1), 3, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]))
            result.extend([callout, Spacer(1, 12 * scale)])
        elif line.startswith("来源：") or line.startswith("查看：") or line.startswith("网站："):
            result.extend([p(line, 9.1 * scale, leading=14 * scale, color=MUTED), Spacer(1, 11 * scale)])
        else:
            if line.startswith("- "):
                line = "• " + line[2:]
            result.extend([p(line, 11.5 * scale), Spacer(1, 10 * scale)])
        index += 1
    if result and isinstance(result[-1], Spacer):
        result.pop()
    return result


def total_height(items: Sequence[Flowable], width: float) -> float:
    return sum(item.wrap(width, 1000)[1] for item in items)


def draw_items(c: Canvas, items: Sequence[Flowable], x: float, y: float, width: float) -> float:
    for item in items:
        _, height = item.wrap(width, 1000)
        y -= height
        item.drawOn(c, x, y)
    return y


def chrome(c: Canvas, number: int, total: int, eyebrow: str) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(0, H - 7, W, 7, stroke=0, fill=1)
    c.setFillColor(MUTED)
    c.setFont("CN", 8.5)
    c.drawString(MARGIN, H - 35, "AI 外贸独立国家域名站群")
    c.drawRightString(W - MARGIN, H - 35, "案例研究与方案解读 / 2026.11")
    c.setStrokeColor(LINE)
    c.line(MARGIN, 40, W - MARGIN, 40)
    c.setFont("CN", 8)
    c.drawString(MARGIN, 26, eyebrow)
    c.drawRightString(W - MARGIN, 26, f"{number:02} / {total:02}")


def title_block(c: Canvas, page: Page) -> float:
    c.setFillColor(TEAL)
    c.setFont("CNB", 10)
    c.drawString(MARGIN, H - 66, page.eyebrow)
    title = p(page.title, 22, leading=30, bold=True)
    _, height = title.wrap(WIDTH, 100)
    title.drawOn(c, MARGIN, H - 82 - height)
    return H - 103 - height


def cover(c: Canvas, total: int) -> None:
    c.setFillColor(INK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(0, H - 18, W, 18, stroke=0, fill=1)
    c.setFont("CN", 10)
    c.setFillColor(colors.HexColor("#A7D9D5"))
    c.drawString(47, H - 65, "CASE STUDIES  /  2026.11")
    c.setFont("CNB", 36)
    c.setFillColor(colors.white)
    c.drawString(44, H - 139, "AI 外贸")
    c.drawString(44, H - 191, "独立国家域名站群")
    c.setFillColor(GOLD)
    c.setFont("CNB", 19)
    c.drawString(46, H - 238, "125 组案例与 AI 建站方案解读")
    summary = Paragraph("从三一、包装与工业 B2B，理解多国家网站的业务价值。<br/>看真实案例，再了解 AI 建站方案能帮你做什么。", style(12.5, leading=22, color=colors.HexColor("#D8E8E9")))
    summary.wrap(430, 100)
    summary.drawOn(c, 47, H - 312)
    # A conceptual network, not a geographic map or a claim about case ownership.
    cx, cy = 297.5, 330
    c.setStrokeColor(colors.HexColor("#26515B"))
    for radius in [92, 145, 197]:
        c.circle(cx, cy, radius, stroke=1, fill=0)
    points = [(135, 400, ".de", "德国 / 德语"), (450, 418, ".fr", "法国 / 法语"), (123, 246, ".co.uk", "英国 / 英语"), (460, 242, ".pl", "波兰 / 波兰语")]
    for x, y, code, label in points:
        c.setStrokeColor(colors.HexColor("#4B8F95"))
        c.line(cx, cy, x, y)
        c.setFillColor(colors.HexColor("#204650"))
        c.roundRect(x - 44, y - 27, 88, 54, 10, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("CNB", 15)
        c.drawCentredString(x, y + 4, code)
        c.setFont("CN", 9)
        c.setFillColor(colors.HexColor("#AFD8D7"))
        c.drawCentredString(x, y - 14, label)
    c.setFillColor(TEAL)
    c.roundRect(cx - 82, cy - 39, 164, 78, 12, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("CNB", 17)
    c.drawCentredString(cx, cy + 6, "产品 × 国家")
    c.setFont("CN", 10)
    c.drawCentredString(cx, cy - 17, "当地内容 · 产品展示 · 询盘入口")
    c.setFillColor(colors.HexColor("#9CBDC2"))
    c.setFont("CN", 8)
    c.drawCentredString(cx, 118, "方案示意 / 目标市场和域名按实际业务选择")
    c.setFillColor(GOLD)
    c.rect(46, 86, 41, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("CN", 10)
    c.drawString(46, 63, f"{len(FIGURES)} 幅图解  /  125 组案例  /  三一与包装完整域名清单  /  {total} 页")
    c.setFillColor(colors.HexColor("#9CBDC2"))
    c.setFont("CN", 8)
    c.drawString(46, 42, "案例研究版 / 2026-11-14 / 外贸工厂、SOHO 与外贸公司")


def toc(c: Canvas, pages: list[Page]) -> None:
    page = pages[1]
    y = title_block(c, page)
    intro = p("先理解国家站的业务价值，再看代表案例与完整清单。AI 建站方案集中在第 04 部分，用两页说明能力和适用需求。", 11.8)
    _, height = intro.wrap(WIDTH, 100)
    intro.drawOn(c, MARGIN, y - height)
    y -= height + 28
    entries = [
        ("01", "国家站的业务价值", "buyer_journey", "买家需求 / 当地语言 / 国家域名"),
        ("02", "代表案例拆解", "case_map", "125 组案例导航 / 欧洲包装 / 中国制造 / 工业产品"),
        ("03", "多站背后的业务分工", "sany", "三一 / 包装网络 / SEO 项目结果 / 国际团队"),
        ("04", "我们的 AI 建站方案", "solution_capabilities", "方案能做什么 / WordPress 与免费静态方案"),
        ("05", "案例补充说明", "architectures", "不同网址结构 / 21 组中国制造案例"),
        ("06", "完整域名清单与 125 组索引", "sany_domains_1", "三一 25 域 / 包装 47 域 / 按行业查阅全部案例"),
        ("07", "资料说明", "methods", "统计范围 / 公开来源 / 三张配套研究表"),
    ]
    mapping = {item.key: index + 1 for index, item in enumerate(pages)}
    for number, title, key, sub in entries:
        c.setFillColor(TEAL)
        c.setFont("CNB", 15)
        c.drawString(MARGIN, y - 15, number)
        c.setFillColor(INK)
        c.setFont("CNB", 12)
        c.drawString(MARGIN + 35, y - 13, title)
        c.setFont("CN", 8.8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 35, y - 30, sub)
        c.setFillColor(TEAL)
        c.setFont("CNB", 12)
        c.drawRightString(W - MARGIN, y - 17, f"{mapping[key]:02}")
        c.linkRect("", key, (MARGIN, y - 41, W - MARGIN, y + 2), relative=0, thickness=0)
        c.setStrokeColor(LINE)
        c.line(MARGIN + 35, y - 42, W - MARGIN, y - 42)
        y -= 67
    assert y > 60


def catalog(c: Canvas, page: Page) -> float:
    top = title_block(c, page)
    note = p("按编号可在随包案例表里找到完整网址与来源。标签说明阅读用途；中国制造案例包含集团、区域与渠道入口，请结合具体网址判断。", 9.2, leading=14, color=MUTED)
    _, nh = note.wrap(WIDTH, 100)
    note.drawOn(c, MARGIN, top - nh)
    top -= nh + 15
    gap = 14.0
    card_width = (WIDTH - gap) / 2
    card_height = (top - 61 - 3 * 12) / 4
    assert page.cases is not None
    min_y = H
    for index, case in enumerate(page.cases):
        x = MARGIN + (index % 2) * (card_width + gap)
        y = top - (index // 2) * (card_height + 12)
        c.setFillColor(colors.white)
        c.setStrokeColor(LINE)
        c.roundRect(x, y - card_height, card_width, card_height, 6, stroke=1, fill=1)
        inner = card_width - 22
        heading = p(f"{case.code}  {case.name}", 10.8, leading=14.3, bold=True)
        _, hh = heading.wrap(inner, 100)
        heading.drawOn(c, x + 11, y - 10 - hh)
        yy = y - 10 - hh - 4
        meta = p(reading_role(case) + " · " + case.industry, 8.1, leading=11, color=MUTED)
        _, mh = meta.wrap(inner, 100)
        meta.drawOn(c, x + 11, yy - mh)
        yy -= mh + 4
        if case.group == "中国制造":
            observation = case.lesson
        elif case.lesson == case.boundary:
            observation = case.boundary
        else:
            observation = case.lesson + "；" + case.boundary
        if case.seo and re.search(r"[+＋]\s*\d|增长|4000|61000", observation):
            observation = "项目披露：" + observation
        # Store the complete description in the public CSV; the card is a reading index.
        if len(observation) > 125:
            observation = case.boundary if len(case.boundary) >= 30 else case.lesson
        desc = p(observation, 9.2, leading=13.3)
        _, dh = desc.wrap(inner, 180)
        desc.drawOn(c, x + 11, yy - dh)
        yy -= dh + 6
        urls = case.urls[:3]
        domains = []
        for url in urls:
            host = urlsplit(url).netloc.removeprefix("www.")
            path = urlsplit(url).path
            label = host + (path if 0 < len(path) <= 8 and path != "/" else "")
            domains.append(f"[{label}]({url})")
        samples = p(" · ".join(domains), 8.0, leading=11.3)
        _, sh = samples.wrap(inner, 100)
        samples.drawOn(c, x + 11, yy - sh)
        yy -= sh + 5
        sources = []
        if case.refs:
            sources.append(f"[公开来源]({case.refs[0]})")
        if case.seo:
            sources.append(f"[项目原文]({case.seo[0]})")
        source = p(" / ".join(sources), 8.0, leading=11, color=MUTED)
        _, rh = source.wrap(inner, 50)
        source.drawOn(c, x + 11, yy - rh)
        yy -= rh
        if yy < y - card_height + 8:
            raise ValueError(f"Catalog overflow {case.name}: {yy} < {y - card_height + 8}")
        min_y = min(min_y, y - card_height)
    return min_y


def create_pdf(pages: list[Page]) -> list[LayoutEntry]:
    FINAL.mkdir(parents=True, exist_ok=True)
    TEMP.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont("CN", "/Library/Fonts/OPPOSans R.ttf"))
    pdfmetrics.registerFont(TTFont("CNB", "/Library/Fonts/OPPOSans H.ttf"))
    pdfmetrics.registerFont(TTFont("Symbols", "/Library/Fonts/Arial.ttf"))
    pdfmetrics.registerFontFamily("CN", normal="CN", bold="CNB", italic="CN", boldItalic="CNB")
    c = Canvas(str(FINAL / PDF_NAME), pagesize=A4, pageCompression=1)
    c.setTitle("AI 外贸独立国家域名站群｜125 组案例与方案解读")
    c.setAuthor("外贸国家站案例研究")
    c.setSubject("125 组公开案例、国家域名、当地语言业务与 AI 建站方案能力")
    c.setKeywords("外贸,独立国家域名,WordPress,Builder Harness,Codex,静态站,三一,包装,AI建站,SEO")
    c.setViewerPreference("DisplayDocTitle", "true")
    c.showOutline()
    audit: list[LayoutEntry] = []
    for index, page in enumerate(pages, 1):
        c.bookmarkPage(page.key)
        c.addOutlineEntry(page.title or "封面", page.key, level=0, closed=False)
        if page.mode == "cover":
            cover(c, len(pages))
            bottom, scale = 42.0, 1.0
        else:
            chrome(c, index, len(pages), page.eyebrow)
            if page.mode == "toc":
                toc(c, pages)
                bottom, scale = 68.0, 1.0
            elif page.mode == "catalog":
                bottom, scale = catalog(c, page), 1.0
            else:
                top = title_block(c, page)
                scale = 1.0
                items = flows(page.body, WIDTH, scale)
                while total_height(items, WIDTH) > top - 62 and scale > 0.91:
                    scale = round(scale - 0.025, 3)
                    items = flows(page.body, WIDTH, scale)
                if total_height(items, WIDTH) > top - 62:
                    raise ValueError(f"Page overflow {page.key}: {total_height(items, WIDTH):.1f} > {top - 62:.1f}")
                bottom = draw_items(c, items, MARGIN, top, WIDTH)
        audit.append({"page": index, "key": page.key, "title": page.title, "bottom": round(bottom, 2), "body_scale": scale})
        c.showPage()
    c.save()
    (WORK / "layout-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2))
    return audit


def editable_master(pages: list[Page]) -> None:
    parts = ["# AI 外贸独立国家域名站群\n\n125 组案例与方案解读\n\n独立国家域名 · 当地语言业务 · AI 建站方案能力\n\n版本：2026-11-14 案例研究版\n"]
    for page in pages:
        if page.mode in {"cover", "toc"}:
            continue
        parts.append(f"\n\n## {page.title}\n\n")
        if page.cases:
            for case in page.cases:
                parts.append(f"### {case.code} {case.name}\n\n{case.industry}｜{reading_role(case)}｜{case.kind}\n\n{case.lesson}\n\n范围：{case.boundary}\n\n")
                parts.append("样本：" + " · ".join(f"[{urlsplit(u).netloc}]({u})" for u in case.urls) + "\n\n")
                parts.append("来源：" + " · ".join(f"[公开来源 {i}]({u})" for i, u in enumerate(case.refs + case.seo, 1)) + "\n")
        else:
            body = page.body
            for key, figure in FIGURES.items():
                body = body.replace(f"[diagram:{key}]", f"**{figure.label}**\n\n{figure.description}\n\n{figure.caption}")
            parts.append(body)
    (WORK / "可编辑完整正文.md").write_text("\n".join(parts), encoding="utf-8")


def package() -> None:
    shutil.copy2(FINAL / PDF_NAME, PACK / PDF_NAME)
    target = FINAL / ZIP_NAME
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACK.iterdir()):
            if path.is_file():
                archive.write(path, path.name)


def main() -> None:
    cases = load_cases()
    public_files(cases)
    pages = load_pages(cases)
    audit = create_pdf(pages)
    editable_master(pages)
    package()
    print(json.dumps({"pdf": str(FINAL / PDF_NAME), "pages": len(pages), "cases": len(cases), "min_text_bottom": min(float(row["bottom"]) for row in audit[2:]), "zip": str(FINAL / ZIP_NAME)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
