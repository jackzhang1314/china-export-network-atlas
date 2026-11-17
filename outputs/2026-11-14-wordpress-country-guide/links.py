"""Collect public site addresses without promoting candidates to confirmed sites."""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Sequence
from urllib.parse import urlsplit

if TYPE_CHECKING:
    from build_pdf import Case


ROOT = Path(__file__).resolve().parents[2]
ALIASES = {
    "Jongen Werkzeugtechnik": "Jongen", "XCMG": "徐工", "LiuGong": "柳工",
    "SANY": "三一重工 / SANY",
    "福田": "福田汽车", "上汽大通": "上汽大通 MAXUS", "杭叉": "杭叉集团",
    "宇通": "宇通客车", "海天": "海天国际", "雷沃": "潍柴雷沃",
    "正泰": "正泰与旗下 NOARK", "诺雅克": "正泰与旗下 NOARK",
    "陕汽": "陕汽 SHACMAN", "汇川": "汇川技术",
}


@dataclass
class SiteLink:
    code: str
    case: str
    url: str
    category: str
    observation: str
    origin: str


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / "outputs" / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def public_url(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if not value.startswith(("http://", "https://")):
        if not re.fullmatch(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?", value):
            return ""
        value = "https://" + value.rstrip("/") + "/"
    parts = urlsplit(value)
    return value if parts.hostname and not re.search(r"\s", value) else ""


def category(observation: str) -> str:
    if any(word in observation for word in ("排除", "不符", "停放", "出售", "停用", "占位")):
        return "排除或停用记录"
    if any(word in observation for word in ("历史", "旧入口")):
        return "历史记录"
    if any(word in observation for word in ("跨域", "跨主机", "转往", "跳转")):
        return "跳转记录"
    if any(word in observation for word in ("另见公开网页取证", "另取得", "另有公开结果", "直接取得品牌页面", "同域页面返回", "同主机有可读标题", "网页工具取得公开页面")):
        return "补充页面记录"
    if any(word in observation for word in ("未确认", "未取得", "待核", "待补", "候选", "验证", "拦截", "受限", "未纳入", "不计入")):
        return "待核或访问受限"
    return "补充页面记录"


def collect_links(cases: Sequence[Case]) -> list[SiteLink]:
    """Preserve addresses and their evidence status for the 125 selected cases."""
    by_name = {case.name: case for case in cases}
    links: dict[tuple[str, str], SiteLink] = {}

    def resolve(name: str) -> str:
        if name in by_name:
            return name
        if name in ALIASES:
            return ALIASES[name]
        first = name.split(" / ")[0]
        return ALIASES.get(first, first)

    def add(name: str, value: str, kind: str, observation: str, origin: str) -> None:
        name, url = resolve(name), public_url(value)
        if name not in by_name or not url:
            return
        key = (name, url)
        if key not in links:
            links[key] = SiteLink(by_name[name].code, name, url, kind, observation, origin)
        else:
            old = links[key]
            if origin not in old.origin.split("；"):
                old.origin += "；" + origin
            if observation and observation not in old.observation.split("；"):
                old.observation += "；" + observation
            # A directory listing must not hide a subsequently recorded exclusion.
            if kind == "排除或停用记录":
                old.category = kind
            elif kind == "跳转记录" and old.category != "排除或停用记录":
                old.category = kind
            elif kind == "补充页面记录" and old.category == "待核或访问受限":
                old.category = kind

    for case in cases:
        for url in case.urls:
            add(case.name, url, "案例总表网址", case.boundary, "案例总表")

    for row in rows("2026-11-12-multilingual-seo/域名核验表.csv"):
        note = row["访问结论"]
        add(row["案例"], row["直接请求"] or row["候选域名"], category(note), note, "跨行业逐域核验表")

    for row in rows("2026-11-12-b2b-multilingual-seo/域名与页面核验表.csv"):
        note = row["观察结论"]
        add(row["案例"], row["请求或引用网址"], category(note), note, "工业与 B2B 逐页核验表")

    for row in rows("2026-11-12-china-b2b-country-networks/厂家公开目录链接与地区标签.csv"):
        add(row["品牌"], row["域名或子域"], "厂家目录所列", row["厂家目录中的标签"], "中国制造厂家目录")

    for row in rows("2026-11-12-china-b2b-country-networks/全部候选与逐页证据.csv"):
        note = row["访问口径"]
        add(row["品牌线索"], row["输入"], category(note), note, "中国制造逐页核验表")

    for row in rows("2026-11-12-sany-global-network/三一全球站点与域名清单.csv"):
        kind = row["分类"]
        add("SANY", row["代表网址"] or row["域名或子域"], kind, row["归属与状态说明"], "三一 101 对象分类表")

    for row in rows("2026-11-12-sany-global-network/三一网站语言与区域路径.csv"):
        if row["类型"] in {"全球主站已声明", "集团与业务站本地样本", "渠道语言样本"}:
            add("SANY", row["入口"], "语言与地区样本", row["类型"] + "；" + row["说明"], "三一语言与区域样本表")

    for row in rows("2026-11-05-site-network/全部核验对象总表.csv"):
        kind = row["分类"]
        label = "包装核心关联入口" if kind.startswith("A ") else category(kind)
        add("PDT R US / Design Media Service", row["域名"], label,
            kind + "；" + row["当前状态"], "包装 60 对象分类表")

    # Keep each publicly observed core URL as recorded, including its www form.
    for row in rows("2026-11-05-site-network/站群域名与逐站证据.csv"):
        add("PDT R US / Design Media Service", row["代表核验页面"], "包装核心关联入口",
            "高置信共同运营关联；不等同法律所有权", "包装核心逐站证据")
        add("PDT R US / Design Media Service", row["联系页"], "公开联系页",
            "原研究公开联系入口", "包装核心逐站证据")

    # These product/contact examples were also cited in the earlier narrative.
    previous_examples = {
        "SANY": [
            "https://sany-france.com/privacy-policy/",
            "https://www.sany.in/about-us/", "https://www.sany.in/dealer/",
            "https://www.sanyeurope.com/produkte/bagger/sy215c/",
            "https://www.sanyglobal.com/product/excavator/medium_excavator/113/145",
            "https://www.sanypoland.com/pl/index.php/kontakt/",
        ],
        "Hilti": ["https://www.hilti.cz/c/CLS_POWER_TOOLS_7125",
                  "https://www.hilti.de/c/CLS_POWER_TOOLS_7125",
                  "https://www.hilti.lt/c/CLS_POWER_TOOLS_7125"],
    }
    for name, urls in previous_examples.items():
        for url in urls:
            add(name, url, "产品与业务页面", "此前正文所列的产品、公司或联系页面", "案例正文页面样本")

    order = {case.name: i for i, case in enumerate(cases)}
    return sorted(links.values(), key=lambda link: order[link.case])


def link_groups(records: Sequence[SiteLink]) -> list[tuple[str, list[str]]]:
    grouped: dict[str, list[str]] = {}
    for record in records:
        grouped.setdefault(record.category, []).append(record.url)
    return list(grouped.items())
