import { localWebsite as local, website as site } from "./network-schema.mjs";
import { source } from "./schema.mjs";

const chintSolar = "https://energy.chint.com/en/about/index.html";
const chintDirectory = "https://www.chintglobal.com/global/en/about-us/about-chint/global-operation-localization.html";
const jinkoStorage = "https://jinkosolar.eu/energy-storage/";
const steelStatement = "https://www.tssgroup.com.cn/en/official-statement-on-illegal-impersonation-of-tsingshan-industrys-website/";
const cimcEnric = "https://en.enricgroup.com/about";
const clivetRelation = "https://hvac.midea.com/about_mbt/";
const boeDirectory = "https://www.boe.com/en/about/BOEGlobal";
const jeBrands = "https://www.jegroupintl.com/brands/";
const chintFiling = "https://static.cninfo.com.cn/finalpage/2026-08-20/1225481499.PDF";

export const manufacturingNetworks = [
  {
    id: "lenovo", industry: "computing", name: "联想集团", english: "Lenovo", structure: "brands", lead: "technical",
    title: "数据中心卖方、渠道门户、制造工厂与 IT 方案团队",
    summary: "同一集团把服务器选型、渠道合作、制造能力和企业技术服务放到各自运营的网站。",
    sites: [
      site("https://www.lenovo.com/us/en/servers-storage/", "全球（此处为美国入口）", "英语及地区语言", "联想集团", "服务器、存储与基础设施采购", "公开企业计算、服务器、存储和数据中心解决方案。", "https://www.lenovo.com/us/en/servers-storage/", "本轮直连受限，可核对企业公开页面与归属依据。"),
      site("https://www.lenovopartnerhub.com/web/lenovo-global-site/channelfirst", "全球", "英语及地区语言", "联想渠道业务", "经销商与合作伙伴", "公开介绍数据中心及设备的伙伴计划，为渠道商提供申请入口。", "https://www.lenovopartnerhub.com/web/lenovo-global-site/channelfirst"),
      site("https://www.lcfc.com/company-details", "中国合肥及全球制造", "中文；有英语入口", "联宝（合肥）电子科技有限公司", "计算机制造与工厂能力", "制造公司独立介绍企业、制造和技术能力。", "https://investor.lenovo.com/en/publications/reports/ar_1718.pdf"),
      site("https://www.lpstech.com/site/en/about-us/company-overview", "亚太", "英语及地区语言", "Lenovo PCCW Solutions", "企业 IT 与系统集成", "按行业、工程、数字化和应用交付组织企业解决方案。", "https://www.lpstech.com/site/en/story/transforming-operational-excellence-post-acquisition"),
    ],
    pattern: "产品网站把型号和方案交给终端企业客户，伙伴站负责渠道合作，制造站展示生产与工程能力，IT 方案团队对接企业需求和交付。四个站按在采购过程中的角色分工。",
    path: "系统集成商先在服务器站对照计算、存储和网络要求，再从合作伙伴门户了解渠道条件。需要企业级项目实施时，可按在地服务范围联系解决方案团队。",
    insight: "将型号选型、渠道政策、工厂证据和集成服务分别维护。公开内容说明买家下一步要提交的数量、配置和实施地点。",
    boundary: "服务器、存储和制造对应计算机业务，渠道和 IT 方案是相邻业务。仅统计有公开 B2B 内容和集团关系出处的独立域。",
    sources: [
      source("联想集团与电讯盈科的企业 IT 合作披露", "https://news.lenovo.com/pressroom/press-releases/lenovo-and-pccw-partnership/", "联想官方说明与 LPS 的交易与业务背景。"),
      source("联想年度报告中的联宝公司资料", "https://investor.lenovo.com/en/publications/reports/ar_1718.pdf", "联想披露联宝为集团子公司。"),
    ],
  },
  {
    id: "jinko", industry: "energy", name: "晶科能源", english: "JinkoSolar", structure: "hybrid", lead: "technical",
    title: "集团光伏站、欧美销售站与储能产品线",
    summary: "同品牌按组件市场与储能业务拆分。欧洲和美国页面承载当地销售、技术文件与项目支持。",
    sites: [
      site("https://www.jinkosolar.com/en/site/aboutus", "全球", "英语；另有中文站内入口", "晶科能源集团", "集团及光伏产品", "集团介绍、全球产品系列和研发制造信息集中维护。", "https://www.jinkosolar.com/en/site/aboutus"),
      site("https://jinkosolar.eu/", "欧洲", "英语及欧洲语言", "JinkoSolar 欧洲业务", "欧洲光伏销售与支持", "按欧洲市场提供组件资料、案例与联系。", "https://jinkosolar.eu/imprint/", "本轮直连受限，可核对企业公开页面与归属依据。"),
      site("https://jinkosolar.us/about-jinko/", "美国", "英语", "JinkoSolar (U.S.) Inc.", "美国光伏产品与服务", "发布面向美国市场的型号和当地团队资料。", "https://jinkosolar.us/legal-statement/"),
      site("https://www.jinkoess.com/en/", "全球", "英语；另有中文站内入口", "晶科储能业务", "全球储能产品与项目", "按储能系统和应用展示产品规格及项目。", jinkoStorage),
      site("https://jinkoess.eu/", "欧洲", "英语", "Jinko ESS 欧洲业务", "欧洲储能选型和资料", "提供储能系统与下载入口，面向当地工程和采购团队。", jinkoStorage),
    ],
    pattern: "组件对比依赖功率、技术路线和市场文件，储能采购还要确认容量、并网条件、系统配置和服务，业务站分别组织资料。同一品牌保留全球与地区两级的入口。",
    path: "欧洲安装商可从组件站下载当地资料，储能集成商可进 ESS 站按系统和容量查资料，再同技术团队核对项目要求。",
    insight: "先按产品与项目流程划分询盘，再按市场管理文件和技术支持。区域站可以写出不同的交期、文件版本和维护窗口。",
    boundary: "晶科储能是光伏组件的相邻业务，纳入公司站群结构。储能站的存在不代表行业出口额包含储能产品。",
    sources: [
      source("晶科欧洲储能入口", jinkoStorage, "欧洲光伏站说明储能业务及其入口。"),
      source("晶科欧洲站法律信息", "https://jinkosolar.eu/imprint/", "可查欧洲站经营信息。"),
    ],
  },
  {
    id: "chint", industry: "energy", name: "正泰集团", english: "CHINT", structure: "hybrid", lead: "rfq",
    title: "光伏和工业配电业务分站与 NOARK 中东欧五国站",
    summary: "正泰按电站、组件、逆变器和配电分站，旗下 NOARK 在中东欧经营当地语言和国家域名相结合的低压电气网站。",
    sites: [
      site("https://energy.chint.com/en", "全球", "英语、中文", "正泰新能源（CHINT Solar）", "新能源项目开发", "介绍电站投资、工程与运营，按项目需求对接。", chintSolar),
      site("https://www.chintglobal.com/global/en/home.html", "全球", "英语及地区语言", "CHINT Global", "工业电气与全球销售", "按配电、工业控制和解决方案等展示产品与当地运营。", chintDirectory),
      site("https://www.astronergy.com/about-astronergy/", "全球", "英语及多语种", "正泰新能（Astronergy）", "光伏电池与组件", "组件系列、产品参数及项目案例面向采购与安装。", "https://www.astronergy.com/terms-of-use/"),
      site("https://en.chintpower.com/about/", "全球", "英语；另有中文站内入口", "正泰电源（CHINT Power）", "逆变器及储能", "按逆变器、储能系统和应用提供设备选型。", "https://en.chintpower.com/about/"),
      site("https://www.chint.eu/es/empresa/chint-global/", "西班牙", "西语", "CHINT Electrics S.L.", "当地配电产品与技术支持", "西语目录和支持联系对接当地项目与经销。", chintDirectory),
      local(".pl", "https://noark-electric.pl/pl", "波兰", "波兰语", "NOARK Electric Sp. z o.o. 区域业务", "波兰低压电气与销售网络", "用波兰语提供断路器、配电产品及经销网络。", "https://noark-electric.pl/pl/o-nas"),
      local(".cz", "https://noark-electric.cz/cz", "捷克", "捷克语", "NOARK Electric Europe s.r.o.", "捷克技术支持与配电选型", "捷克语支持页发布办公室、仓储及区域联系。", "https://noark-electric.cz/cz/terms-and-conditions"),
      local(".ro", "https://noark-electric.ro/ro", "罗马尼亚", "罗马尼亚语", "NOARK Electric 罗马尼亚业务", "当地配电与经销资料", "罗马尼亚语目录和经销清单帮助采购找到供货渠道。", "https://noark-electric.ro/ro/terms-and-conditions"),
      local(".sk", "https://noark-electric.sk/sk", "斯洛伐克", "斯洛伐克语", "NOARK Electric Europe 斯洛伐克站", "当地配电目录与渠道", "斯洛伐克语站提供产品、技术支持和当地销售资料。", "https://noark-electric.sk/sk/podpora"),
      local(".hu", "https://noark-electric.hu/hu", "匈牙利", "匈牙利语", "NOARK Electric Europe 匈牙利站", "匈牙利配电产品与文件", "匈牙利语提供产品目录及技术资料。", "https://noark-electric.hu/hu/dokumentumok-es-szoftver"),
    ],
    pattern: "集团按业务分工拆开项目、组件和逆变器。NOARK 的中东欧五站沿用低压电气产品体系，各自提供当地语言、技术资料与分销联系。一个品牌、相似的产品模板和多个独立国家域可以同时存在。",
    path: "采购先确定需求是电站、组件还是低压配电。当地安装商和经销商可进对应的 NOARK 国家站核对型号、说明和销售渠道。",
    insight: "同一产品体系可以复用型号资料。国家站维护当地语言、可供货范围、售后和经销窗口。地区团队是否足以维护这些差异，可以作为是否分域的判断依据。",
    boundary: "NOARK 按集团财务披露和当地站的经营与支持页面核对。正泰光伏与低压电气的分站用于比较集团运营，行业统计保留原商品范围。",
    sources: [
      source("正泰新能源集团介绍", chintSolar, "可核新能源业务与集团关系。"),
      source("正泰全球本地运营目录", chintDirectory, "列有西班牙等地经营主体及当地站点。"),
      source("正泰电器 2026 年半年度报告", chintFiling, "查正泰电器与 NOARK 相关企业关系。"),
      source("NOARK 欧洲地区支持", "https://noark-electric.cz/cz/podpora", "展示捷克、波兰、罗马尼亚等当地支持主体。"),
    ],
  },
  {
    id: "yuto", industry: "packaging", name: "裕同科技", english: "YUTO", structure: "hybrid", lead: "sample",
    title: "集团制造能力、澳洲销售、环保材料与欧洲工厂",
    summary: "不同站点分别处理跨国订单、区域联系、植物纤维包装试样和当地印刷交付。",
    sites: [
      site("https://www.szyuto.com/", "全球", "英语、中文", "深圳市裕同包装科技股份有限公司", "集团包装与制造", "提供包装服务、行业应用、全球制造和联系入口。", "https://www.szyuto.com/"),
      site("https://yuto.com.au/", "澳大利亚", "英语", "YUTO Australia Pty. Ltd.", "澳洲包装项目对接", "澳洲市场独立介绍包装能力及联系，支持当地沟通。", "https://yuto.com.au/about-us/Global%20Footprint/"),
      site("https://www.yutoeco.com/", "全球", "英语及多语种", "裕同环保包装业务（YUTOECO）", "植物纤维与环保包装", "以材料、应用和包装产品组织选型，适合样品与定制。", "https://www.yutoeco.com/association_nc10"),
      local(".hu", "https://gelberteco.hu/", "匈牙利及欧洲", "匈牙利语、英语", "Gelbert ECO Print Kft.", "当地印刷包装工厂", "工厂独立发布印刷、包装业务和地区联系。", "https://www.szyuto.com/newsdetail/9881"),
    ],
    pattern: "总部面向跨国品牌讲包装能力，澳洲团队提供区域联系，环保专站围绕材料与样品，欧洲工厂保留本地生产与印刷业务。四站都有独自可用的页面内容。",
    path: "品牌采购先按产品应用和交付地识别合适站点。环保包装项目准备尺寸、材料要求、数量、样品和时间后，可与专线沟通；欧洲印刷项目可找工厂核实交期。",
    insight: "集团、工厂和销售团队需要共享产品材料规格，分别明确报价、打样、量产及交货的负责人。专线页适合展示可定制属性和样品信息。",
    boundary: "此案例覆盖纸品、植物纤维等相邻包装做法。国家统计局的塑料制品出口数据按商品口径单列。",
    sources: [
      source("裕同可持续产品", "https://www.szyuto.com/sustainability/sustainable_product", "集团披露环保包装方向。"),
      source("裕同发布匈牙利印刷厂股权交易", "https://www.szyuto.com/newsdetail/9881", "集团资料说明与 Gelbert ECO Print 的股权关系。"),
    ],
  },
  {
    id: "tsingshan", industry: "steel", name: "青山实业", english: "Tsingshan", structure: "brands", lead: "rfq",
    title: "不锈钢集团、制造厂与海外园区",
    summary: "四个域名可以从集团公告逐一对照。英文集团站负责企业与国际业务资料，青拓、永青和上海鼎信各自展示生产、销售或海外布局。",
    sites: [
      site("https://www.tssgroup.com.cn/en/", "全球", "英语、中文", "青山控股集团有限公司", "不锈钢与国际联系", "提供全球业务、企业资料和联系窗口。", steelStatement),
      site("https://www.tsingtuo.com/", "中国工厂与采购", "中文", "青拓集团有限公司", "生产、产品手册与销售", "提供制造、产品手册、资质和销售中心。", steelStatement),
      site("https://www.etsingshan.com/Col/Col7/Index.aspx", "中国与印度尼西亚", "中文", "永青集团有限公司", "海外产业园与制造信息", "展示不锈钢材料及印尼项目的产业配套。", steelStatement),
      site("https://decent-china.com/", "中国与印度尼西亚", "中文；另有英语入口", "上海鼎信投资（集团）有限公司", "跨国项目与生产基地", "保留上海鼎信与印尼项目的集团、园区和联系资料。", steelStatement),
    ],
    pattern: "以企业角色划分网站。集团英文站是对外入口，钢材品类、手册和销售留在制造公司，跨国园区披露和联系放在运营主体的网站。",
    path: "采购商可先核对材料牌号、产品记录和销售主体，再确认对应基地、数量、交货地和质量文件。跨国项目资料可从永青与上海鼎信继续查找。",
    insight: "大宗材料交易需要能查到发货地点、质量规格和合同主体。集团直接公布真实域名，可以为不同主体的采购沟通提供归属依据。",
    boundary: "部分站点以中文为主，承担集团供应链或生产展示。集团公告列出的四个域名是本页归属证据。",
    sources: [
      source("青山实业官方域名公告", steelStatement, "集团逐一公开四个官方网站及经营主体。"),
      source("青山集团全球业务入口", "https://www.tssgroup.com.cn/en/", "英文集团站汇总不锈钢与国际业务。"),
    ],
  },
  {
    id: "cimc", industry: "containers", name: "中集集团", english: "CIMC", structure: "brands", lead: "rfq",
    title: "集团入口、特种箱工厂与罐箱业务",
    summary: "买家在集团看业务范围，在工厂和专线站核对特种箱、罐箱和运输设备的接口、尺寸及工程要求。",
    sites: [
      site("https://www.cimc.com/en/index.php?a=show&c=index&catid=36&id=1&m=content", "全球", "英语、中文", "中国国际海运集装箱（集团）股份有限公司", "集团业务与制造布局", "集团入口解释集装箱、能源装备等业务及专业制造。", "https://www.cimc.com/en/index.php?a=show&c=index&catid=36&id=1&m=content"),
      site("https://www.cimcnt.com/?lang=en", "全球", "英语、中文", "南通中集特种运输设备制造有限公司", "特种箱工厂", "发布特种运输和定制设备信息，区分生产与应用。", "https://www.cimcnt.com/?lang=en"),
      site("https://www.cimctank.com/", "全球", "中文；有英语入口", "中集安瑞环科技股份有限公司（CIMC Safeway）", "罐箱型号与工程支持", "以罐式集装箱为独立目录，公开企业联系方式。", cimcEnric),
      site("https://en.enricgroup.com/", "全球", "英语、中文", "中集安瑞科控股有限公司", "能源化工运输及储运装备", "提供液体散货、能源装备和工程方案等业务资料。", cimcEnric),
    ],
    pattern: "站点分工依据箱型、用途与工程能力。集团站解释装备制造板块，工厂和专业公司的人群更具体，可以对应罐体、配件和使用条件。",
    path: "项目采购按箱型、介质、接口、数量和使用地查工厂或罐箱品牌，再向对应团队咨询设计与交付。",
    insight: "产品详情明确标准、接口和适配。复杂特种箱的询价流程应引导买家先准备介质、用量、工况和交付地。",
    boundary: "集团、工厂与上市业务主体以原始企业页面为准。能源工程设备站用于观察罐箱和储运的业务衔接。",
    sources: [source("中集安瑞科公司资料与收购沿革", cimcEnric, "说明加入中集集团的历史以及安瑞环等企业关系。")],
  },
  {
    id: "boe-varitronix", industry: "components", name: "京东方", english: "BOE", structure: "hybrid", lead: "technical",
    title: "显示集团、车载显示专业团队与日本业务",
    summary: "全球集团及不同工程主体经营独立站，分别服务显示器件、车载显示项目、日本客户和 LED 芯片。",
    sites: [
      site("https://www.boe.com/global/en/about.html", "全球", "英语、中文", "京东方科技集团股份有限公司", "集团与显示器件", "按应用组织显示器件、技术与全球运营。", boeDirectory),
      site("https://www.boevx.com/", "全球", "英语、中文", "京东方精电有限公司", "车载及工业显示", "公开车载显示业务、核心技术和定制产品。", boeDirectory),
      site("https://www.boevx.uk/", "英国及欧洲", "英语", "BOE Varitronix 英国业务", "当地显示技术支持", "面向英国工程和采购提供显示业务及当地对接。", "https://www.boevx.uk/about"),
      site("https://www.boe.co.jp/", "日本", "日语", "BOE Japan Co., Ltd.", "日本地区业务联系", "独立日语页面给出日本业务和所在地。", boeDirectory),
      site("https://hcsemitek.com/enAbout.html", "全球", "英语；另有中文入口", "京东方华灿光电股份有限公司", "LED 芯片与显示相关器件", "芯片专业站按照明、显示等应用提供资料。", "https://hcsemitek.com/engupiaoxinxi.html"),
    ],
    pattern: "器件集团站承载品类和企业介绍，车载显示专业站面向定制工程项目，英国、日本分别提供客户窗口，LED 芯片站单独呈现专业应用。",
    path: "工程师先核对工况、接口和设计阶段，按产品类别和地区找到专业团队。车载显示项目应预备尺寸、分辨率、环境要求和预计产量。",
    insight: "保持型号与版本可检索，让业务站围绕工程师的应用问题补足资料。区域站列出技术支持范围和本地联系。",
    boundary: "显示模组与集成电路为两个不同贸易指标。案例展示相邻的显示与光电器件业务。",
    sources: [
      source("京东方全球运营资料", boeDirectory, "集团目录可查京东方精电和日本公司。"),
      source("京东方华灿企业与证券信息", "https://hcsemitek.com/engupiaoxinxi.html", "核对公司法定名称及上市业务。"),
    ],
  },
  {
    id: "midea-mbt", industry: "appliances", name: "美的楼宇科技与 Clivet", english: "Midea Building Technologies · Clivet", structure: "hybrid", lead: "technical",
    title: "集团商用暖通、产品品牌与英德本地支持",
    summary: "美的楼宇科技为暖通 B2B 买家提供选型，Clivet 保留品牌和当地支持企业的网站。",
    sites: [
      site("https://hvac.midea.com/", "全球", "英语", "美的楼宇科技", "商用 HVAC 与楼宇解决方案", "面向工程、安装和经销提供商用系统和服务资料。", clivetRelation),
      site("https://www.clivet.com/en/support/assistance-for-your-company", "全球（意大利业务）", "英语、意大利语等", "Clivet S.p.A.", "Clivet 产品与企业支持", "按设备、安装和企业需求组织商用暖通入口。", clivetRelation),
      site("https://www.clivet.de/de/", "德国", "德语", "Clivet 德国业务", "德国安装及服务团队", "地区站提供德语系统目录、技术和联系。", "https://www.clivet.de/privacy/impressum"),
      site("https://www.clivetgroup.co.uk/en/", "英国", "英语", "Clivet Group UK Ltd", "英国商用暖通与本地支持", "提供独立英国站的服务和当地技术资料。", "https://www.clivet.com/documents/d/clivet-uk/accessibility-statement-www-clivetgroup-co-uk-10-09-2025"),
    ],
    pattern: "母业务提供商用暖通和楼宇系统解决方案，Clivet 品牌站面向具体设备和企业。地区站配套当地语言、服务和安装团队。",
    path: "暖通项目采购按冷量、能效、系统和现场条件查产品。德国或英国团队可跟进当地技术、安装和维保要求。",
    insight: "不同市场的系统规范和售后能力直接决定交付。可按当地支持能力设置资料下载和工程选型入口，再把申请交给实际服务团队。",
    boundary: "案例侧重与空调相邻的商用暖通，家电出口数据按行业原始口径展示。",
    sources: [
      source("美的楼宇科技业务介绍", clivetRelation, "包含 Clivet 与美的业务关系。"),
      source("Clivet 德国站法律信息", "https://www.clivet.de/privacy/impressum", "说明德国站及所属集团。"),
    ],
  },
  {
    id: "je-furniture", industry: "furniture", name: "精一家具", english: "JE Furniture", structure: "brands", lead: "sample",
    title: "佛山办公家具制造商与三个品牌站",
    summary: "工厂集团站介绍产线和多品牌，Sitzone、Goodtone 与 ENOVA 分别展示办公座椅、设计师座椅和项目。",
    sites: [
      site("https://www.jegroupintl.com/", "全球", "英语及多语种", "广东精一家具股份有限公司", "办公座椅工厂与出口目录", "按椅型和办公空间展示多品牌产品与询价。", jeBrands),
      site("https://www.sitzonechair.com/", "全球", "英语及多语种", "广东精一家具 SITZONE 品牌", "办公座椅选型与批量询价", "围绕员工、行政、会议等用途维护办公椅目录。", jeBrands),
      site("https://goodtone.cn/", "中国市场与国际项目", "中文", "精一家具 Goodtone 谷腾品牌", "设计座椅与办公项目", "按产品、展会及项目应用展示品牌设计能力。", jeBrands),
      site("https://www.enova-office.com/", "全球", "英语", "ENOVA Office Furniture", "设计座椅与项目采购", "独立组织任务椅、休闲椅、项目和销售询价。", jeBrands),
    ],
    pattern: "工厂和集团目录回答规模、产线与供货问题，品牌站提供更聚焦的产品和办公场景。ENOVA 页脚也链接同集团的 SITZONE 和 Goodtone。",
    path: "办公项目采购按空间和椅型查品牌目录，随后提供材质、颜色、用量、交期和交货地。希望做经销的买家还需要核对各品牌的型号与当地供货。",
    insight: "同一制造商的品牌若有不同设计定位、价格和项目采购方式，可分别承载案例和选型。统一维护基础规格，避免跨站版本混淆。",
    boundary: "品牌归属参考精一家具名单，并通过品牌站页脚与公开品牌页面交叉核对。多语子域随各品牌登记域归并。",
    sources: [
      source("精一家具品牌目录", jeBrands, "集团列示 SITZONE、Goodtone 与 ENOVA 的产品定位。"),
      source("ENOVA 品牌站与其他品牌链接", "https://www.enova-office.com/", "页尾链接 SITZONE 和 Goodtone，并列业务联系。"),
    ],
  },
];
