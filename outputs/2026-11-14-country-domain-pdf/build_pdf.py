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


ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
FINAL = ROOT / "output" / "pdf"
PACK = WORK / "领取资料包"
TEMP = ROOT / "tmp" / "pdfs" / "country-domain-1114"
PDF_NAME = "AI外贸独立国家域名站群_125组案例与首站实操手册.pdf"
ZIP_NAME = "AI外贸独立国家域名站群_案例与实操资料包.zip"
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
    if case.group == "中国制造" or "国家站" in case.kind:
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
    fields = ["目标国家", "目标语言", "采购人群", "主力产品线", "实际需求线索", "可交付地区", "报价与样品条件", "候选国家域名", "域名注册资格与可用性", "域名续费与负责人", "国家站部署项目", "收件邮箱", "回复负责人", "公司资料位置", "产品主表位置", "术语与语言审核人", "按域统计与Search Console资源", "工具与托管预算", "待补资料", "计划检查日期", "首站验收结果"]
    write_csv(PACK / "04_首站启动表.csv", ["项目", "填写内容", "负责人", "状态"], [[field, "", "", "待填写"] for field in fields])
    write_csv(PACK / "05_产品与语言对应表.csv", ["内部产品编号", "产品名称", "型号", "规格版本", "参数与单位", "图片文件", "技术附件", "国家", "国家域名", "语言", "分类URL", "产品URL", "对应国家产品URL", "术语版本", "市场差异", "审核人", "批准日期", "发布版本", "待确认项"], [[""] * 19 for _ in range(10)])
    write_csv(PACK / "06_竞品观察表.csv", ["品牌", "行业", "国家", "语言", "国家域名", "官方目录URL", "入口URL", "最终URL", "深页是否保留国家域名", "产品或系列", "页面结构", "交付服务", "销售主体", "询价入口", "观察到的事实", "待核推断", "我想采用的做法", "观察日期"], [[""] * 18 for _ in range(10)])
    write_csv(PACK / "07_维护记录表.csv", ["日期", "资料版本", "产品编号", "变更原因", "受影响国家", "国家域名", "部署项目", "页面URL", "修改字段", "预览版本", "审核人", "发布版本", "检查结果", "恢复版本", "用时分钟", "待处理事项"], [[""] * 16 for _ in range(10)])
    write_csv(PACK / "08_询盘观察表.csv", ["提交时间", "域名", "页面URL", "产品编号", "语言", "目标国家", "来源渠道", "是否测试", "是否重复", "销售负责人", "有效性判断", "是否回复", "报价或样品进展", "下一步", "备注"], [[""] * 15 for _ in range(10)])
    text = (WORK / "book.md").read_text()
    prompts = re.search(r"<!-- page: prompts_1.*?(?=<!-- page: action)", text, re.S)
    assert prompts is not None
    (PACK / "09_5组AI任务模板.md").write_text("# AI 外贸独立国家域名站群：5 组任务模板\n\n" + re.sub(r"<!--.*?-->\n", "", prompts.group(), flags=re.S), encoding="utf-8")
    domain_fields = ["国家", "主语言", "国家域名", "注册主体", "注册商", "注册资格核对", "到期日", "续费负责人", "Cloudflare项目", "正式主网址", "主力产品线", "收件邮箱", "回复负责人", "Search Console资源", "统计来源标识", "产品主表版本", "发布版本", "实际收件验证日期", "恢复版本", "备注"]
    write_csv(PACK / "10_国家域名与发布配置表.csv", domain_fields, [[""] * len(domain_fields) for _ in range(10)])
    (PACK / "先读我.txt").write_text(
        "AI 外贸独立国家域名站群｜案例与实操资料包\n版本：2026-11-14\n\n"
        "主方案：独立国家域名 + 当地语言内容 + AI 集中维护。先完成一国，再扩展下一国。\n\n"
        "1. 先读 PDF 的主推方案和国家域名案例，再看三一与包装的业务分工。蓝色链接可以打开，书签用于跳转。\n"
        "2. 01 至 03 是案例查阅表。三一与包装的对象分类请保留，待核、历史和排除项不能算作已确认官网。\n"
        "3. 04 至 08 与 10 是可填写模板；10 用于逐国记录域名、部署、收件与资产负责人。请另存副本后填写。\n"
        "4. 09 是可复制的 AI 任务模板。建站 Skill 请使用视频配发的对应安装包与说明；本包不包含 Skill 软件。\n"
        "5. 125 组包含国家域名样本、SEO 方法、其他架构与跨行业参照。用途列不是整组域名的运营状态判定；请结合具体样本与证据阅读。\n\n"
        "案例观察主要为 2026-11-05 至 2026-11-12，平台说明于 2026-11-13 补核，域名与语言版本说明于 11 月 14 日补核。"
        "公开网站与套餐会变化，采用具体做法前请核对链接和账户规则。\n"
        "本包提供结构案例、项目引用与实施建议；不将案例网站认定为本次 Skill 所建，不提供排名或询盘数量保证。\n",
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
        result.append(Page(f"sany_domains_{i}", "07 / 完整域名清单", f"三一：25 个集团与业务根域 · {i}/2", body))
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
        body += "各市场有不同联系信息；把不同入口识别清楚，才能设计自己的内容与询盘来源表。\n\n"
        body += "> 两页合计 47 个核心根域。另有 1 个已确认历史关联对象，不计入核心。与这些站相似的欧洲语言站，需要单独核对经营关系。\n"
        result.append(Page(f"pack_matrix_{i}", "07 / 完整域名清单", f"包装：47 个核心根域 · {i}/2", body))
    return result


def load_pages(cases: list[Case]) -> list[Page]:
    raw = (WORK / "book.md").read_text()
    chunks = re.split(r"(<!-- (?:page|auto):.*?-->)", raw)
    pages = [Page("cover", "", "", mode="cover"), Page("contents", "阅读导航", "这份手册，怎样帮你落地", mode="toc")]
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
                    pages.append(Page(f"catalog_{group_index}_{offset // 8}", "07 / 125 组案例索引", f"{group} · {offset // 8 + 1}/{math.ceil(len(group_cases) / 8)}", cases=group_cases[offset:offset + 8], mode="catalog"))
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


class Diagram(Flowable):
    def __init__(self, kind: str, width: float) -> None:
        super().__init__()
        self.kind = kind
        self.width = width
        self.height = 170.0 if kind in {"sany", "country"} else 145.0

    def draw(self) -> None:
        c = self.canv
        w = self.width

        def box(x: float, y: float, width: float, height: float, title: str, sub: str, dark: bool = False) -> None:
            c.setFillColor(INK if dark else MINT)
            c.roundRect(x, y, width, height, 8, fill=1, stroke=0)
            first = p(title, 11.5, bold=True, color=colors.white if dark else INK)
            _, ph = first.wrap(width - 20, 100)
            first.drawOn(c, x + 10, y + height - ph - 8)
            second = p(sub, 8.5, leading=12, color=colors.HexColor("#CDE4E3") if dark else MUTED)
            _, sh = second.wrap(width - 20, 100)
            second.drawOn(c, x + 10, y + 8)

        c.setStrokeColor(TEAL)
        c.setLineWidth(1.3)
        if self.kind == "country":
            box(w / 2 - 114, 112, 228, 52, "产品资料 + AI 集中维护", "共用事实、术语、组件和更新记录", True)
            gap = 10
            col = (w - gap * 2) / 3
            for index, (title, sub) in enumerate([
                ("德国 .de", "德语内容 / 德国询盘"), ("法国 .fr", "法语内容 / 法国询盘"), ("波兰 .pl", "波兰语内容 / 波兰询盘"),
            ]):
                center = index * (col + gap) + col / 2
                c.line(w / 2, 112, center, 83)
                box(index * (col + gap), 23, col, 60, title, sub)
            c.setFillColor(MUTED)
            c.setFont("CN", 8.5)
            c.drawString(0, 4, "规划示意：各国家域名承载本国页面，分别发布和记录来源。")
        elif self.kind == "sany":
            box(w / 2 - 114, 111, 228, 53, "全球品牌与产品主站", "sanyglobal.com / 同域 12 种语言", True)
            for x in [w / 6, w / 2, w * 5 / 6]:
                c.line(w / 2, 111, x, 80)
            gap = 10
            col = (w - gap * 2) / 3
            for index, (title, sub) in enumerate([
                ("区域业务站", "印度 / 欧洲 / 法国等"), ("产品线入口", "挖掘机 / 重卡 / 混凝土"), ("本地渠道", "经销商 / 当地销售与服务"),
            ]):
                box(index * (col + gap), 20, col, 60, title, sub)
        elif self.kind == "packaging":
            labels = [("产品与市场入口", "纸盒 / 标签 / 纸袋"), ("统一联系能力", "表单映射 / 客服配置"), ("保留来源信息", "域名 / 页面 / 国家")]
            col = (w - 30) / 3
            for index, (title, sub) in enumerate(labels):
                if index < 2:
                    c.line(index * (col + 15) + col, 78, (index + 1) * (col + 15), 78)
                box(index * (col + 15), 43, col, 70, title, sub, index == 1)
            c.setFillColor(MUTED)
            c.setFont("CN", 9)
            c.drawString(0, 16, "前两项为公开观察；来源记录与分配方式需在自己的项目中实施。")
        else:
            labels = [("AI + Skill", "共用资料 → 国家内容"), ("国家域名 + 发布", "Cloudflare / 独立项目"), ("Resend → 邮箱", "逐域来源 / 可回复")]
            col = (w - 30) / 3
            for index, (title, sub) in enumerate(labels):
                if index < 2:
                    c.line(index * (col + 15) + col, 78, (index + 1) * (col + 15), 78)
                box(index * (col + 15), 43, col, 70, title, sub, index == 1)
            c.setFillColor(MUTED)
            c.setFont("CN", 9)
            c.drawString(0, 16, "可选即时聊天：Tidio；业务员仍负责回复、报价与跟进。")


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
    c.drawRightString(W - MARGIN, H - 35, "案例与首站实操 / 2026.11")
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
    c.drawString(47, H - 65, "FIELD GUIDE  /  2026.11")
    c.setFont("CNB", 36)
    c.setFillColor(colors.white)
    c.drawString(44, H - 139, "AI 外贸")
    c.drawString(44, H - 191, "独立国家域名站群")
    c.setFillColor(GOLD)
    c.setFont("CNB", 19)
    c.drawString(46, H - 238, "125 组案例与首站实操手册")
    summary = Paragraph("独立国家域名 + 当地语言内容 + AI 集中维护。<br/>看懂制造与包装案例，先完成一国，再扩展下一国。", style(12.5, leading=22, color=colors.HexColor("#D8E8E9")))
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
    c.roundRect(cx - 72, cy - 39, 144, 78, 12, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("CNB", 17)
    c.drawCentredString(cx, cy + 6, "一套产品资料")
    c.setFont("CN", 10)
    c.drawCentredString(cx, cy - 17, "AI 集中维护 · 各国独立发布")
    c.setFillColor(colors.HexColor("#9CBDC2"))
    c.setFont("CN", 8)
    c.drawCentredString(cx, 118, "方案示意 / 目标市场和域名按实际业务选择")
    c.setFillColor(GOLD)
    c.rect(46, 86, 41, 3, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("CN", 10)
    c.drawString(46, 63, f"真实案例索引  /  可复制任务模板  /  {total} 页行动资料")
    c.setFillColor(colors.HexColor("#9CBDC2"))
    c.setFont("CN", 8)
    c.drawString(46, 42, "国家域名方案版 2026-11-14 · 面向外贸工厂、小团队与 SOHO")


def toc(c: Canvas, pages: list[Page]) -> None:
    page = pages[1]
    y = title_block(c, page)
    intro = p("本册围绕独立国家域名展开：先看一国一域的方案与真实案例，再完成自己的首站。其他架构放入补充参照，完整研究清单保留在附录。", 11.8)
    _, height = intro.wrap(WIDTH, 100)
    intro.drawOn(c, MARGIN, y - height)
    y -= height + 28
    entries = [
        ("01", "主推方案：一国一域", "mainplan", "国家域名 / 当地内容 / AI 维护 / 首站选择"),
        ("02", "独立国家域名的真实案例", "packaging_europe", "欧洲包装 / 中国制造 / 工业产品多国对照"),
        ("03", "三一与包装网络的业务分工", "sany", "印度国家站 / 英澳国家域名 / 跨站资料与联系"),
        ("04", "把首个国家域名站做出来", "static", "独立发布 / 域名管理 / 内容 / 收件 / 统计"),
        ("05", "5 组任务模板与首站行动表", "prompts_1", "一国一域提示词 / 七步启动 / WordPress 路线"),
        ("06", "补充参照：架构与运营方法", "architectures", "辨认目录、子域与迁移 / SEO 项目 / 维护分工"),
        ("07", "完整域名清单与 125 组索引", "sany_domains_1", "三一 25 域 / 包装 47 域 / 全案例按用途查阅"),
        ("08", "研究方法、来源与随包工具", "methods", "统计口径 / 官方文档 / 国家域名与发布配置表"),
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
        y -= 61
    assert y > 60


def catalog(c: Canvas, page: Page) -> float:
    top = title_block(c, page)
    note = p("编号与随包案例表一致。“国家域名样本”指该组的相应入口；SEO 方法、其他架构和跨行业案例分别标注。具体网址状态与证据范围请结合 CSV 查阅。", 9.2, leading=14, color=MUTED)
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
    c.setTitle("AI 外贸独立国家域名站群｜125 组案例与首站实操手册")
    c.setAuthor("外贸国家站案例研究")
    c.setSubject("独立国家域名、当地语言内容、AI 集中维护与首站实操")
    c.setKeywords("外贸,独立国家域名,多语言,一国一域,三一,包装,AI建站,案例,SEO")
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
    parts = ["# AI 外贸独立国家域名站群\n\n125 组案例与首站实操手册\n\n独立国家域名 + 当地语言内容 + AI 集中维护\n\n版本：2026-11-14\n"]
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
            body = body.replace("[diagram:country]", "产品资料 + AI 集中维护 → 德国 .de / 法国 .fr / 波兰 .pl；当地内容、独立发布、按域统计")
            body = body.replace("[diagram:sany]", "全球主站 → 区域业务站 / 产品线入口 / 本地渠道")
            body = body.replace("[diagram:packaging]", "产品与市场入口 → 统一联系能力 → 自己项目中的来源记录")
            body = body.replace("[diagram:static]", "AI + Skill → 国家内容 → Cloudflare 独立项目与国家域名 → Resend → 带域名来源的询盘邮件；Tidio 为可选聊天入口")
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
