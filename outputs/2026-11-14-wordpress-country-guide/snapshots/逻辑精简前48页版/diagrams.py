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
    "history": Figure("历史证据 / AI 建站普及之前的国家站实践", 180, "历史节点来自企业公告、创始人访谈与项目原文。", "2004 年 Onlineprinters 德国 .de 站；2011 年法国 .fr 和西班牙 .es 站；2018 年 Mascus 项目已有 32 个国家域名与 25 种语言。"),
    "mascus_results": Figure("Mascus / 欧洲项目 2018 年下半年对比 2017 年同期", 188, "增长数字与同比范围均来自原始项目披露。", "自然搜索会话 +21%；联系请求 +13.1%。原文图表记录联系请求从约 90,000 增至 101,900。"),
    "ai_economics": Figure("工作量变化 / AI 协助降低三类重复投入", 190, "展示可协助的工作环节，不代表统一的成本降幅或工期。", "建站：AI 与可复用规范协助设计开发；内容：共同产品资料支撑多语言初稿；维护：AI 协助整理与更新，业务人员确认事实。"),
    "solution_value": Figure("方案能力 / 从网站展示到多国内容经营", 171, "按真实业务定制；各国语言和商业承诺以企业确认的资料为依据。", "AI 协助定制外贸网站、制作当地语言内容与持续经营；WordPress 提供产品和内容后台。"),
    "case_map": Figure("案例导航 / 去重后的四组阅读入口", 191, "分组按本册阅读用途归档；重复案例合并后总计 125 组。", "2 组主案例、21 组中国制造、71 组工业与 B2B、31 组跨行业与架构参照，共 125 组。"),
    "buyer_journey": Figure("教学示意 / 从采购需求到咨询", 165, "每一步都需要相应的页面与信息支持。", "采购需求 → 当地语言搜索 → 阅读合适页面 → 提出具体咨询。"),
    "three_layers": Figure("教学示意 / 三项工作的分工", 195, "三项配合：覆盖语言、回答采购问题、明确服务市场。", "多语言解决谁能读懂；当地化解决怎样表达采购信息；国家域名说明面向哪个市场。"),
    "domain_value": Figure("教学示意 / 地域信号与经营工作", 180, "国家后缀帮助表达面向的市场；具体排名由更多因素共同影响。", ".de 提供德国市场线索；产品内容、可信资料、网站可用性和持续运营共同支持业务。"),
    "sticker_network": Figure("案例结构 / StickerPrinting 欧洲语言入口", 190, "根据公开入口与经营声明重绘；不表示各市场的流量或经营规模。", "StickerPrinting Deutschland 的德国、法国、西班牙、意大利和罗马尼亚入口，分别使用当地语言。"),
    "packaging_terms": Figure("案例结构 / 五种语言的硬盒入口", 203, "域名词语是研究当地叫法的线索，页面内容仍须结合实际产品核对。", "西语 cajasforradas.es、法语 boitesrigides.fr、德语 stabileschachtel.de、意语 scatolerivestite.it、英语 rigidboxespackaging.co.uk。"),
    "china_sales": Figure("案例观察 / 国家入口里的采购路径", 174, "厂家目录与当地经营身份一起核对；这些路径不代表已验证实际成交。", "徐工智利：设备与报价；福田波兰：主力车型与当地联系；MAXUS：车型、经销和服务。"),
    "china_industry": Figure("案例观察 / 工业国家站的内容组织", 174, "同一份产品事实，按各市场的选型与服务需求组织。", "杭叉将产品与配件、服务连接；海天在同一市场区分产品线；NOARK 以稳定编号对应多国目录。"),
    "igus_product": Figure("案例结构 / 同一 E2/000 系列", 181, "四国样本都有对应产品页；图中连线表示产品对应关系。", "igus E2/000 系列对应 igus.de、igus.pl、igus.cz、igus.ro 的当地语言产品页。"),
    "industry_compare": Figure("案例观察 / 多国网站深入到具体产品与采购分类", 183, "同一产品体系，以各国页面承接当地阅读与采购需求。", "PERI DUO 系列对应捷克和斯洛伐克；Hilti 多国电动工具类目共用 CLS_POWER_TOOLS_7125 编号。"),
    "sany_purchase": Figure("案例结构 / sany.in 的国家业务入口", 179, "印度站使用英语；语言选择根据目标采购人群确定。", "三一印度国家域名 sany.in 连接产品、公司、经销与零部件信息。"),
    "sany": Figure("案例结构 / 三一的多层业务分工", 176, "25 个高置信集团及业务根域，包含全球、区域和产品线等入口。", "三一全球品牌与产品主站，连接国家或区域业务、产品线和当地渠道等职责。"),
    "packaging_counts": Figure("案例数据 / 47 个核心关联根域", 185, "按研究中的目标市场归类；43 个获客站 + 4 个公司或综合门户。", "英国 16 个、美国与全球门户 18 个、澳大利亚 13 个，共 47 个核心关联根域。"),
    "packaging": Figure("案例与启发 / 多个入口，集中承接", 185, "左侧来自公开联系页；右侧是可借鉴的业务组织方式。", "公开观察：43 个获客站映射到共用联系表单；业务启发：多个市场与产品入口可以集中承接，并区分咨询来源。"),
    "project_results": Figure("项目结果 / 专业内容与 SEO 的业务价值", 202, "三个项目的时期、范围与指标不同；数字均为发布方披露。", "PROFISHOP 项目点击 +109%；Quick-Step 六市场优化内容页平均点击 +100.53%；Dextra 12 个月自然搜索询盘 +38%。"),
    "team_split": Figure("成本结构 / 国家站长期需要的协作", 176, "参考 Manutan 的 23 市场项目，概括共同与当地工作的关系。", "共同产品资料、技术与监测；当地用词、采购问题与服务内容；持续的销售沟通和内容反馈。"),
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
        elif k == "case_map":
            col = (w - 14) / 2
            values = [("2 组 · 主案例", "三一 / PDT R US 包装网络"), ("21 组 · 中国制造", "徐工 / 福田 / 杭叉 / 海天等"), ("71 组 · 工业与 B2B", "igus / Hilti / Festo / RAJA 等"), ("31 组 · 跨行业与架构", "vidaXL / Skyscanner / Picodi 等")]
            for i, (title, sub) in enumerate(values):
                self.box((i % 2) * (col + 14), 26 + (i // 2) * 65, col, 58, title, sub, dark=i == 0, title_size=12, sub_size=9)
        elif k == "buyer_journey":
            self.sequence([("01 采购需求", "定制硬盒\n尺寸 / 材料 / 数量"), ("02 搜索", "使用熟悉的语言\n寻找产品与供应商"), ("03 看页面", "核对选项、资料\n交付与服务"), ("04 提咨询", "提交具体要求\n销售继续沟通")], height=98, dark_index=2)
        elif k == "three_layers":
            self.sequence([("多语言", "让不同语言的\n采购人群读懂\n\n例：德语 / 法语"), ("当地化内容", "用行业用词回答\n选型与合作问题\n\n例：材料 / 拿样"), ("独立国家域名", "为目标市场设置\n清楚的业务入口\n\n例：.de / .fr")], height=130, dark_index=1, connect=False)
        elif k == "domain_value":
            self.box(0, 28, 134, 60, ".de", "德国国家后缀", dark=True, title_size=18)
            self.arrow(140, 58, 187, 58)
            self.box(194, 28, w - 194, 60, "面向德国市场的线索", "帮助表达服务地区", title_size=12)
            for i, title in enumerate(["相关产品内容", "可信业务资料", "网站正常可用", "持续更新运营"]):
                width = (w - 24) / 4
                self.box(i * (width + 8), 101, width, 40, title, "", title_size=10)
        elif k == "sticker_network":
            self.hub("StickerPrinting Deutschland", "相关经营声明指向同一德国主体", [("德国 .de", "德语内容"), ("法国 .fr", "法语内容"), ("西班牙 .es", "西语内容"), ("意大利 .it", "意语内容"), ("罗马尼亚 .ro", "罗语内容")], child_height=60)
        elif k == "packaging_terms":
            self.box(0, 29, 103, 134, "定制硬盒", "同类产品\n\n不同语言\n不同采购表达", dark=True)
            values = [("西语", "cajasforradas.es"), ("法语", "boitesrigides.fr"), ("德语", "stabileschachtel.de"), ("意语", "scatolerivestite.it"), ("英语", "rigidboxespackaging.co.uk")]
            for i, (language, host) in enumerate(values):
                top = 28 + i * 28
                self.rect(117, top, w - 117, 24, MINT if i % 2 == 0 else colors.HexColor("#F3F6F6"), radius=3)
                self.text(language, 126, top + 5, 40, size=9.2, bold=True, max_height=17)
                self.text(host, 173, top + 5, w - 183, size=10, max_height=17)
        elif k == "china_sales":
            self.sequence([("徐工 · 智利", "xcmg.cl\n设备信息\n继续进入报价入口"), ("福田 · 波兰", "e-van.com.pl\nFOTON eAumark\n主力产品与当地联系"), ("MAXUS · 北欧", "挪威 / 丹麦 / 芬兰\n车型介绍\n经销与服务信息")], height=106, connect=False)
        elif k == "china_industry":
            self.rows([("杭叉", "叉车产品与参数", "配件、维修与支持"), ("海天", "同一国家的业务入口", "按注塑等产品线分工"), ("NOARK", "多国语言产品目录", "稳定编号与技术附件")], row_height=39)
        elif k == "igus_product":
            self.hub("E2/000 · 同一拖链系列", "稳定产品身份，分别组织当地页面", [("igus.de", "德国 / 德语"), ("igus.pl", "波兰 / 波兰语"), ("igus.cz", "捷克 / 捷克语"), ("igus.ro", "罗马尼亚 / 罗语")], child_height=56)
        elif k == "industry_compare":
            col = (w - 16) / 2
            self.box(0, 27, col, 119, "PERI · DUO 产品系列", "捷克 .cz  ↔  斯洛伐克 .sk\n\n共同的产品系列\n分别表达当地产品资料", dark=True)
            self.box(col + 16, 27, col, 119, "Hilti · 电动工具类目", "德国 .de / 立陶宛 .lt / 捷克 .cz\n\n共用类目编号\nCLS_POWER_TOOLS_7125", sub_size=8.6)
        elif k == "sany_purchase":
            self.hub("sany.in · 印度国家域名", "让买家在一个市场入口继续了解业务", [("产品", "查型号与用途"), ("公司", "了解当地业务"), ("经销商", "寻找销售联系"), ("零部件", "了解后续支持")], child_height=54)
        elif k == "sany":
            self.hub("全球品牌与产品主站", "sanyglobal.com / 同域 12 种语言声明", [("国家与区域", "印度 / 欧洲等"), ("产品线", "设备与业务入口"), ("当地渠道", "经销 / 销售 / 服务")], child_height=50)
        elif k == "packaging_counts":
            domain_counts = [("英国", 16), ("美国 / 全球", 18), ("澳大利亚", 13)]
            for i, (label, count) in enumerate(domain_counts):
                top = 33 + i * 38
                self.text(label, 0, top + 5, 94, size=10.3, bold=True, max_height=22)
                self.rect(102, top, (w - 145) * count / 18, 24, TEAL if i != 1 else INK, radius=3)
                self.text(str(count), 111 + (w - 145) * count / 18, top + 4, 32, size=11, bold=True, max_height=24)
        elif k == "packaging":
            col = (w - 20) / 2
            self.box(0, 28, col, 121, "公开观察", "43 个获客站\n↓\n共用联系表单\n保留品牌与地区代码", dark=True)
            self.box(col + 20, 28, col, 121, "业务启发", "不同国家与产品入口\n↓\n集中承接客户需求\n保留各市场的咨询来源", gold=True)
        elif k == "project_results":
            col = (w - 20) / 3
            data = [("PROFISHOP", "+109%", "项目点击\n2020.05 上线至\n2022.12 披露"), ("Quick-Step", "+100.53%", "优化内容页平均点击\n六市场 / 项目为期 1 年\n比较起止日期未明确"), ("Dextra", "+38%", "自然搜索询盘\n12 个月的项目\n未拆分域名贡献")]
            for i, (name, metric, scope) in enumerate(data):
                x = i * (col + 10)
                self.rect(x, 28, col, 136, MINT)
                self.text(name, x + 10, 37, col - 20, size=10.8, bold=True, max_height=20)
                self.text(metric, x + 10, 63, col - 20, size=18 if i == 1 else 20, color=TEAL, bold=True, max_height=32)
                self.text(scope, x + 10, 102, col - 20, size=8.6, color=MUTED, max_height=50)
        elif k == "team_split":
            self.sequence([("集中管理", "共同产品资料\n技术模板与监测\n保持资料版本一致"), ("当地确认", "行业用词与客户问题\n产品选择与服务承诺\n确认页面适用范围"), ("销售反馈", "回复咨询与报价\n记录有效性和新问题\n带回下一轮内容任务")], height=109, dark_index=0)
        elif k == "solution_value":
            self.sequence([("定制外贸网站", "展示产品与制造能力\n承接具体询价需求"), ("多语言国家站", "不同国家独立入口\n当地语言与采购内容"), ("长期内容经营", "产品、文章与案例\nAI 和团队持续参与")], height=105, dark_index=1, connect=False)
        else:
            raise ValueError(f"Renderer missing for figure: {k}")
        c.restoreState()
