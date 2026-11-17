import { localWebsite as local, website as site } from "./network-schema.mjs";
import { source } from "./schema.mjs";

const nobleGroup = "https://www.nobleliftgroup.com/about/about.htm";
const nobleGermany = "https://www.noblelifteurope.com/index.asp?b_id=&k_id=32547&lng=en";
const savoyeGroup = "https://www.savoye.com/company/savoye-renforce-sa-dynamique-strategique-digitale-et-consolide-son-positionnement-technologique-au-sein-du-groupe-noblelift/";
const leoFactory = "https://www.leopump.com/en/pump-manufacturer.html";
const leoEurope = "https://leopump.eu/about-leo/";
const fuyaoReport = "https://www.fuyaogroup.com/upfiles/investor/202603/1774340758671.pdf";
const fuyaoHu = "https://www.fuyaogroup.hu/en/about/index.html";
const oppleEurope = "https://opple.co.in/en/news/opple-enters-european-market";
const goldwindReport = "https://www.goldwind.com/data/uploads/bdc_content2026/41232056875722360832.pdf";

export const countryIndustryNetworks = [
  {
    id: "noblelift", industry: "warehouse", name: "诺力股份", english: "Noblelift", structure: "hybrid", lead: "technical",
    title: "法国叉车国家站与法德仓储设备、系统集成",
    summary: "诺力当地站给搬运设备做选型，法国旗下 SAVOYE 承接更复杂的整仓系统工程。",
    sites: [
      site("https://www.nobleliftgroup.com/en/", "全球", "英语、中文", "诺力智能装备股份有限公司", "集团制造及物流业务", "按搬运装备和物流系统介绍产业与生产布局。", nobleGroup),
      local(".fr", "https://www.noblelift.fr/", "法国", "法语、英语", "Noblelift France", "叉车、高空作业平台和仓储设备", "法语目录与当地服务面向设备买家。", "https://www.noblelift.fr/fr/mentions-legales.aspx"),
      site("https://www.noblelifteurope.com/", "德国及欧洲", "德语、英语", "Noblelift Germany GmbH 区域业务", "欧洲搬运设备选型与销售", "用德语型号目录和售后入口承接区域采购。", nobleGermany),
      site("https://www.savoye.com/company/qui-sommes-nous/notre-histoire/", "法国及全球", "法语、英语", "SAVOYE", "自动化仓储系统与集成", "按分拣、拣选、物流软件与系统方案介绍项目业务。", savoyeGroup),
    ],
    pattern: "法国设备站承接叉车、平台等单品选型，SAVOYE 负责仓储系统和软件，欧洲站提供区域设备及联系。当地语言跟设备与项目场景一同维护。",
    path: "选叉车时优先考虑载重、提升高度、通道宽度及电源。仓储集成项目还要准备吞吐量、订单结构、楼层与软件接口，再交专业团队设计。",
    insight: "卖标准设备与卖工程方案时，采购资料颗粒度不同。有独立团队的项目业务可以不受设备目录结构限制。",
    boundary: "SAVOYE 与诺力的关系由双方公开资料交叉佐证。当地仅担任进口商或经销商的品牌入口留作渠道线索。",
    sources: [
      source("诺力集团与法国业务", nobleGroup, "披露旗下法国 SAVOYE 及海外销售、制造布局。"),
      source("SAVOYE 股东与业务关系公告", savoyeGroup, "列示 SAVOYE 对应的集团股东及系统业务。"),
    ],
  },
  {
    id: "leo", industry: "pumps", name: "利欧泵业", english: "LEO Pump", structure: "hybrid", lead: "channel",
    title: "工业水泵的泰语、印尼语国家域与配套渠道",
    summary: "出口站做工况、产品和项目资料，泰国与印尼公司各用当地后缀、语言、设备目录和联系经营。",
    sites: [
      site("https://www.leopump.com/en/", "全球", "英语、中文及多语种", "利欧泵业", "泵产品与工程选型", "按建筑、工业、市政和农业用途展示设备及适用案例。", leoFactory),
      site("https://leoglobal.com/about", "中国及全球", "中文、英语", "利欧集团股份有限公司", "集团业务与制造方向", "提供集团业务、企业沿革和泵业的制造板块说明。", "https://leoglobal.com/about"),
      local(".co.th", "https://www.leo.co.th/", "泰国", "泰语、英语", "LEO (Thailand) Co., Ltd", "当地水泵目录和渠道支持", "公开泰文水泵用途、活动、服务和询盘入口。", "https://en.leo.co.th/about"),
      local(".co.id", "https://leopumps.co.id/", "印度尼西亚", "印尼语", "PT LEO Pump Indonesia", "印尼水泵选型与分销", "印尼语站展示泵产品和经销资料，用当地公司承接咨询。", "https://leopumps.co.id/distributor"),
      site(leoEurope, "欧洲", "英语", "LEO Pump Europe", "欧洲供应与销售服务", "地区站介绍欧洲库配和工业产品能力。", leoEurope, "企业公开页面可读，本次测试环境曾遇直连超时。"),
    ],
    pattern: "泰文和印尼文站点分别承接采购、经销和当地服务。集团与全球泵业站继续承担制造历史及共用产品资料。",
    path: "目标买家从用途、流量、扬程和介质开始选设备，查当地渠道、配套条件和交付支持。",
    insight: "同类水泵可以保留同一套关键参数，各市场补充自己的叫法、使用场景、经销联系以及本地资料下载。",
    boundary: "泰国与印尼页面分别说明当地公司与集团关系。欧洲站的 .eu 域面向区域读者。",
    sources: [
      source("利欧泵业公司发展与海外设立", leoFactory, "集团材料列示泰国、印尼与其他海外业务。"),
      source("利欧印尼公司分销资料", "https://leopumps.co.id/distributor", "印尼公司页面说明股东关系与经销职责。"),
    ],
  },
  {
    id: "fuyao", industry: "auto-parts", name: "福耀玻璃", english: "Fuyao", structure: "hybrid", lead: "rfq",
    title: "汽车玻璃原厂配套、替换件渠道和匈牙利站",
    summary: "集团负责制造能力和客户覆盖，欧洲及匈牙利来接区域项目，替换件站用专门目录服务维修供应链。",
    sites: [
      site("https://www.fuyaogroup.com/en/about.html", "全球", "英语、中文", "福耀玻璃工业集团股份有限公司", "原厂配套与全球制造", "介绍汽车玻璃和零部件业务，提供集团工厂与采购信息。", "https://www.fuyaogroup.com/en/contact.html"),
      local(".hu", "https://www.fuyaogroup.hu/", "匈牙利及东欧", "匈牙利语、英语", "Fuyao Glass Eastern Europe Kft.", "东欧业务和当地制造", "匈牙利语站点公布当地企业与业务入口。", fuyaoHu),
      site("https://www.fuyaogroup.eu/unternehmen/", "德国及欧洲", "德语、英语", "Fuyao Europe GmbH", "欧洲汽车玻璃制造与客户项目", "德语站核对实际生产、研发、主体与区域联系。", "https://www.fuyaogroup.eu/impressum/"),
      site("https://fuyaousa.com/", "美国", "英语", "Fuyao Glass America Inc.", "北美制造、供应与分销", "向当地买家说明生产、产品和分销布局。", fuyaoReport),
      site("https://www.fygi.com/en/category/about.html", "全球", "英语", "福耀汽车替换玻璃业务（Fuyao ARG）", "售后替换玻璃销售", "独立按车型和替换用途服务维修企业、分销团队及采购。", "https://fygi.com/en/category/contact.html"),
    ],
    pattern: "同一企业分别服务整车配套、当地工厂和售后零件。匈牙利站和德国区域站提供当地语言。配套项目和替换件需要的型号、履约与支持信息采用不同目录。",
    path: "主机厂按车型平台、供货周期与工厂能力确定合作公司。维修和批发买家从替换件市场查车型、配置、当地库存和售后。",
    insight: "主机厂项目和后市场询盘进入不同团队时，可用独立产品站承接不同的型号与报价流程。集团导航说明当地工厂责任。",
    boundary: "匈牙利站配当地语言与国家域，德国团队使用欧洲区域域。企业归属以集团披露与当地法律声明为准。",
    sources: [
      source("福耀 2025 年年度报告", fuyaoReport, "可查海外制造主体与集团关系。"),
      source("福耀东欧公司介绍", fuyaoHu, "列示对应匈牙利企业。"),
    ],
  },
  {
    id: "opple", industry: "commercial-lighting", name: "欧普照明", english: "OPPLE Lighting", structure: "country", lead: "technical",
    title: "商用照明的西语、法语国家域与欧洲工程资料",
    summary: "欧普在欧洲用区域站和当地域呈现专业照明。西语及法语目录承接产品图纸、项目支持与当地联系。",
    sites: [
      site("https://www.opple.com/en", "全球", "英语及多语种", "欧普照明股份有限公司", "集团与商用照明业务", "全球站提供照明产品、项目和区域联系。", "https://www.opple.com/en/about-opple-lighting-mobile-version"),
      site("https://www.opple.eu/en", "欧洲", "英语及地区语言", "OPPLE Lighting B.V.", "欧洲工程照明与选型", "按建筑、办公、仓储等环境组织专业产品。", oppleEurope),
      local(".es", "https://www.opple.es/es", "西班牙", "西语", "OPPLE Lighting 欧洲业务（西班牙入口）", "西语商用照明与技术下载", "西语页面包含灯具目录、产品资料和联系。", "https://www.opple.es/es/terminos-de-uso"),
      local(".fr", "https://www.opple.fr/fr", "法国", "法语", "OPPLE Lighting 欧洲业务（法国入口）", "法语专业产品、项目及支持", "法语页面介绍室内外工程灯具和项目支持。", "https://www.opple.fr/fr/contact-0"),
    ],
    pattern: "西班牙和法国站与区域站使用可以并行的独立注册域，按当地语言提供相近的照明品类。产品文件的语言、服务窗口和当地保修资料随市场切换。",
    path: "工程买家按环境、安装条件、光效和防护等要求筛选，再获取技术文件，联系所在市场的项目支持。",
    insight: "欧普案例展示即使维护统一的产品规格，市场站仍可提供当地语言的下载、保修和联系方式。当地站的工程目录能帮助采购进到明确型号。",
    boundary: "本案例读取各域商用灯具与工程选型内容。区域域 .eu 计为独立网站，西班牙和法国后缀计为相应国家域。",
    sources: [
      source("欧普欧洲业务介绍", oppleEurope, "集团公开说明欧洲子公司的设立。"),
      source("欧普西班牙使用条款", "https://www.opple.es/es/terminos-de-uso", "核对主体验证和西语入口。"),
      source("欧普法国联系", "https://www.opple.fr/fr/contact-0", "法语当地采购和项目支持入口。"),
    ],
  },
  {
    id: "goldwind", industry: "wind-power", name: "金风科技", english: "Goldwind", structure: "hybrid", lead: "rfq",
    title: "整机、风场和德国风电控制业务分站",
    summary: "金风及美洲业务经营各自入口，德国 VENSYS 把整机和电气控制产品放到两个德语站点。",
    sites: [
      site("https://www.goldwind.com/en/about/", "全球", "英语、中文", "金风科技股份有限公司", "风电整机与工程方案", "公开风电设备、项目、运维和集团能力。", goldwindReport),
      site("https://www.goldwindamericas.com/", "美洲", "英语", "Goldwind Americas", "美洲风电项目", "地区公司站介绍商业项目、设备与当地业务联系。", "https://www.goldwindamericas.com/"),
      local(".de", "https://www.vensys.de/", "德国及欧洲", "德语、英语及多语种", "VENSYS Energy AG", "德国整机技术与运维", "德语整机资料按平台、机型、服务及项目组织。", "https://www.goldwind.com/cn/news/focus-922427606081730560/"),
      local(".de", "https://www.vensys-elektrotechnik.de/kontakt/", "德国及欧洲", "德语", "Vensys Elektrotechnik GmbH", "电力电子与控制配套", "电气工程专业站展示控制技术、工程和相关解决方案。", goldwindReport, "企业德语页面可查，本次测试环境直连曾超时。"),
    ],
    pattern: "集团和区域项目站按市场对接。德国团队保留原有品牌，整机站与电气系统站有独立产品、采购场景和联系人。",
    path: "风场开发方先核对机组平台、场地情况、并网与维护范围。采购电气或控制配套的制造商可直接进入专业企业站。",
    insight: "两家不同子公司在同一国家也可以经营两个网站。是否值得拆分，可从目录、交付对象和工程联系是否实质独立判断。",
    boundary: "两个德语 .de 域均面向德国业务，分别计为不同注册域。股权和主体以金风合并财务披露为根据。",
    sources: [
      source("金风合并财务报表附注", goldwindReport, "列示 VENSYS 及电气技术公司的集团关系。"),
      source("VENSYS 业务集团说明", "https://www.vensys.de/unternehmen/vensys-gruppe", "介绍德国技术开发与分工。"),
    ],
  },
];
