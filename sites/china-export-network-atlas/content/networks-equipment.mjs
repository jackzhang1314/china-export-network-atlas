import { website as site } from "./network-schema.mjs";
import { source } from "./schema.mjs";
import { sany } from "./network-sany.mjs";

const xcmgProfile = "https://www.xcmg.co/company-profile/";
const zoomlionReport = "https://en.zoomlion.com/upload/file/2025/06/04/c1314cd998734917b63520ae39e02955.pdf";
const liugongDirectory = "https://www.liugong.com/en/contact-us/";
const linglongDirectory = "https://en.linglong.cn/";
const hangchaDirectory = "https://www.hcforklift.com/contact/";

export const equipmentNetworks = [
  sany,
  {
    id: "xcmg", industry: "machinery", name: "徐工集团", english: "XCMG", structure: "country", lead: "rfq",
    title: "全球设备目录与各市场报价服务",
    summary: "全球站展示设备与集团能力，欧洲、美国、智利和印尼站把设备需求转成本地销售、经销或服务对接。",
    sites: [
      site("https://www.xcmg.com/", "中国及全球", "中文；有英文入口", "徐工集团", "集团与区域导航", "集团展示装备业务，并链接各地业务入口。", "https://www.xcmg.com/site/search.htm"),
      site("https://www.xcmg.co/", "全球", "英语", "徐工国际业务", "国际产品与品牌", "独立呈现装备目录、公司与国际业务资讯。", xcmgProfile),
      site("https://xcmg-europe.de/", "欧洲", "德语、英语", "XCMG Europe GmbH", "欧洲工程与集团业务", "展示欧洲公司、技术与集团在欧洲的业务能力。", "https://xcmg-europe.de/"),
      site("https://xcmg-usa.com/", "美国及北美", "英语", "XCMG 北美业务", "本地设备与经销", "组织当地在售机型和经销支持，可按北美市场浏览。", "https://www.xcmg.co/news/news-653/"),
      site("https://xcmg.cl/", "智利", "西语", "XCMG Chile S.A.", "智利选型与报价", "给挖掘机设置独立报价入口并提供当地销售联系。", "https://xcmg.cl/noticias/comunicado-xcmg-chile-s-a-representante-y-distribuidor-oficial/"),
      site("https://www.xcmg.co.id/id/", "印度尼西亚", "印尼语、英语", "PT XCMG Group Indonesia", "印尼产品与经销", "印尼语目录与当地经销信息同站，便于买家继续查找。", "https://www.xcmg.co.id/about/aboutxcmg.htm"),
    ],
    pattern: "集团与国际站分别解释企业能力与设备目录，国家站以当地销售和售后衔接设备需求。智利站的挖掘机报价页、美国站的经销网络和印尼语渠道页承担不同的采购下一步。",
    path: "智利项目采购可先在当地机器目录筛吨位和工况，再从挖掘机报价入口联系采购。同类买家进入北美站时，可以从设备型号找到附近的经销服务。",
    insight: "按市场保留交付地、设备规格和售后供应差异。当地站的询价表可预选型号，让销售收到能直接跟进的需求。",
    boundary: "保留页面可以定位到集团、当地经营主体或官方交叉入口的独立域。由当地合作伙伴经营的品牌官网需要另行核对。",
    sources: [
      source("徐工集团站点导航", "https://www.xcmg.com/site/search.htm", "关联集团与多地区入口。"),
      source("徐工国际业务简介", xcmgProfile, "列示集团与国际业务组织。"),
    ],
  },
  {
    id: "zoomlion", industry: "machinery", name: "中联重科", english: "Zoomlion", structure: "hybrid", lead: "channel",
    title: "国家销售服务站与混凝土、高空作业品牌站",
    summary: "巴西、澳新和土耳其承接区域设备业务。CIFA 和 Zoomlion Access 独立展示专业目录。",
    sites: [
      site("https://en.zoomlion.com/", "全球", "英语；其他语言按站内切换", "中联重科股份有限公司", "全球设备与服务", "按产品线展示设备，通过服务网络定位市场。", "https://en.zoomlion.com/service/service_network.htm"),
      site("https://www.zoomlion.com.tr/", "土耳其", "土耳其语", "Zoomlion Cifa Makine", "当地销售与服务", "把在售装备、当地联系与维修支持放在土语站。", "https://www.zoomlion.com.tr/servisler/servis-agi"),
      site("https://www.zoomlion.com.br/", "巴西", "巴西葡语", "Zoomlion Brasil Indústria", "巴西销售和渠道", "葡语设备目录附当地联系。", zoomlionReport),
      site("https://zoomlion.au/", "澳大利亚、新西兰", "英语", "Zoomlion Australia-New Zealand", "澳新设备与渠道", "区域入口组织机型及当地经销和支持。", zoomlionReport),
      site("https://www.cifa.com/", "全球（意大利业务）", "英语、意大利语等", "CIFA S.p.A.", "混凝土机械品牌", "围绕泵送、运输和喷射设备呈现专业型号与服务。", "https://eu.zoomlion.com/about-us/"),
      site("https://global.zoomlion-access.com/en/cooperation/cooperation-reference.htm", "全球", "英语", "中联重科高空作业机械业务", "高空作业产品线", "独立品牌站展示高空作业平台和合作应用。", "https://global.zoomlion-access.com/en/cooperation/cooperation-reference.htm"),
    ],
    pattern: "母站覆盖大类，区域公司的域名按当地经销和售后运营，专业品牌站处理选型和应用资料。欧洲集团入口与全球站在同一注册域。",
    path: "在当地找交付或维修时，从区域站定位支持团队。需要核对混凝土泵或高空作业平台的型号时，直接查独立产品目录和适用工况。",
    insight: "设备产品差异足以形成独立选型流程时，可给专业业务独立目录。区域销售和技术团队的咨询入口应写清责任。",
    boundary: "本页按独立注册域计数。地区办事处、外部网点和欧洲子域仍然可以提供采购信息。",
    sources: [
      source("中联重科服务网络", "https://en.zoomlion.com/service/service_network.htm", "展示区域联系和集团的服务网络。"),
      source("中联重科上市公司通函", zoomlionReport, "可查部分区域主体在集团内的关系。"),
    ],
  },
  {
    id: "liugong", industry: "machinery", name: "柳工", english: "LiuGong", structure: "country", lead: "channel",
    title: "全球工况目录与区域整机、经销和售后",
    summary: "集团直接公布欧洲、巴西和俄罗斯团队，使区域站的实际业务身份可以交叉核对。",
    sites: [
      site("https://www.liugong.com/en/", "全球", "英语及多语种", "广西柳工机械股份有限公司", "全球设备与行业应用", "按设备类别和行业查找产品，国际销售和渠道有独立联系人。", liugongDirectory),
      site("https://liugong.eu/en/", "欧洲", "英语及欧洲语言", "LiuGong Europe", "欧洲产品、经销与售后", "集中发布欧洲设备、经销和本地服务。", liugongDirectory),
      site("https://liugongla.com/", "拉美（巴西）", "巴西葡语", "LiuGong Machinery Latin America, LTDA", "拉美设备与交付", "巴葡产品及行业应用配当地联系。", liugongDirectory),
      site("https://liugongrussia.ru/", "俄罗斯", "俄语", "LiuGong Machinery Rus, LLC", "俄语设备与当地服务", "面向区域买家组织俄语设备与经销服务。", liugongDirectory),
    ],
    pattern: "国家或区域团队承担设备报价、经销和售后，全球站集中讲清产品系列和多地区业务。总部公布的主体与区域网站名称、联络方式可以互核。",
    path: "拉美买家能在巴葡站找设备和当地联系。欧洲和俄罗斯渠道商先核对区域机型，再就经销或零件支持对接当地团队。",
    insight: "总部留一张归属明确、经常更新的地区导航。各区域站沿用可识别的设备名称，并提供自己的型号、经销和备件入口。",
    boundary: "按集团公开地区名单与可读页面收录。即使主页有授权品牌，经销商自有网站也属于该经销商。",
    sources: [source("柳工全球联系目录", liugongDirectory, "列出欧洲、拉美和俄罗斯业务主体与当地联系。")],
  },
  {
    id: "hangcha", industry: "machinery", name: "杭叉集团", english: "Hangcha", structure: "hybrid", lead: "channel",
    title: "叉车区域销售、租赁、维修与自动化项目",
    summary: "杭叉从全球站直接链接当地企业。区域站保留当地型号、经销和售后，北美自动化团队以独立域接工程项目。",
    sites: [
      site("https://www.hcforklift.com/", "全球", "英语及多语种", "杭叉集团股份有限公司", "集团叉车与仓储设备", "放置各类叉车、物流设备选型及全球地区入口。", hangchaDirectory),
      site("https://www.hangchaeurope.com/", "德国及欧洲", "英语、德语等", "Hangcha Europe GmbH", "欧洲设备及零件支持", "欧洲团队对接型号、供应、备件和服务。", "https://www.hangchaeurope.com/hangcha/company"),
      site("https://www.hcforkliftamerica.com/", "美国", "英语", "HC Forklift America Corporation", "美国经销与设备选型", "当地设备、展会、经销与服务面向美国买家。", "https://www.hcforkliftamerica.com/new-introductions/"),
      site("https://www.hcforkliftcanada.com/", "加拿大", "英语、法语", "Hangcha Forklift Canada Inc.", "加拿大设备与渠道", "提供本地设备、经销、售后与法语入口。", hangchaDirectory),
      site("https://www.hcforkliftmexico.com/", "墨西哥", "西语", "Hangcha Forklift Mexico", "墨西哥叉车目录", "按当地设备和业务窗口承接西语采购。", hangchaDirectory),
      site("https://www.hangchabrasil.com/", "巴西", "巴西葡语", "Hangcha Brasil Ltda.", "巴西选型与本地销售", "当地产品和联系在巴葡站提供。", hangchaDirectory),
      site("https://hcrs.fr/", "法国", "法语", "Hangcha Europe Rental & Sales", "法国设备、租赁和服务", "在法国市场并列展示叉车、租赁和服务。", "https://www.hangchaeurope.com/news/news_read/135"),
      site("https://www.hcforkliftnetherlands.com/", "荷兰", "荷兰语", "Hangcha Netherlands B.V.", "荷兰地区设备服务", "使用本地语言展示产品、支持和联系。", hangchaDirectory),
      site("https://hangchaaustralia.com.au/", "澳大利亚", "英语", "HC Forklift Australia Pty Ltd", "澳洲销售与经销", "按设备与业务需求展示产品、当地网点及咨询。", hangchaDirectory),
      site("https://hangchajp.com/", "日本", "日语", "HANGCHA JAPAN株式会社", "日本设备和项目支持", "公司、产品和行业资料有日语版本及当地联系。", hangchaDirectory),
      site("https://www.hangchaforklift-id.com/", "印度尼西亚", "印尼语、英语", "杭叉印度尼西亚业务", "当地设备与支持", "展示电动、内燃叉车和当地联系。", hangchaDirectory),
      site("https://www.hcforkliftmy.com/", "马来西亚", "英语", "杭叉马来西亚业务", "马来西亚叉车销售", "独立地区目录提供采购与本地联系。", hangchaDirectory),
      site("https://www.hangcha-middleeast.com/", "中东", "英语", "Hangcha Middle East General Trading FZE", "区域叉车与运营支持", "按品类组织中东站产品，便于联系当地业务团队。", hangchaDirectory),
      site("https://www.hcforkliftvietnam.com/", "越南", "越南语及英语入口", "Công ty TNHH Xe Nâng Hangcha Việt Nam", "越南设备与本地联系", "站点展示当地产品和联系，集团目录列出对应主体。", hangchaDirectory),
      site("https://www.haslagv.com/", "北美", "英语", "Hangcha America Smart Logistics", "自动化仓储工程", "围绕 AGV、仓储流程和系统工程组织采购资料。", "https://de.hangchaeurope.com/news/news_read/147"),
    ],
    pattern: "全球站按叉车和物流设备筛选，各地区站负责当地型号、经销、配件和租赁。北美自动化站面对的是整套仓储流程和集成，与一般叉车选型的工作不同。",
    path: "车队或仓库采购可按吨位、门架、电池和当地网点筛设备。仓储自动化项目再按托盘、场地和软件接口与专业团队沟通。",
    insight: "在集团导航链接实际运营团队。地区站维护本地型号、服务承诺和备件供货。自动化项目的咨询入口可先收集作业流、负荷与接口。",
    boundary: "集团导航列出的可用公开业务站才进入清单。只剩域名停放页的入口和服务登录页均未计入。",
    sources: [
      source("杭叉全球导航与联系方式", hangchaDirectory, "集团目录分别列有地区站与当地经营主体。"),
      source("杭叉欧洲子公司介绍", "https://www.hangchaeurope.com/hangcha/company", "说明欧洲团队的子公司身份和服务职责。"),
    ],
  },
  {
    id: "yutong", industry: "vehicles", name: "宇通客车", english: "Yutong", structure: "hybrid", lead: "rfq",
    title: "客车全球目录、欧洲项目站和法国实体",
    summary: "集团国际入口介绍宇通业务，客车站提供车型。欧洲和法国分别承担区域项目与当地联系。",
    sites: [
      site("https://en.yutong.com/", "全球", "英语及多语种", "宇通客车股份有限公司", "客车产品与使用场景", "按公交、旅行及不同用途查看车型、项目与服务。", "https://en.yutong.com/"),
      site("https://www.yutong.global/", "全球", "英语", "宇通集团国际业务", "集团全球业务入口", "集团业务与各产品线总入口，提供企业层面的资料。", "https://www.yutong.global/"),
      site("https://www.yutongeurope.com/", "欧洲", "英语及欧洲语言", "宇通客车股份有限公司", "欧洲车型与项目对接", "以欧洲市场的可售车型、案例与联系组织采购。", "https://www.yutongeurope.com/privacy/"),
      site("https://www.yutong.fr/", "法国", "法语", "YUTONG FRANCE SAS", "法国销售与合作", "法语车型与当地联系配合公交和车队项目。", "https://www.yutong.fr/contact/"),
    ],
    pattern: "集团站覆盖多个宇通业务，客车专业站面向车辆选型，欧洲与法国各有自己的车型和项目支持。较大的采购标的需要区域现场团队参与。",
    path: "公交或旅游车采购可以先按载客、路况和电动化需求选车型，再咨询当地的车型配置、交车和维护，法国客户可直接使用法语联系页。",
    insight: "车型参数与服务信息同时本地化。工厂若已有签约、备件和技术团队，可用国家站展示实际交付案例与负责人。",
    boundary: "法国站由该市场的宇通业务运营，归属可在集团披露查找。海外进口商的自有域与宇通同域的语言版不计。",
    sources: [
      source("宇通欧洲站隐私声明", "https://www.yutongeurope.com/privacy/", "标明宇通客车股份有限公司。"),
      source("宇通集团公开财务报告", "https://www.yutong.global/static/res/2025/9/25/audit-report/1971049565016690688.pdf", "可查 YUTONG FRANCE SAS 等企业的集团关系。"),
    ],
  },
  {
    id: "linglong", industry: "tires", name: "玲珑轮胎", english: "Linglong Tire", structure: "hybrid", lead: "channel",
    title: "集团、海外与德国渠道，加上特种胎出口目录",
    summary: "集团页给商用车轮胎做工况选型，德国站组织近场经销，特种胎站为矿山和工程采购单列型号。",
    sites: [
      site(linglongDirectory, "全球", "英语；另有中文入口", "山东玲珑轮胎股份有限公司", "集团目录与经销导航", "按载重、尺寸、工况或区域查轮胎与经销。", linglongDirectory),
      site("https://www.linglongtire.com/en/global/index.html", "全球及北美", "英语及多语种", "山东玲珑轮胎股份有限公司", "海外产品与服务目录", "提供乘用及卡客车产品、资料下载、服务与北美入口。", linglongDirectory),
      site("https://www.linglong.de/", "德国", "德语、英语", "Linglong Germany GmbH", "德国产品与渠道", "德国团队的联系与法律主体可在站内核对。", "https://www.linglong.de/impressum"),
      site("https://www.linglongotr.com/", "全球", "英语及多语种", "玲珑特种轮胎业务", "工程、矿山和农业特种胎", "按工况、尺寸和轮胎结构查目录并询价。", linglongDirectory),
    ],
    pattern: "同一母品牌可同时组织区域渠道和专业胎型。面向工程车辆的采购需要特种胎规格，类别、尺寸和工况与常规乘用车目录不同。",
    path: "矿山车队先在 OTR 站确认胎型、规格和适用系列，再发出选型需求。欧洲渠道采购根据当地供应和责任主体联系区域团队。",
    insight: "从规格和用途建立可复用目录。地区站保留经销、适配和质保信息，专业线用详尽工况说明提高询盘可用性。",
    boundary: "集团页链接多个外部入口，只有页面可核、在独立注册域有实际业务内容的入口纳入本次清单。",
    sources: [
      source("玲珑轮胎全球站及页尾链接", linglongDirectory, "集团页可核实美洲及特种轮胎入口。"),
      source("玲珑德国法律声明", "https://www.linglong.de/impressum", "列示负责当地站的企业。"),
    ],
  },
  {
    id: "sailun", industry: "tires", name: "赛轮集团", english: "Sailun Group", structure: "hybrid", lead: "channel",
    title: "区域销售站与工业轮胎品牌",
    summary: "集团站连接全球布局，美国与欧洲站提供当地产品和渠道，MAXAM 服务工程、矿业和工业设备。",
    sites: [
      site("https://en.sailungroup.com/about/global.html", "全球", "英语；另有中文入口", "赛轮集团股份有限公司", "海外布局和制造业务", "全球布局说明生产与海外业务，方便识别区域团队。", "https://en.sailungroup.com/investor/index.html"),
      site("https://sailuntireusa.com/en-us/", "美国", "英语", "Sailun Tire USA", "美国轮胎和经销渠道", "提供当地产品与门店入口，并展示商用车型用途。", "https://en.sailungroup.com/investor/index.html"),
      site("https://www.sailun-tyres.eu/", "欧洲", "英语、德语等", "Sailun Europe GmbH", "欧洲产品和技术资料", "欧洲规格、产品标签、营销及销售支持按当地需求组织。", "https://www.sailun-tyres.eu/media/pm-sailun-reifenpartner-fia-de.pdf"),
      site("https://maxamtire.com/", "全球", "英语等", "MAXAM Tire（赛轮集团子公司）", "工业和工程轮胎", "用矿业、工地和工业设备等场景组织规格及渠道。", "https://maxamtire.com/sustainability/", "本轮直连受限，可核对企业公开页面与归属依据。"),
    ],
    pattern: "常规轮胎按销售市场展示，本地车型和经销入口有独立配置。专业品牌的目标买家是工业车队、工程项目和设备服务商，规格和内容单独维护。",
    path: "轮胎经销商可查当地站的系列、尺寸、资料及供货渠道。矿山或物料搬运项目在 MAXAM 按用途缩小候选，再与业务团队讨论负荷与工况。",
    insight: "先把技术参数按产品统一，再让当地渠道站对接库存、标签和承诺。同类品牌的分站可以集中展现不同工况的材料与服务。",
    boundary: "样本展示制造集团自有业务入口，消费端门店查询作为当地销售环节存在。网站数量按注册域计算。",
    sources: [
      source("赛轮投资者资料", "https://en.sailungroup.com/investor/index.html", "从集团公开资料核对美国业务。"),
      source("MAXAM 可持续发展与归属", "https://maxamtire.com/sustainability/", "页面说明 MAXAM Tire 为赛轮集团子公司。"),
    ],
  },
];
