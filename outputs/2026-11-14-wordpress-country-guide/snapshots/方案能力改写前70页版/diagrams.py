"""Vector teaching figures for the country-domain field guide."""
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
    "case_map": Figure("案例导航 / 去重后的四组阅读入口", 191, "分组按本册阅读用途归档；重复案例合并后总计 125 组。", "2 组主案例、21 组中国制造、71 组工业与 B2B、31 组跨行业与架构参照，共 125 组。"),
    "buyer_journey": Figure("教学示意 / 从采购需求到咨询", 165, "每一步都需要相应的页面与信息支持。", "采购需求 → 当地语言搜索 → 阅读合适页面 → 提出具体咨询。"),
    "three_layers": Figure("教学示意 / 三项工作的分工", 195, "三项配合：覆盖语言、回答采购问题、明确服务市场。", "多语言解决谁能读懂；当地化解决怎样表达采购信息；国家域名说明面向哪个市场。"),
    "domain_value": Figure("教学示意 / 地域信号与经营工作", 180, "国家后缀帮助表达面向的市场；具体排名由更多因素共同影响。", ".de 提供德国市场线索；产品内容、可信资料、网站可用性和持续运营共同支持业务。"),
    "search_steps": Figure("教学示意 / 上线后的搜索过程", 163, "各阶段分别检查；上线不代表已经收录，也不代表获得询盘。", "发布让页面可以访问，抓取是读取页面，收录是纳入索引，展示是匹配相关查询。"),
    "country": Figure("实施示意 / 共用资料，分别发布", 184, "共用的是资料与组件；各国内容、正式域名和来源记录分别管理。", "批准的产品资料与 AI 维护流程，支持德国 .de、法国 .fr、波兰 .pl 三个国家入口。"),
    "sticker_network": Figure("案例结构 / StickerPrinting 欧洲语言入口", 190, "根据公开入口与经营声明重绘；不表示各市场的流量或经营规模。", "StickerPrinting Deutschland 的德国、法国、西班牙、意大利和罗马尼亚入口，分别使用当地语言。"),
    "packaging_terms": Figure("案例结构 / 五种语言的硬盒入口", 203, "域名词语是研究当地叫法的线索，页面内容仍须结合实际产品核对。", "西语 cajasforradas.es、法语 boitesrigides.fr、德语 stabileschachtel.de、意语 scatolerivestite.it、英语 rigidboxespackaging.co.uk。"),
    "china_sales": Figure("案例观察 / 国家入口里的采购路径", 174, "厂家目录与当地经营身份一起核对；这些路径不代表已验证实际成交。", "徐工智利：设备与报价；福田波兰：主力车型与当地联系；MAXUS：车型、经销和服务。"),
    "china_industry": Figure("案例观察 / 工业国家站的内容组织", 174, "同一份产品事实，按各市场的选型与服务需求组织。", "杭叉将产品与配件、服务连接；海天在同一市场区分产品线；NOARK 以稳定编号对应多国目录。"),
    "igus_product": Figure("案例结构 / 同一 E2/000 系列", 181, "四国样本都有对应产品页；图中连线表示产品对应关系。", "igus E2/000 系列对应 igus.de、igus.pl、igus.cz、igus.ro 的当地语言产品页。"),
    "industry_compare": Figure("案例观察 / 用产品与类目身份保持对应", 183, "可读页面与技术声明分别检查；不能从首页推断全部产品页的设置。", "PERI DUO 系列对应捷克和斯洛伐克；Hilti 多国电动工具类目共用 CLS_POWER_TOOLS_7125 编号。"),
    "sany_purchase": Figure("案例结构 / sany.in 的国家业务入口", 179, "印度站使用英语；语言选择根据目标采购人群确定。", "三一印度国家域名 sany.in 连接产品、公司、经销与零部件信息。"),
    "sany": Figure("案例结构 / 三一的多层业务分工", 176, "25 个高置信集团及业务根域，包含全球、区域和产品线等入口。", "三一全球品牌与产品主站，连接国家或区域业务、产品线和当地渠道等职责。"),
    "product_master": Figure("实施示意 / 从 SY215C 样本提炼管理方法", 181, "同型号先核配置与适用市场，再决定哪些参数和附件可以共用。", "以 SY215C 产品身份关联全球英文、西语以及欧洲德语、英语页面，分别记录配置和资料版本。"),
    "packaging_counts": Figure("案例数据 / 47 个核心关联根域", 185, "按研究中的目标市场归类；43 个获客站 + 4 个公司或综合门户。", "英国 16 个、美国与全球门户 18 个、澳大利亚 13 个，共 47 个核心关联根域。"),
    "packaging": Figure("案例与实施 / 集中联系，保留入口来源", 185, "左侧来自公开联系页；右侧是供你实施的来源记录与销售分配建议。", "公开观察：43 个获客站映射到共用联系表单；实施建议：记录国家、域名、产品和页面，再分配负责人。"),
    "project_results": Figure("项目披露 / 指标的范围比大小更重要", 202, "三个项目的时期、范围与指标不同，不构成可直接比较的效果排行。", "Mascus 欧洲项目 2018 下半年同比：自然搜索会话 +21%，联系请求 +13.1%；PROFISHOP 项目点击 +109%；Quick-Step 六市场优化内容页平均点击 +100.53%。"),
    "team_split": Figure("实施示意 / 参考 Manutan 的集中与当地协作", 176, "Manutan 项目覆盖 23 个市场；本图将分工方法转成小团队的任务。", "集中管理产品资料、技术与监测；当地确认用词、采购问题与服务；销售跟进需求并反馈内容问题。"),
    "query_intent": Figure("教学示意 / 采购任务对应页面", 181, "中文示例用于解释方法，没有附加搜索量或排名假设。", "找定制硬盒供应商对应分类页；了解内托材料选择对应采购指南；查看 BOX-001 参数对应产品详情。"),
    "search_snippet": Figure("教学示意 / 虚拟搜索结果", 209, "用中文解释结构；正式标题与摘要按当地语言和已批准事实编写。", "搜索结果由网址、标题和摘要构成；标题说清产品，摘要说明材料、定制与报价信息，正文兑现这些内容。"),
    "product_page": Figure("教学示意 / 定制硬盒产品页结构", 236, "图中只有内容结构，未预设真实规格、认证、最低起订量或交期。", "产品页先展示产品身份和真实图片，再提供材料规格、工艺证据、合作流程及询价入口。"),
    "content_links": Figure("教学示意 / 内链把采购问题连到产品", 167, "每个国家站都应有自己的清晰路径；链接文字说明下一页能看到什么。", "采购指南连接相关分类与产品，产品提供资料下载和询价入口。"),
    "trust_links": Figure("教学示意 / 网站内外的可信资料", 182, "自家国家站的版本切换属于导航；独立行业来源的引用需要分别识别。", "网站内展示产品事实、公司与交付证据；网站外通过相关行业、客户或伙伴的真实引用帮助买家核对。"),
    "language_seo": Figure("教学示意 / 同一产品的跨国版本", 214, "网址为结构示意；独立当地页的首选地址与跨国版本表承担不同职责。", "德国产品页声明自己的首选网址，法国产品页也声明自己；两页的 hreflang 表同时列出自身与对方。"),
    "ai_quality": Figure("实施示意 / 从批准资料到可发布页面", 173, "每个国家页都要能独立帮助买家了解产品并提出需求。", "批准资料 → AI 整理与起草 → 产品和目标语审核 → 发布有用的当地页面。"),
    "static": Figure("实施示意 / 静态页面与询盘处理", 186, "Tidio 可作为聊天入口；业务员负责回复、报价与跟进。", "AI 与 Skill 制作文件，Cloudflare 发布国家网站，服务端程序处理表单，Resend 将询盘发到邮箱。"),
    "launch": Figure("实施示意 / 首站的三个验收结果", 166, "用正式域名检查实际输出；编辑、保存与收件分别记录结果。", "检查前台内容和正式网址；验证后台编辑或静态更新发布；提交测试询盘并核对保存与实际收件。"),
    "maintain_cycle": Figure("实施示意 / 一次产品变化的维护闭环", 198, "保存资料与发布版本；市场专属的交付、联系与服务说明单独保留。", "更新产品主表 → 找出受影响国家页 → 审核修改预览 → 分别发布并复查，再把反馈带回主表。"),
    "measure_funnel": Figure("教学示意 / 从搜索表现到销售推进", 192, "层级形状只表示流程，不表示人数、转化率或各阶段的真实比例。", "搜索曝光 → 搜索点击 → 收到咨询 → 判定有效询盘 → 报价或样品推进；前两层由搜索工具观察，后三层由表单与销售记录。"),
    "operations": Figure("日常场景 / 三类读者怎样使用后台", 184, "工作方式示意；常改内容需要在建站时安排好编辑入口。", "工厂老板把日常修改交给同事；SOHO 自己完成少量更新；外贸公司用产品编号对齐不同供应商的资料。"),
    "wp_editor": Figure("编辑示意 / 后台栏目与产品页对应", 235, "按产品编辑方式绘制的示意图；实际栏目与样式按网站设计。", "产品名称、图片、参数、详情、常见问题和关联产品在后台分别编辑；前台模板将它们组织成产品展示与询价页面。"),
    "wp_team": Figure("协作示意 / 新内容从草稿到发布", 178, "角色和权限按本站配置；已发布内容的修改另行核对影响。", "AI 或编辑准备草稿，业务负责人核事实，目标语审核人核表达，具有权限的人发布并检查。"),
    "wp_country": Figure("实施方案 / 共用资料，各国独立维护", 213, "不假定一个总后台自动同步全部网站；按项目分别更新与检查。", "共用批准资料、术语和设计规范，德国、法国、波兰分别使用独立 WordPress 站；各国保留当地内容、收件负责人和发布记录。"),
    "learning_path": Figure("实操路径 / 六项能够亲手展示的能力", 222, "完成条件看实际结果；学习与建站进度根据资料和项目复杂度安排。", "规划页面、完成首站、编辑产品、发布当地内容、验证实际收件、执行更新与恢复演练。"),
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
        if k == "case_map":
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
        elif k == "search_steps":
            self.sequence([("发布", "页面可以访问\n先检查正式网址"), ("抓取", "搜索引擎访问\n读取页面内容"), ("收录", "分析后纳入\n可检索的索引"), ("搜索展示", "相关查询出现\n再匹配结果")], height=95, dark_index=2)
        elif k == "country":
            self.hub("产品资料 + AI 集中维护", "共用事实、术语、组件和变更记录", [("德国 .de", "德语内容\n德国业务来源"), ("法国 .fr", "法语内容\n法国业务来源"), ("波兰 .pl", "波兰语内容\n波兰业务来源")], child_height=56)
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
            self.box(0, 27, col, 119, "PERI · DUO 产品系列", "捷克 .cz  ↔  斯洛伐克 .sk\n\n产品身份对应\n页面内容与技术标记分开核对", dark=True)
            self.box(col + 16, 27, col, 119, "Hilti · 电动工具类目", "德国 .de / 立陶宛 .lt / 捷克 .cz\n\n共用类目编号\nCLS_POWER_TOOLS_7125", sub_size=8.6)
        elif k == "sany_purchase":
            self.hub("sany.in · 印度国家域名", "让买家在一个市场入口继续了解业务", [("产品", "查型号与用途"), ("公司", "了解当地业务"), ("经销商", "寻找销售联系"), ("零部件", "了解后续支持")], child_height=54)
        elif k == "sany":
            self.hub("全球品牌与产品主站", "sanyglobal.com / 同域 12 种语言声明", [("国家与区域", "印度 / 欧洲等"), ("产品线", "设备与业务入口"), ("当地渠道", "经销 / 销售 / 服务")], child_height=50)
        elif k == "product_master":
            self.hub("SY215C · 产品身份与版本记录", "具体配置、参数和附件按市场核对", [("全球英文", "sanyglobal.com"), ("全球西语", "sanyglobal.com"), ("欧洲德语", "sanyeurope.com"), ("欧洲英语", "sanyeurope.com")], child_height=56)
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
            self.box(col + 20, 28, col, 121, "你的实施设计", "国家 + 域名 + 产品 + 页面\n↓\n可识别来源的询盘记录\n负责人回复与跟进", gold=True)
        elif k == "project_results":
            col = (w - 20) / 3
            data = [("Mascus", "+21%", "自然搜索会话\n联系请求 +13.1%\n欧洲 / 2018 下半年同比"), ("PROFISHOP", "+109%", "项目点击\n2020.05 上线至\n2022.12 公布"), ("Quick-Step", "+100.53%", "优化内容页平均点击\n六个市场\n未逐国家域名拆分")]
            for i, (name, metric, scope) in enumerate(data):
                x = i * (col + 10)
                self.rect(x, 28, col, 136, MINT)
                self.text(name, x + 10, 37, col - 20, size=10.8, bold=True, max_height=20)
                self.text(metric, x + 10, 63, col - 20, size=20 if i < 2 else 18, color=TEAL, bold=True, max_height=32)
                self.text(scope, x + 10, 102, col - 20, size=8.6, color=MUTED, max_height=50)
        elif k == "team_split":
            self.sequence([("集中管理", "共同产品资料\n技术模板与监测\n保持资料版本一致"), ("当地确认", "行业用词与客户问题\n产品选择与服务承诺\n确认页面适用范围"), ("销售反馈", "回复咨询与报价\n记录有效性和新问题\n带回下一轮内容任务")], height=109, dark_index=0)
        elif k == "query_intent":
            self.rows([("找供应商", "定制硬盒供应商", "→ 产品分类页"), ("比较选择", "硬盒内托材料怎样选", "→ 采购指南"), ("核对产品", "BOX-001 的参数", "→ 产品详情页")], row_height=41)
        elif k == "search_snippet":
            self.rect(0, 27, w, 145, colors.white, LINE)
            self.rect(12, 38, w - 24, 27, colors.HexColor("#F3F6F6"), radius=13)
            self.text("搜索：定制硬盒 材料与尺寸", 24, 45, w - 48, size=10, max_height=18)
            self.text("1. example.invalid / 国家站 / 定制硬盒", 18, 79, w - 175, size=9, color=MUTED, max_height=18)
            self.text("2. 定制硬盒 · 材料与定制方式", 18, 102, w - 175, size=13, color=BLUE, bold=True, max_height=22)
            self.text("3. 了解材料与结构选项，查看询价需提供的尺寸、数量和设计资料。", 18, 131, w - 175, size=9.2, max_height=29)
            self.text("网址：页面在哪里\n\n标题：提供什么\n\n摘要：为什么继续看", w - 143, 79, 132, size=9.3, color=MUTED, max_height=86)
        elif k == "product_page":
            left = w * 0.61
            self.rect(0, 26, left, 178, colors.white, LINE)
            self.rect(9, 35, left - 18, 18, INK, radius=3)
            self.text("产品 / 应用 / 质量 / 联系", 18, 38, left - 36, size=8, color=colors.white, max_height=14)
            self.rect(10, 62, 91, 58, MINT, radius=3)
            c.setStrokeColor(TEAL)
            c.setLineWidth(1)
            c.rect(29, self.height - 103, 50, 23, stroke=1, fill=0)
            c.line(29, self.height - 80, 42, self.height - 70)
            c.line(79, self.height - 80, 88, self.height - 70)
            c.line(42, self.height - 70, 88, self.height - 70)
            self.text("真实产品图片", 18, 108, 78, size=7.7, max_height=13)
            self.text("1. 定制硬盒 / 型号", 114, 63, left - 124, size=10, bold=True, max_height=17)
            self.text("用途与可选结构\n材料、尺寸与工艺", 114, 85, left - 124, size=8.8, max_height=29)
            bands = [("2. 规格 / 选项 / 技术资料", MINT), ("3. 制造证据 / 样品与交付流程", colors.HexColor("#F3F6F6")), ("4. 提交数量、尺寸与图纸，申请报价", SAND)]
            for i, (title, fill) in enumerate(bands):
                self.rect(10, 129 + i * 23, left - 20, 19, fill, radius=3)
                self.text(title, 17, 132 + i * 23, left - 34, size=8.3, max_height=14)
            self.text("1. 我在看什么产品？\n\n2. 能否满足我的要求？\n\n3. 怎样核对与合作？\n\n4. 要提供什么才能报价？", left + 17, 40, w - left - 20, size=9.5, max_height=158)
        elif k == "content_links":
            self.sequence([("采购指南", "解释内托怎么选\n链接到相关盒型"), ("产品分类", "比较系列与用途\n找到适合的产品"), ("具体产品", "核对材料与参数\n下载对应资料"), ("询价入口", "自动带出产品来源\n买家补充需求")], height=100, dark_index=2)
        elif k == "trust_links":
            self.sequence([("网站内的事实", "产品与技术资料\n真实公司与交付安排\n证书的适用范围"), ("买家能够核对", "谁提供产品\n能否满足用途\n怎样继续联系"), ("外部真实引用", "客户与合作伙伴\n协会与行业媒体\n相关资料的正常引用")], height=115, dark_index=1, connect=False)
            col = (w - 30) / 3
            self.arrow(col + 2, 87, col + 12, 87)
            self.arrow(2 * col + 28, 87, 2 * col + 18, 87)
        elif k == "language_seo":
            col = (w - 60) / 2
            self.box(0, 29, col, 137, "德国产品 A · 德语", "首选地址 canonical\n指向本页\n\n版本表 hreflang\nde-DE：本页\nfr-FR：法国对应页", dark=True, sub_size=8.8)
            self.box(col + 60, 29, col, 137, "法国产品 A · 法语", "首选地址 canonical\n指向本页\n\n版本表 hreflang\nfr-FR：本页\nde-DE：德国对应页", sub_size=8.8)
            self.arrow(col + 6, 96, col + 54, 96, both=True)
            self.text("对应", col + 14, 72, 38, size=9, color=TEAL, max_height=15)
            self.text("两页各有首选地址，版本表则相互列出自己和对方。", 0, 173, w, size=9.2, bold=True, max_height=18)
        elif k == "ai_quality":
            self.sequence([("批准资料", "产品参数与图片\n术语和服务范围"), ("AI 初稿", "整理信息与结构\n起草当地语言"), ("人工审核", "核事实与承诺\n核行业和语言"), ("发布页面", "提供完整答案\n支持实际询价")], height=106, dark_index=2)
        elif k == "static":
            self.sequence([("AI + Skill", "协助生成与修改\n网页和配置文件"), ("Cloudflare", "发布国家网站\n绑定正式域名"), ("表单程序", "服务端处理需求\n附上产品来源"), ("Resend + 邮箱", "发出询盘邮件\n销售实际收到")], height=112, dark_index=2)
        elif k == "launch":
            self.sequence([("01 前台与网址", "内容与手机布局\n正式域名及深页\n语言与 SEO 输出"), ("02 内容可维护", "编辑并保存重开\n新增草稿或更新文件\n检查实际页面生效"), ("03 询盘可追踪", "提交标记测试询盘\n核对保存与实际收件\n识别产品和来源")], height=101, dark_index=1)
        elif k == "maintain_cycle":
            col = (w - 34) / 2
            self.box(0, 28, col, 55, "1 更新批准主表", "记录型号、字段和资料版本", dark=True)
            self.box(col + 34, 28, col, 55, "2 找到受影响页面", "按产品编号查国家与配置")
            self.box(col + 34, 103, col, 55, "3 审核修改预览", "核参数、语言和市场专属内容")
            self.box(0, 103, col, 55, "4 分别发布并复查", "保留版本，带回问题与反馈", gold=True)
            self.arrow(col + 3, 55, col + 31, 55)
            self.arrow(col + 34 + col / 2, 87, col + 34 + col / 2, 99)
            self.arrow(col + 31, 130, col + 3, 130)
            self.arrow(col / 2, 99, col / 2, 87)
        elif k == "measure_funnel":
            labels = [("搜索曝光", "搜索结果里出现"), ("搜索点击", "从搜索进入页面"), ("收到咨询", "表单或联系记录"), ("有效询盘", "销售判定需求匹配"), ("报价 / 样品", "记录后续推进状态")]
            for i, (title, sub) in enumerate(labels):
                width = 270 - i * 28
                x, top = (270 - width) / 2, 27 + i * 25
                self.rect(x, top, width, 21, TEAL if i < 2 else INK, radius=3)
                self.text(title, x + 11, top + 4, width - 22, size=9, color=colors.white, max_height=15)
                self.text(sub, 291, top + 4, w - 291, size=9.1, color=MUTED, max_height=16)
        elif k == "operations":
            self.sequence([("工厂老板", "同事按栏目维护\n负责人核对事实\n交接时有章可循"), ("SOHO", "自己换图、改参数\n草稿逐步补齐\n批量任务请 AI 协助"), ("外贸公司", "不同产品分开编号\n参数与图片相对应\n同事能找回正确资料")], height=116, dark_index=1, connect=False)
        elif k == "wp_editor":
            col = (w - 46) / 2
            self.rect(0, 28, col, 169, colors.white, LINE)
            self.rect(col + 46, 28, col, 169, MINT)
            self.text("团队编辑的内容", 11, 38, col - 22, size=11, bold=True, max_height=18)
            self.text("买家看到的产品页", col + 57, 38, col - 22, size=11, bold=True, max_height=18)
            fields = ["产品名称 / 型号", "图片 / 图库", "参数 / 规格", "产品说明 / 常见问题", "分类 / 关联产品"]
            outputs = ["标题与产品身份", "产品图片展示", "清楚的参数表", "采购问题的答案", "分类入口与推荐产品"]
            for i, (field, output) in enumerate(zip(fields, outputs)):
                top = 66 + i * 23
                self.rect(10, top, col - 20, 19, colors.HexColor("#F3F6F6"), radius=3)
                self.text(field, 17, top + 3, col - 34, size=9, max_height=15)
                self.text(output, col + 59, top + 3, col - 26, size=9, max_height=15)
                self.arrow(col + 7, top + 10, col + 39, top + 10)
        elif k == "wp_team":
            self.sequence([("1 准备草稿", "AI 或编辑人员\n使用批准资料"), ("2 核对事实", "业务负责人\n参数与承诺"), ("3 复核表达", "目标语审核人\n术语与阅读"), ("4 发布检查", "有权限的人员\n页面与联系路径")], height=106, dark_index=3)
        elif k == "wp_country":
            self.hub("批准资料 + 术语 + 已确认设计", "AI 根据各站当前内容，按范围协助维护", [("德国 WordPress", ".de / 德语\n当地产品与文章\n独立后台和收件"), ("法国 WordPress", ".fr / 法语\n当地产品与文章\n独立后台和收件"), ("波兰 WordPress", ".pl / 波兰语\n当地产品与文章\n独立后台和收件")], child_height=78)
        elif k == "learning_path":
            col = (w - 24) / 3
            tasks = [("01 规划页面", "产品与采购问题对应"), ("02 完成首站", "自己的国家与产品资料"), ("03 使用后台", "新增产品、修改参数"), ("04 经营内容", "发布当地选型文章"), ("05 验证收件", "正式域名、真实测试"), ("06 接着维护", "核对更新、演练恢复")]
            for i, (title, sub) in enumerate(tasks):
                self.box((i % 3) * (col + 12), 29 + (i // 3) * 79, col, 67, title, sub, dark=i == 2, title_size=11, sub_size=8.8)
        else:
            raise ValueError(f"Renderer missing for figure: {k}")
        c.restoreState()
