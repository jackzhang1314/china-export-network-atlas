export const nbs = "https://www.stats.gov.cn/sj/zxfbhjd/202602/t20260228_1962662.html";
export const nbsEnglish = "https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html";
export const tradeTotal = 269890;
export const tradeGrowth = 6.1;
export const electricalTotal = 164683;

export const groups = {
  digital: "电子与家电",
  industrial: "装备与能源",
  materials: "材料与供应链",
  consumer: "消费与轻工",
};

function national(item, amount, growth) {
  return { item, amount, growth, unit: "亿元", source: nbs, publisher: "国家统计局公报 · 表11", national: true };
}

function sector(item, amount, growth, unit, publisher, source) {
  return { item, amount, growth, unit, publisher, source, national: false };
}

export const industries = [
  {
    id: "computing", group: "digital", name: "计算机与服务器", english: "Computing & Servers",
    metrics: [national("自动数据处理设备及其零部件", 14530, -0.8)],
    scope: "出口统计覆盖自动数据处理设备及零部件。研究关注工业计算机、企业服务器、配件与当地采购支持。",
    buyer: "企业 IT、系统集成商与渠道商分别关心型号供货、配置兼容、批量采购价格、维保与本地技术支持。",
    compare: "联想给服务器产品、渠道合作、合肥工厂和亚太企业 IT 团队各自设置入口。按买家角色分站时，可分别给系统集成商、渠道伙伴和项目买家准备资料。",
    apply: "以产品型号为核心维护参数、驱动和文档。国家页保留当地供货清单、服务窗口及企业采购入口。渠道商和终端买家的入口应有不同的字段。",
  },
  {
    id: "components", group: "digital", name: "芯片与显示器件", english: "Semiconductors & Displays",
    metrics: [national("集成电路", 14442, 27.4), national("液晶平板显示模组", 2306, 11.7)],
    scope: "集成电路与液晶平板显示模组分别引用国家统计局商品项。车载显示与光电器件站群体现工程买家如何联系专业团队。",
    buyer: "设计工程师通过料号、封装、接口、工作温度和长期供应条件筛选。工程样品、选型资料、技术沟通和分销库存是后续决策环节。",
    compare: "京东方把车载显示、LED 芯片和集团显示业务放到各自站点。海外支持公司的独立域提供本地客户联系，帮助工程买家把需求交给对应团队。",
    apply: "先建立能按料号访问的产品详情、规格书和版本管理，再按当地服务差异分出支持入口。询盘应带上项目阶段、数量和设计要求。",
  },
  {
    id: "phones", group: "digital", name: "手机", english: "Mobile Phones",
    metrics: [national("手机", 8696, -9)],
    scope: "出口额采用手机商品项。行业研究聚焦 ODM 工厂、区域采购与量产交付。",
    buyer: "品牌采购与通信渠道关心研发能力、型号定制、制式、量产计划、可选产地和交付支持。",
    compare: "产品方案和量产能力通常由总部公开。区域沟通若涉及不同制式、法定认证、本地实验室或交付节点，应在所在市场的页面明确。",
    apply: "把产品方案、可定制范围、样机阶段、量产与市场交付写给企业采购。区域站强调当地项目对接，全球站维护统一能力说明。",
  },
  {
    id: "appliances", group: "digital", name: "家用电器", english: "Home Appliances",
    metrics: [sector("家用电器", 6888.5, -3.3, "亿元", "中国家用电器研究院 · 海关口径", "https://cheari.ac.cn/index.php/Show/cid/104/aid/4136")],
    scope: "行业报告引用全国海关统计。以与空调相邻的商用暖通观察多站运营，金额沿用家电总体口径。",
    buyer: "经销商和项目采购常查容量、能效、电源、安装尺寸、说明书和当地服务。家电还需要国家层面的售后与备件分配。",
    compare: "美的楼宇科技提供商用暖通选型，Clivet 品牌站展示设备与企业服务。英国和德国站各有当地的技术组织与客户支持。",
    apply: "把同系列机型的市场规格差异做成字段，型号 PDF 与安装说明随本地页面呈现。客户入口按购买、安装或渠道合作分流。",
  },
  {
    id: "machinery", group: "industrial", name: "工程机械", english: "Construction Machinery",
    metrics: [sector("工程机械产品（含主机和零部件）", 602.3, 13.9, "亿美元", "中国机电产品进出口商会 · 海关口径", "https://www.cccme.org.cn/model5-1/news/details.aspx?classid=3AFFFDC5D50285DC&id=FA31909AA38635DB58A6BB39B8975578&xgid=F868932F64EB7AAF")],
    scope: "商会报告同时给出 2025 年亚洲 251.6 亿美元、欧洲 129.6 亿美元、非洲 88.9 亿美元的样本地区出口数据。金额反映已有货物流向，市场页优先级还要考虑当地渠道与服务。",
    buyer: "租赁商、承包商和经销商按吨位、工况、机型及附件采购。交付后，他们还关心零件、维修、培训及当地人员是否可以到场。",
    compare: "三一印度站集中选型、经销与配件，徐工智利站给挖掘机设置西语报价入口，杭叉法国站提供租赁与售后。中联的混凝土、高空作业和杭叉北美自动化业务各用专业目录承接项目。",
    apply: "先做适用于当地的主机系列，给规格和应用配上明确的报价或经销入口。备件、保修和本地联系人直接对应机器型号。",
  },
  {
    id: "vehicles", group: "industrial", name: "汽车与商用车", english: "Vehicles & Commercial Vehicles",
    metrics: [national("汽车（包括底盘）", 10183, 22)],
    scope: "统计项涵盖汽车及底盘。站群研究关注公交与商用车项目采购及当地服务，轮胎单列。",
    buyer: "公交与客运采购要核对乘员配置、线路和维保方式。商用卡车看载重、上装、续航、车队交付和总使用成本。",
    compare: "宇通的客车站让买家看全球车型，欧洲与法国站提供下一步的区域项目资料、车型与服务窗口。对复杂商业车辆，交付和维保责任影响站点分工。",
    apply: "只展示可在当地销售、交付和维护的车型。工厂可以借鉴按国家设定销售责任、用途内容以及咨询去向的做法。",
  },
  {
    id: "tires", group: "industrial", name: "轮胎", english: "Tires",
    metrics: [sector("橡胶轮胎", 1677.03, 2, "亿元", "中国橡胶工业协会 · 海关口径", "https://www.cria.org.cn/a/2017043170962018306")],
    scope: "协会称其中新的充气橡胶轮胎为 1,611.23 亿元，汽车橡胶轮胎为 1,376.12 亿元。两个子口径有交叉，分别用于说明结构。",
    buyer: "进口商、胎店、车队与主机厂按尺寸、负荷和速度级别找产品，也要核对配套、使用场景、产品标签和当地服务。",
    compare: "玲珑展示集团销售与德国经销入口分工。赛轮美国品牌站负责找胎与门店，欧洲产品信息可以与供应方公开标签交叉核对。",
    apply: "让产品页覆盖规格、适配车辆、花纹与应用，并按型号维护当地可公开资料。分开设计经销合作、终端找店和质保入口。",
  },
  {
    id: "energy", group: "industrial", name: "光伏与储能", english: "Solar & Energy Storage",
    metrics: [sector("光伏产品（硅片、电池片、组件）", 294.5, -8, "亿美元", "中国机电产品进出口商会 · 海关口径", "https://www.cccme.org.cn/model5-1/news/details.aspx?classid=7685F2FA1E54A7F5&id=B31FE14D32F9104E20D30B61AB70D332&xgid=F868932F64EB7AAF")],
    scope: "指标覆盖硅片、电池片、光伏组件。案例也观察同集团在储能、逆变器和配电领域的相邻网站。",
    buyer: "安装商、渠道商、项目集成商按系列、功率、接口与项目规模筛选。数据表、安装手册、合规文件、技术支持和运维能力影响下一步。",
    compare: "晶科按市场分光伏站，储能系统另设产品线域。正泰用不同网站承接电站开发、组件、逆变器和配电。每站需要匹配自己的技术文件和项目责任。",
    apply: "产品文件用型号和市场归档，保留版本与适用范围。以当地服务工程师、安装商支持或项目咨询为页面目标，根据覆盖能力规划独立站。",
  },
  {
    id: "textiles", group: "materials", name: "纺织纱线与面料", english: "Textiles & Yarns",
    metrics: [national("纺织纱线、织物及其制品", 10205, 1)],
    scope: "纱线、面料和纺织制品按国家公报口径观察。研究关注面料选样、定制生产和多地交付。",
    buyer: "织造厂、服装品牌采购团队查纤维成分、纱支、克重、色牢度、色卡、起订量、样品与产地。跨国工厂还涉及各地产能和打样联系。",
    compare: "纺织站的目录要回答能否拿样、批次能否复购、从哪里生产与交付。地区切换时，看区域站是否有独立的打样、库存或供货团队。",
    apply: "为产品做结构化成分和工艺资料，按买家搜索区分原料、规格与用途。多个地区有真实选型、打样及服务差异时，才有充分理由各自建页。",
  },
  {
    id: "apparel", group: "consumer", name: "服装与衣着附件", english: "Apparel",
    metrics: [national("服装及衣着附件", 10822, -4.4)],
    scope: "出口额引用服装及衣着附件商品项。研究关注品牌与批发商的成衣定制、运动服 OEM 和打样供应链。",
    buyer: "服装品牌采购关注面辅料、工艺、样衣、品控、最小订量与交付周期。不同类型的定制需要提交不同资料。",
    compare: "品牌、ODM 和成衣工厂在面料选择、样版和订单管理上有不同职责。核对报价前需要的样衣、面辅料、工艺细节和数量，能判断各站承担哪一步。",
    apply: "工厂可把尺码、面料、工艺和打样条件结构化，按市场补充交付约束。把国家页的动作收敛到索样、拿规格或者批量询价。",
  },
  {
    id: "packaging", group: "materials", name: "塑料制品与包装", english: "Plastics & Packaging",
    metrics: [national("塑料制品", 7487, -0.8)],
    scope: "金额是塑料制品整体口径。案例中的纸张和植物纤维包装用于对照相邻包装业务的网站分工。",
    buyer: "品牌方和灌装厂从容量、口径、材质、起订量、结构和工艺进入采购。不同国家的样品快递与可供应方案也会影响联系。",
    compare: "裕同全球站说明制造与多地交付，澳洲站提供当地采购联系，环保包装站展示材料和产品，匈牙利工厂提供印刷包装服务。",
    apply: "拿同一款产品做对照，检查两国页面的尺寸、材料、交期和样品入口是否真的有差异。产品分站需要清晰的产品边界与持续内容能力。",
  },
  {
    id: "steel", group: "materials", name: "钢材", english: "Steel Products",
    metrics: [national("钢材", 5911, -0.7)],
    scope: "2025 年钢材数量 11,902 万吨，同比增长 7.5%。数量增加伴随金额略降，适合把规模与金额增速一起阅读。",
    buyer: "工程采购用牌号、执行标准、尺寸、公差及表面处理筛选，之后需要材质证明、交期与贸易条款，并区分现货与产线定做。",
    compare: "青山公开列出旗下企业实际运营的域名。集团提供国际业务与联系，青拓提供产品与销售资料，永青和上海鼎信介绍跨国园区与供应链。",
    apply: "先做规范页、牌号对照、材料证明和报价资料。地域页承载库存、交付和合适的责任主体，帮助买家从材料识别走向采购。",
  },
  {
    id: "furniture", group: "consumer", name: "家具与家居", english: "Furniture & Homewares",
    metrics: [national("家具及其零件", 4559, -5.6)],
    scope: "出口按家具及零件计。案例聚焦办公家具工厂、品牌组合和空间项目采购。",
    buyer: "经销商、办公项目和批发采购分别关注材质、尺寸、安装和交货。查看当地展厅及交付范围，可以更快判断项目能否承接。",
    compare: "精一家具的出口站呈现多品牌目录，品牌站各自展示适用空间和产品。家具集团可以按客群、设计定位和采购模式分站。",
    apply: "优先建立统一产品和配件的规格数据，再以本地仓配、售后与采购窗口分市场。做 B2B 时强调工程案例、组合规格和批量交付。",
  },
  {
    id: "footwear", group: "consumer", name: "鞋靴", english: "Footwear",
    metrics: [national("鞋靴", 2975, -10.8)],
    scope: "公报鞋靴项包括多种鞋类。研究关注鞋厂代工、大货订单和贸易采购。",
    buyer: "品牌采购核对鞋楦、尺码、材料、鞋底、工艺、数量和样期。能否从纸样到成品共同开发，会影响选择哪家供应商。",
    compare: "工厂站应能说明鞋楦开发、材料准备和大货品控。贸易团队面向海外采购交代型号、订单与交付。看独立站时先核对业务角色和经营主体。",
    apply: "用鞋型、适用场景和工艺做目录，每页给出需要买家提交的规格与开发材料。若同一鞋型服务多国，可为不同尺码标准和渠道规则补充当地页。",
  },
  {
    id: "luggage", group: "consumer", name: "箱包与背包", english: "Luggage & Bags",
    metrics: [national("箱包及类似容器", 2140, -12.9)],
    scope: "公报使用箱包及类似容器口径。研究关注软包、旅行包、OEM 订单及产贸关系。",
    buyer: "品牌、批发商和礼品采购常按容量、材质、附件、目标价格、起订量、标识和定制包装筛选。",
    compare: "定制采购由用途、材料和标识工艺共同决定。比较各工厂及贸易站时，核对有没有分别列出生产能力、样品和报价动作。",
    apply: "可将常用材料、部件、工艺及用途做成产品和方案资料。询盘应便于描述打样、目标市场、数量、运输及上市节奏。",
  },
  {
    id: "toys", group: "consumer", name: "玩具", english: "Toys",
    metrics: [national("玩具", 2493, -12.1)],
    scope: "出口额按玩具商品项。研究关注生产、出口贸易与海外经销在产品规格和合作流程上的分工。",
    buyer: "分销商看品牌授权、适龄、包装、条码、商品目录和最低订货条件。产品说明、备件和售后条件也关系到渠道能否长期供货。",
    compare: "分销站可以公开产品与合作；工厂站可以围绕产品合规、功能及可定制内容。研究站群归属时，确认工厂、贸易和授权经销是否为同组主体。",
    apply: "按系列和年龄维护产品资料，区分说明、配件（售后）与经销申请。各市场的授权和合规信息由实际主体核定后公开。",
  },
  {
    id: "containers", group: "industrial", name: "集装箱与特种箱", english: "Containers & Special Equipment",
    metrics: [national("集装箱", 972, -19.9)],
    scope: "公报统计集装箱出口。标准干箱、冷藏箱和定制特种箱具有不同选型与询盘逻辑，案例覆盖从集团到工厂的分工。",
    buyer: "航运、租赁、工程集成商需要箱型、尺寸、制冷或专用设备接口、应用环境、交付地与生产周期。",
    compare: "中集集团总览集装箱与运输业务，特种箱工厂面向定制设备，安瑞环和安瑞科分别组织罐箱与运输储运方案。",
    apply: "以箱型、工况和定制条件组织页面，把询盘导向对应生产基地或区域团队。尺寸与选件表应帮助买家说明用途、数量、交付地。",
  },
  {
    id: "cables", group: "materials", name: "光纤通信与电力线缆", english: "Optical & Power Cables", metrics: [],
    scope: "跟踪线缆与光通信制造商的海外工厂，观察葡语、印尼语和土耳其语的当地选型入口。",
    buyer: "工程商、电网和电信采购按通信或电力用途、敷设环境、结构参数、项目验收与交付地筛选。",
    compare: "亨通的葡萄牙、巴西与印尼站按当地工厂经营。中天巴西与土耳其分别展示通信和电力线缆，产品内容随制造职责变化。",
    apply: "集团可统一说明测试与制造能力；不同制造地的网站补充在地库存、标准文件、交付与销售联系。",
  },
  {
    id: "molding", group: "industrial", name: "注塑机械与成型装备", english: "Injection Molding", metrics: [],
    scope: "观察注塑设备工厂如何在当地用语言、机型和试模支持与加工厂对接。",
    buyer: "设备买家需要确认材料、模具、制品重量、周期、自动化配合和当地备件。",
    compare: "海天在土耳其用独立国家域对接客户，巴西用以品牌命名的葡语网站。全电动注塑机则由品牌专站讲清产品差异。",
    apply: "当地团队有试模、培训和配件时，可以把这些能力写进市场页，并让表单收集模具、制品和产量信息。",
  },
  {
    id: "laser", group: "industrial", name: "激光加工装备", english: "Laser Processing Equipment", metrics: [],
    scope: "研究金属激光切割设备制造者的本地化技术资料、选型、展厅和服务。",
    buyer: "工厂采购按板材和管材、厚度、尺寸、产线节拍及售后半径确定设备。样件试切和当地维修经常影响采购顺序。",
    compare: "宏山用 .co.jp 和 .co.kr 提供日语和韩语技术与销售。国家域和当地公司相对应，国际站则统一产品系列。",
    apply: "从工况、样件、交付地和当地支持设计询盘字段，给客户提供能预约测试和沟通项目的入口。",
  },
  {
    id: "industrial-compressors", group: "industrial", name: "工业制冷与压缩设备", english: "Industrial Refrigeration & Compressors", metrics: [],
    scope: "覆盖工业制冷压缩机、空压机与海外专业品牌，比较意大利语及德语工程网站。",
    buyer: "买家要提供使用场景、压力或制冷工况、安装条件与当地备件服务，才能初步确定设备匹配。",
    compare: "雪人的意大利站以压缩机选型为主，开山旗下奥地利 LMF 为德语工程客户提供产品服务。两个集团都保留被并入品牌的专业站。",
    apply: "按设备与用途维护资料，注明能提供调试、备件与维护的当地团队。",
  },
  {
    id: "warehouse", group: "industrial", name: "仓储搬运与物流系统", english: "Warehousing & Intralogistics", metrics: [],
    scope: "研究叉车等搬运设备和整仓自动化项目如何分流至不同企业入口。",
    buyer: "单台设备关注载荷、上升高度、作业空间及动力系统；自动化项目关心流程、吞吐量、投入期和系统接口。",
    compare: "诺力法国国家域经营搬运设备，在同一集团内由 SAVOYE 另站承接仓储系统和软件。",
    apply: "将由渠道提供的设备报价和由工程团队管理的复杂项目分别收集。当地站保留可交付型号与支持。",
  },
  {
    id: "pumps", group: "industrial", name: "水泵与流体设备", english: "Pumps & Fluid Equipment", metrics: [],
    scope: "观察面向建筑、农灌、市政和产业项目的水泵选型及当地分销入口。",
    buyer: "采购按液体、流量、扬程、环境和电源筛选。配套件与后期维护关系到现场效果。",
    compare: "利欧用泰国和印尼国家域提供本地语言及具体市场销售渠道，并给欧洲业务配置区域站。",
    apply: "把跨市场共用的参数和当地采购入口一起呈现。地区页补充场景、配套、展示和联系。",
  },
  {
    id: "auto-parts", group: "industrial", name: "汽车零部件与配套", english: "Automotive Components", metrics: [],
    scope: "观察配套制造、区域工厂与零部件售后市场如何使用不同域名。",
    buyer: "整车配套采购重视车型平台、产线与质量验证，替换件批发关注车型适配、库存和地区支持。",
    compare: "福耀的集团、欧洲、匈牙利和美国站面向制造与区域采购。全球替换件网站有独立产品用途和销售联系。",
    apply: "按配套和售后市场整理不同规格与报价路径，国家站列明交付地点和责任团队。",
  },
  {
    id: "commercial-lighting", group: "digital", name: "商用与工程照明", english: "Professional Lighting", metrics: [],
    scope: "对照工程灯具在西班牙与法国的技术目录、项目支持和资料语言。",
    buyer: "批发商、设计师和工程采购查场景、安装方式、光学参数、维护、技术文件与保修。",
    compare: "欧普通用欧洲站面向工程采购，西班牙、法国国家域保留各自语言的资料和地区联系。",
    apply: "每个地区站可以复用设备参数，同时维护本地使用条件、文件和售后说明。",
  },
  {
    id: "wind-power", group: "industrial", name: "风电整机与电气系统", english: "Wind Power Equipment", metrics: [],
    scope: "通过整机、当地风电工程和德国电气技术公司观察集团站点的技术分工。",
    buyer: "整机或场站项目需要核对地形、资源、并网、运维和交付。配套采购会关注电气设备界面和集成条件。",
    compare: "金风的德国风电整机与电气控制公司使用各自的德语国家域，区域项目另有集团及美洲入口。",
    apply: "将整机和配套采购的资料与联系人写清楚。以实际工程团队和业务范围判断分站价值。",
  },
];

export const seoSource = "https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites";
