"""Vector evidence and concept figures for the country-domain casebook."""
from __future__ import annotations

import html
import math
from dataclasses import dataclass
from typing import Sequence

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable, Paragraph


INK = colors.HexColor("#142F39")
TEAL = colors.HexColor("#087F84")
MINT = colors.HexColor("#E9F5F2")
MUTED = colors.HexColor("#577079")
LINE = colors.HexColor("#D8E3E3")
GOLD = colors.HexColor("#D7A64F")
SAND = colors.HexColor("#FBF2DF")
BLUE = colors.HexColor("#225A9A")


@dataclass(frozen=True)
class Figure:
    label: str
    height: float
    caption: str
    description: str


FIGURES: dict[str, Figure] = {
    "case_proof": Figure("案例对照 / 三种可直接查看的市场入口", 177, "展示实际网站布局；结构证据与流量、询盘结果分别判断。", "三一印度：国家业务入口；英澳包装：同类产品分国家经营；欧洲贴纸：国家域名与当地语言结合。"),
    "history": Figure("历史证据 / AI 建站普及之前的国家站实践", 180, "历史节点来自企业公告、创始人访谈与项目原文。", "2004 年 Onlineprinters 德国 .de 站；2011 年法国 .fr 和西班牙 .es 站；2018 年 Mascus 项目已有 32 个国家域名与 25 种语言。"),
    "mascus_results": Figure("Mascus / 欧洲项目 2018 年下半年对比 2017 年同期", 188, "增长数字与同比范围均来自原始项目披露。", "自然搜索会话 +21%；联系请求 +13.1%。原文图表记录联系请求从约 90,000 增至 101,900。"),
    "ai_economics": Figure("工作量变化 / AI 协助降低三类重复投入", 190, "展示可协助的工作环节，不代表统一的成本降幅或工期。", "建站：AI 与可复用规范协助设计开发；内容：共同产品资料支撑多语言初稿；维护：AI 协助整理与更新，业务人员确认事实。"),
    "solution_value": Figure("方案能力 / 从网站展示到多国内容经营", 171, "按真实业务定制；各国语言和商业承诺以企业确认的资料为依据。", "AI 协助定制外贸网站、制作当地语言内容与持续经营；WordPress 提供产品和内容后台。"),
    "case_map": Figure("案例导航 / 去重后的四组阅读入口", 191, "分组按本册阅读用途归档；重复案例合并后总计 125 组。", "2 组主案例、21 组中国制造、71 组工业与 B2B、31 组跨行业与架构参照，共 125 组。"),
    "buyer_journey": Figure("教学示意 / 从采购需求到咨询", 165, "每一步都需要相应的页面与信息支持。", "采购需求 → 当地语言搜索 → 阅读合适页面 → 提出具体咨询。"),
}


class Diagram(Flowable):
    """Render figures with measured text and explicit bounded layout."""

    def __init__(self, kind: str, width: float) -> None:
        super().__init__()
        if kind not in FIGURES:
            raise ValueError(f"Unknown diagram: {kind}")
        self.kind = kind
        self.spec = FIGURES[kind]
        self.width = width
        self.height = self.spec.height

    def text(self, text: str, x: float, top: float, width: float, *, size: float = 10.0,
             color: colors.Color = INK, bold: bool = False, max_height: float = 200.0) -> float:
        value = html.escape(text).replace("\n", "<br/>")
        for symbol in ("→", "↔", "↓"):
            value = value.replace(symbol, f'<font name="Symbols">{symbol}</font>')
        para = Paragraph(value, ParagraphStyle("figure", fontName="CNB" if bold else "CN", fontSize=size,
                                             leading=size * 1.42, textColor=color, wordWrap="CJK"))
        _, height = para.wrap(width, max_height)
        if height > max_height + 0.2:
            raise ValueError(f"Figure text overflow {self.kind}: {text!r} ({height} > {max_height})")
        para.drawOn(self.canv, x, self.height - top - height)
        return height

    def rect(self, x: float, top: float, width: float, height: float, fill: colors.Color = MINT,
             stroke: colors.Color | None = None, radius: float = 7.0) -> None:
        self.canv.setFillColor(fill)
        self.canv.setStrokeColor(stroke or fill)
        self.canv.setLineWidth(0.8)
        self.canv.roundRect(x, self.height - top - height, width, height, radius, fill=1, stroke=int(stroke is not None))

    def arrow(self, x1: float, t1: float, x2: float, t2: float, *, color: colors.Color = TEAL,
              both: bool = False, dashed: bool = False) -> None:
        c = self.canv
        y1, y2 = self.height - t1, self.height - t2
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(1.1)
        c.setDash(3, 2) if dashed else c.setDash()
        c.line(x1, y1, x2, y2)
        c.setDash()

        def tip(x: float, y: float, angle: float) -> None:
            path = c.beginPath()
            path.moveTo(x, y)
            path.lineTo(x - 4.8 * math.cos(angle - 0.45), y - 4.8 * math.sin(angle - 0.45))
            path.lineTo(x - 4.8 * math.cos(angle + 0.45), y - 4.8 * math.sin(angle + 0.45))
            path.close()
            c.drawPath(path, fill=1, stroke=0)

        angle = math.atan2(y2 - y1, x2 - x1)
        tip(x2, y2, angle)
        if both:
            tip(x1, y1, angle + math.pi)

    def box(self, x: float, top: float, width: float, height: float, title: str, sub: str,
            *, dark: bool = False, gold: bool = False, title_size: float = 11.0, sub_size: float = 9.0) -> None:
        self.rect(x, top, width, height, INK if dark else SAND if gold else MINT)
        used = self.text(title, x + 10, top + 9, width - 20, size=title_size, bold=True,
                         color=colors.white if dark else INK, max_height=height - 18)
        if sub:
            self.text(sub, x + 10, top + used + 12, width - 20, size=sub_size,
                      color=colors.HexColor("#CDE4E3") if dark else MUTED, max_height=height - used - 18)

    def sequence(self, labels: Sequence[tuple[str, str]], *, top: float = 30, height: float = 101,
                 dark_index: int = -1, connect: bool = True) -> None:
        gap = 15.0
        width = (self.width - gap * (len(labels) - 1)) / len(labels)
        for i, (title, sub) in enumerate(labels):
            x = i * (width + gap)
            if i and connect:
                self.arrow(x - gap + 2, top + height / 2, x - 3, top + height / 2)
            self.box(x, top, width, height, title, sub, dark=i == dark_index,
                     title_size=10.3 if len(labels) > 3 else 11.0, sub_size=8.8)

    def hub(self, title: str, subtitle: str, children: Sequence[tuple[str, str]], *, top: float = 26,
            child_height: float = 63) -> None:
        width, cx = self.width, self.width / 2
        hub_width = min(300.0, width * 0.68)
        self.box(cx - hub_width / 2, top, hub_width, 48, title, subtitle, dark=True, title_size=10.7, sub_size=8.5)
        gap = 10.0
        col = (width - (len(children) - 1) * gap) / len(children)
        for i, (name, sub) in enumerate(children):
            x = i * (col + gap)
            self.arrow(cx, top + 48, x + col / 2, top + 70)
            self.box(x, top + 73, col, child_height, name, sub, title_size=10.0, sub_size=8.4)

    def rows(self, rows: Sequence[tuple[str, str, str]], *, top: float = 28, row_height: float = 39,
             widths: tuple[float, float, float] = (0.19, 0.42, 0.39)) -> None:
        for i, row in enumerate(rows):
            self.rect(0, top + i * row_height, self.width, row_height - 4,
                      MINT if i % 2 == 0 else colors.HexColor("#F3F6F6"), radius=4)
            x = 10.0
            for j, cell in enumerate(row):
                col_width = self.width * widths[j]
                self.text(cell, x, top + i * row_height + 8, col_width - 18, size=9.5,
                          bold=j == 0, color=INK if j == 0 else MUTED, max_height=row_height - 14)
                x += col_width

    def draw(self) -> None:
        c, w, k = self.canv, self.width, self.kind
        c.saveState()
        self.text(self.spec.label, 0, 1, w, size=8.7, color=TEAL, bold=True, max_height=18)
        self.text(self.spec.caption, 0, self.height - 26, w, size=8.2, color=MUTED, max_height=25)
        if k == "history":
            self.sequence([("2004", "德国 diedruckerei.de\n开始线上销售"), ("2011", "法国 .fr / 西班牙 .es\n当地语言国家站"), ("2018", "Mascus 欧洲项目\n32 国家域名 / 25 语言")], height=112, dark_index=1)
        elif k == "mascus_results":
            col = (w - 16) / 2
            for i, (metric, title, note) in enumerate([
                ("+21%", "自然搜索会话", "自然搜索访问增加\n同期欧洲项目口径"),
                ("+13.1%", "联系请求", "约 90,000 → 101,900\n项目披露的联系指标"),
            ]):
                x = i * (col + 16)
                self.rect(x, 28, col, 123, INK if i == 1 else MINT)
                self.text(title, x + 14, 40, col - 28, size=11.2, bold=True, color=colors.white if i == 1 else INK, max_height=20)
                self.text(metric, x + 14, 66, col - 28, size=27, bold=True, color=GOLD if i == 1 else TEAL, max_height=41)
                self.text(note, x + 14, 112, col - 28, size=9.0, color=colors.HexColor("#CDE4E3") if i == 1 else MUTED, max_height=30)
        elif k == "ai_economics":
            self.sequence([("建站投入", "规范与组件可复用\nAI 协助设计开发\n\n减少重复制作"), ("多语言内容", "共用产品事实\nAI 协助语言初稿\n\n减少逐份重做"), ("长期维护", "AI 协助整理修改\n业务人员确认事实\n\n减少重复搬运")], height=124, dark_index=1, connect=False)
        elif k == "case_proof":
            self.sequence([("三一 · 印度", "sany.in\n国家业务入口\n产品 / 经销 / 服务"), ("包装 · 英国与澳洲", ".co.uk / .com.au\n同类产品分国家经营\n主要使用英语"), ("贴纸 · 欧洲", ".de / .fr / .es\n当地语言产品内容\n同一品牌多国入口")], height=111, dark_index=1, connect=False)
        elif k == "case_map":
            col = (w - 14) / 2
            values = [("2 组 · 主案例", "三一 / PDT R US 包装网络"), ("21 组 · 中国制造", "徐工 / 福田 / 杭叉 / 海天等"), ("71 组 · 工业与 B2B", "igus / Hilti / Festo / RAJA 等"), ("31 组 · 跨行业与架构", "vidaXL / Skyscanner / Picodi 等")]
            for i, (title, sub) in enumerate(values):
                self.box((i % 2) * (col + 14), 26 + (i // 2) * 65, col, 58, title, sub, dark=i == 0, title_size=12, sub_size=9)
        elif k == "buyer_journey":
            self.sequence([("01 采购需求", "定制硬盒\n尺寸 / 材料 / 数量"), ("02 搜索", "使用熟悉的语言\n寻找产品与供应商"), ("03 看页面", "核对选项、资料\n交付与服务"), ("04 提咨询", "提交具体要求\n销售继续沟通")], height=98, dark_index=2)
        elif k == "solution_value":
            self.sequence([("定制外贸网站", "展示产品与制造能力\n承接具体询价需求"), ("多语言国家站", "不同国家独立入口\n当地语言与采购内容"), ("长期内容经营", "产品、文章与案例\nAI 和团队持续参与")], height=105, dark_index=1, connect=False)
        else:
            raise ValueError(f"Renderer missing for figure: {k}")
        c.restoreState()
