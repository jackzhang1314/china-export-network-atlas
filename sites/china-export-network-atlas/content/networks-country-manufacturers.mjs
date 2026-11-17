import { localWebsite as local, website as site } from "./network-schema.mjs";
import { source } from "./schema.mjs";

const htDirectory = "https://www.hengtonggroup.com/en/home/company/business.html";
const zttProfile = "https://www.zttgroup.com/company-profile/";
const zttTurkey = "https://www.zttgroup.com/aspx/main/news_show.aspx?id=463";
const haitianLocations = "https://haitianinter.com/worldwide-presence/";
const hsgFiling = "https://reportdocs.static.szse.cn/UpFiles/rasinfodisc1/202306/RAS_202306_CA1D8EA51B1E445EB717D66C4232C88B.pdf";
const hsgKorea = "https://www.hsglaser.com/news/254.html";
const snowmanNews = "https://www.snowman.group/en/news/snowman_release/6fc5fd3b3c954e8e96d8774970604ee9.html";
const kaishanProfile = "https://www.kaishan-group.com/about.html";

export const countryManufacturers = [
  {
    id: "hengtong", industry: "cables", name: "亨通集团", english: "Hengtong", structure: "hybrid", lead: "rfq",
    title: "线缆工厂保留葡萄牙、巴西和印尼的本地品牌域名",
    summary: "亨通的集团目录直接链接不同制造主体。葡语和印尼语采购可以进入供应地的线缆、工厂及联系页面。",
    sites: [
      site(htDirectory, "全球", "英语、中文", "亨通集团", "集团业务与全球制造主体", "列出各地线缆及光通信企业、制造业务和联系。", htDirectory),
      local(".pt", "https://www.alcobre.pt/", "葡萄牙", "葡萄牙语", "Alcobre – Condutores Eléctricos, S.A.", "葡萄牙电缆选型与询价", "按线缆用途和规格找产品，并保留当地工厂联系。", htDirectory, "公开葡语页面可查，部分访问会先进入验证页。"),
      local(".com.br", "https://htcabos.com.br/", "巴西", "巴西葡语、英语", "HT Cabos e Tecnologia Ltda.", "巴西通信线缆与技术", "本地葡语产品强调光纤和电信网络，便于查在巴西的制造与供货。", htDirectory),
      local(".co.id", "https://www.voksel.co.id/id", "印度尼西亚", "印尼语、英语", "PT Voksel Electric Tbk", "印尼电缆与工程业务", "以印尼语展示电力、通信线缆与企业联系。", htDirectory),
      site("https://www.cablescom.com/", "西班牙及欧洲", "西语、英语", "Cable de Comunicaciones Zaragoza, S.L.", "通信和信号线缆制造", "发布西语产品及企业信息，服务电信和工程采购。", htDirectory),
      site("https://htegypt.com.eg/", "埃及及周边", "英语", "Hengtong Optic-Electric Egypt Co., S.A.E", "埃及光纤及线缆工厂", "当地工厂介绍和技术产品使用独立埃及域，公开入口的主要正文为英语。", htDirectory),
      site("https://www.hengtongaustralia.com/", "澳大利亚", "英语", "Hengtong Cable Australia Pty Ltd", "澳洲线缆采购与支持", "面向区域工程和采购列产品与联系。", htDirectory),
    ],
    pattern: "集团页给采购识别各国工厂和负责企业，区域工厂保留已有品牌和产品线。葡萄牙、巴西虽然都用葡语，各自的产品、联系和交付地独立维护。埃及和澳洲的站展示了另一种组合，由当地团队用英语对接。",
    path: "网络或电力工程买家可先根据用途和敷设环境找产品，再核对制造地点、当地执行标准、试验报告、项目交付距离以及负责人。",
    insight: "已有海外工厂或收购品牌时，可以保留客户熟悉的域名，补公司关系、规格文件和本地销售联系。先让买家确认谁能供货，再规划翻译范围。",
    boundary: "各站关系依据亨通集团官网业务目录及当地经营内容。网站服务范围以页面公开信息为准。",
    sources: [
      source("亨通全球业务与企业链接", htDirectory, "可逐一交叉核对葡萄牙、巴西、印尼、西班牙、埃及与澳洲站点。"),
      source("亨通集团制造布局", "https://www.hengtonggroup.com/en/home/company/", "集团介绍列有海外工厂与相关业务。"),
    ],
  },
  {
    id: "ztt", industry: "cables", name: "中天科技集团", english: "ZTT", structure: "hybrid", lead: "rfq",
    title: "线缆总部、巴西葡语站与土耳其制造工厂",
    summary: "巴西团队按当地市场展示光通信产品，土耳其工厂保留 Demirer 品牌和土耳其语产品资料。",
    sites: [
      site("https://www.ztt.cn/", "中国制造", "中文", "中天科技集团", "集团与中国制造业务", "集团中文网站提供制造板块、企业和项目资料。", "https://m.ztt.cn/contact/49"),
      site(zttProfile, "全球", "英语及多语种", "中天科技国际业务", "线缆出口目录与制造", "覆盖电力、海缆和光通信业务，集团目录公开海外生产与联系。", "https://www.zttgroup.com/contact-us/"),
      local(".com.br", "https://www.zttcable.com.br/", "巴西", "巴西葡语", "ZTT do Brasil Ltda.", "巴西光通信线缆", "葡语站介绍在地工厂、光纤通信业务和询价窗口。", "https://www.zttcable.com.br/o-grupo-ztt/"),
      local(".com.tr", "https://www.demirerkablo.com.tr/", "土耳其", "土耳其语、英语", "Demirer Kablo", "土耳其电力线缆制造", "工厂以土语展示电缆、配套和企业联系。", zttTurkey),
    ],
    pattern: "巴西站以本地光通信制造为主，土耳其站以收购的电力线缆工厂为主。同一集团的国家站各自服务当地实际产品，行业内容也随工厂职责变化。",
    path: "巴西通信项目与土耳其电力项目分别查本地产品和技术团队。实际报价前准备敷设环境、长度、结构、验收与交付地。",
    insight: "国家分站适合把销售语言、工厂能力和负责交付的主体合在同一条采购路径。独立保留已被客户熟悉的当地品牌，可以继续承接原有产品线。",
    boundary: "巴西和土耳其的主体与网站可核对。集团目录中只有公司地址而未确认独立站点的市场另存为研究线索。",
    sources: [
      source("中天科技全球联系目录", "https://www.zttgroup.com/contact-us/", "列示巴西、土耳其等市场与经营主体。"),
      source("中天科技发布 Demirer Kablo 收购信息", zttTurkey, "说明土耳其业务的集团关系和产品分工。"),
    ],
  },
  {
    id: "haitian", industry: "molding", name: "海天国际与海天塑机", english: "Haitian", structure: "hybrid", lead: "technical",
    title: "注塑机国际业务、土语选型与巴西技术支持",
    summary: "总部国际站介绍生产布局，土耳其和巴西团队对接试模、设备和服务需求，长飞亚有自己的网站。",
    sites: [
      site(haitianLocations, "全球", "英语、中文及多语种", "海天国际", "国际业务与生产布局", "公开制造、应用中心和区域服务布局。", haitianLocations),
      site("https://haitianpm.com/", "全球", "英语、中文", "海天塑机集团", "海天注塑机系列与选型", "围绕注塑设备平台、产品系列和相关技术组织目录。", haitianLocations),
      site("https://zhafir.com/", "全球（德国研发业务）", "英语、中文及地区语言", "长飞亚塑机（Zhafir）", "全电动注塑机品牌", "用独立产品目录介绍全电动设备与应用。", "https://haitianinter.com/about-us/", "本轮初查可打开，复核时直连超时。"),
      local(".com.tr", "https://www.haitian.com.tr/kurumsal", "土耳其", "土耳其语、英语", "Haitian Türkiye", "土耳其设备、试模与支持", "土语介绍本地业务及设备，集团将当地列为试模、培训和备件支持点。", "https://www.haitian.com.tr/en/corporate", "本轮初查可打开，复核时直连超时。"),
      site("https://haitianbrazil.com/", "巴西", "巴西葡语、英语", "Haitian International Brazil", "巴西设备选型与现场支持", "葡语页面介绍设备系列以及当地业务和联系。", "https://haitianbrazil.com/en/company/"),
    ],
    pattern: "海天国际页解释各区域能提供什么，机械品牌站按设备技术分工，土耳其和巴西站把销售、技术与当地联系落地。巴西采用 .com 域名提供葡语，土耳其将土耳其语和当地后缀结合。",
    path: "加工厂先提供材料、制品重量、模具和产量，查适配机型和吨位。当地团队可核对试模、培训和备件请求。",
    insight: "当地语言产品词和当地技术服务配套，可以把询盘从通用联系推进到可评估的生产项目。",
    boundary: "集团地区目录区分生产、应用及服务中心。通过同一注册域提供的欧洲、越南语言版本可供阅读，站数按域名合并。",
    sources: [
      source("海天国际生产与应用中心", haitianLocations, "列出土耳其等市场的工厂、试模或服务设施。"),
      source("海天巴西公司介绍", "https://haitianbrazil.com/en/company/", "可核对当地入口与海天国际品牌业务。"),
    ],
  },
  {
    id: "hsg", industry: "laser", name: "宏山激光", english: "HSG Laser", structure: "country", lead: "technical",
    title: "激光装备出口站与日语、韩语国家域名",
    summary: "广东宏山用国际站介绍产品平台。日本和韩国的公司各有独立域名、当地语言产品和本地咨询入口。",
    sites: [
      site("https://www.hsglaser.cn/", "中国制造", "中文", "广东宏石激光技术股份有限公司", "工厂能力与国内产品", "提供金属成形、激光切割及工厂资料。", "https://www.hsglaser.cn/c/about_hsg.html"),
      site("https://www.hsglaser.com/", "全球", "英语及多语种", "广东宏石激光技术股份有限公司", "出口选型与项目目录", "按板材、管材与自动化等设备应用组织产品，国际联系中列日本等团队。", "https://www.hsglaser.com/pages/contact-us/"),
      local(".co.jp", "https://www.hsglaser.co.jp/", "日本", "日语", "HSGエンジニアリング株式会社", "日本研发、设备与联系", "日语展示激光装备、公司和当地窗口。", hsgFiling),
      local(".co.kr", "https://www.hsglaser.co.kr/", "韩国", "韩语", "HSG Laser Korea", "韩国设备、展厅与技术服务", "韩语目录和到访地址对接釜山当地选型、展示和售后。", hsgKorea),
    ],
    pattern: "同一制造商的日本站展示当地研发与销售，韩国站把设备、展厅和服务组合起来。国际站继续维护通用机型和多语目录，两个独立国家站各有当地团队。",
    path: "金属加工买家先按板材或管材、规格和加工目标核对机型，再联系各地工程团队，确认测试、交付和售后支持。",
    insight: "国家域名可以从本地展厅、工程服务或常用规格入手。按地区单独收集工件条件和交付地点，方便本地服务团队跟进。",
    boundary: "日本关系来源于上市申报披露，韩国关系来源于集团对当地业务的公告。部分德国与北美品牌入口由主域或经销商承担。",
    sources: [
      source("宏石激光上市申报文件", hsgFiling, "披露 HSG 工程为日本研发及销售公司。"),
      source("宏山韩国本地化业务公告", hsgKorea, "可核对韩国团队身份和釜山展厅。"),
    ],
  },
  {
    id: "snowman", industry: "industrial-compressors", name: "福建雪人集团", english: "Fujian Snowman Group", structure: "brands", lead: "technical",
    title: "工业制冷设备与欧洲压缩机品牌",
    summary: "雪人集团保留意大利压缩机品牌和瑞典技术站。意大利语采购可进入 SRMTec 工厂站查目录和应用。",
    sites: [
      site("https://www.snowman.group/en/product/screw_compressor.html", "全球", "英语、中文", "福建雪人集团", "工业制冷设备与系统", "集中展示螺杆压缩机等工程产品。", snowmanNews),
      local(".it", "https://www.srmtec.it/", "意大利及欧洲", "意大利语、英语", "SRMTec Italy", "意大利压缩机制造和选型", "用意大利语介绍压缩机、工厂与当地技术资料。", "https://www.srmtec.it/snowman-group/"),
      site("https://rotor.se/", "瑞典及全球", "英语", "Svenska Rotor Maskiner", "瑞典螺杆压缩研发与方案", "瑞典国家域覆盖压缩机技术业务，公开主入口以英语为主。", snowmanNews),
      site("https://www.refcomp.com/company/", "意大利及全球", "意大利语、英语", "RefComp", "压缩机品牌与技术资料", "独立品牌站提供公司和制冷压缩机专业资料。", "https://www.srmtec.it/en/srmtec-italy-en/"),
    ],
    pattern: "主站用于系统和集团能力，意大利业务站按型号和应用提供选型，瑞典研发主体展示技术方案。当地制造和旧品牌的专业内容可以沿用，集团入口负责说明关系。",
    path: "系统集成商根据工况、制冷量和安装条件确定候选产品，再找对应品牌和区域团队核对技术资料、配套及售后。",
    insight: "收购型站群可以保留品牌用户熟悉的规格和文件。当地语言页面把维保和技术支持放在选型附近。",
    boundary: "瑞典站使用 .se 后缀和英语正文，本次按瑞典业务站计入独立域。意大利站满足当地非英语语言与国家域同时出现。",
    sources: [
      source("雪人关于 RefComp 与瑞典 SRM 的公开说明", snowmanNews, "可核对两个欧洲制冷技术品牌的收购关系。"),
      source("SRMTec 意大利业务与前身", "https://www.srmtec.it/en/srmtec-italy-en/", "说明 RefComp 与意大利制造业务的沿革。"),
    ],
  },
  {
    id: "kaishan", industry: "industrial-compressors", name: "开山集团", english: "Kaishan", structure: "hybrid", lead: "technical",
    title: "空气压缩机的美国、澳洲和奥地利业务站",
    summary: "集团、美国和澳洲站按市场展示压缩设备，奥地利 LMF 保留德语产品、工程技术和售后支持。",
    sites: [
      site(kaishanProfile, "全球", "英语、中文", "开山集团股份有限公司", "集团与国际工程业务", "介绍空气压缩设备、制造研发和海外布局。", kaishanProfile),
      local(".at", "https://www.lmf.at/", "奥地利及德语市场", "德语、英语", "Leobersdorfer Maschinenfabrik（LMF）", "奥地利压缩机与工程", "德语首页、设备和联系保留了当地工程业务。", kaishanProfile),
      site("https://kaishanusa.com/", "美国", "英语", "Kaishan USA", "美国压缩空气设备及支持", "当地站围绕工业空压机和企业买家提供选型和支持。", kaishanProfile),
      site("https://www.kaishan.com.au/", "澳大利亚", "英语", "Kaishan Australia Pty Ltd", "澳洲空压机销售与维保", "以澳洲工况、设备系列和支持联系承接采购。", "https://www.kaishan.com.au/the-industrial-air-compressor-industry/"),
    ],
    pattern: "同一集团在英语工程市场按当地支持经营，收购的奥地利设备供应商保留 .at 和德语工程知识。国家域与业务语言相结合时能清楚解释谁交付、谁维护。",
    path: "工厂采购按照流量、压力和服务地点缩小设备范围，再请当地团队核对可交付配置、备件和维保窗口。",
    insight: "老品牌的规格、服务协议和维护渠道可以继续由当地团队维护。集团站放清楚各团队职责，帮助跨境买家找正确的报价主体。",
    boundary: "奥地利 LMF 的归属依据开山集团披露，澳洲站用当地子公司页面交叉核实。澳洲网站使用英语，保留为对照市场。",
    sources: [
      source("开山全球制造与奥地利 LMF 资料", kaishanProfile, "集团公开列出美国基地及所收购的奥地利设备公司。"),
      source("开山澳大利亚业务介绍", "https://www.kaishan.com.au/the-industrial-air-compressor-industry/", "说明澳洲地区主体与集团关系。"),
    ],
  },
];
