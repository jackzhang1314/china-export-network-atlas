import { website as site } from "./network-schema.mjs";
import { source } from "./schema.mjs";

const parent = "https://www.sanygroup.com/";

export const sany = {
  id: "sany", industry: "machinery", name: "三一集团", english: "SANY", structure: "hybrid", lead: "channel",
  title: "全球产品站、国家销售服务站与独立产品线",
  summary: "同一品牌既按市场分站，也给挖掘机、混凝土机械和重卡单独设站。买家可在各地查看当地机型、经销、维修和配件。",
  sites: [
    site("https://www.sanyglobal.com/", "全球", "英语及多语种", "三一集团国际业务", "全球产品目录", "按设备大类选型，再进入联系或经销服务。主站多语共用一个注册域。", "https://www.sanyglobal.com/press_releases/1104/"),
    site("https://www.sanyeurope.com/", "欧洲", "德语、英语、法语、西语", "SANY Europe GmbH", "欧洲产品与渠道", "提供欧洲机型、经销网络和服务资料，也链接欧洲产品线网站。", "https://www.sanyeurope.com/impressum/"),
    site("https://www.sanyuk.com/", "英国、爱尔兰", "英语", "SANY Heavy Machinery (UK) Ltd", "本地销售与售后", "把设备、二手设备、金融、保修和配件分开展示。", "https://www.sanyuk.com/about-sany/"),
    site("https://www.sany-ne.com/", "瑞典及北欧", "英语", "SANY Northern Europe AB", "北欧经销与服务", "发布区域经销与服务联系，面向当地设备用户。", "https://www.sany-ne.com/contact/"),
    site("https://www.sany-benelux.com/", "荷兰、比利时、卢森堡", "英语、荷兰语、法语", "SANY Benelux B.V.", "比荷卢区域业务", "同一个区域站按语言提供产品、经销商与联系信息。", "https://www.sany-benelux.com/about-us/"),
    site("https://sany-france.com/", "法国", "法语", "SANY Heavy Machinery (France) SAS", "法国销售与网络", "法语设备目录和销售服务指向当地业务。", "https://sany-france.com/privacy-policy/"),
    site("https://www.sanyiberia.com/es/servicio-repuestos", "西班牙、葡萄牙", "西语、葡语、英语", "Putzmeister Holding GmbH（站点声明）", "伊比利亚区域站", "西班牙与葡萄牙市场在同一个域下展示语言和产品入口。", "https://www.sanyiberia.com/imprint-sanyiberia"),
    site("https://www.sanyitalia.com/", "意大利", "意大利语", "三一意大利团队", "意大利销售与服务", "正文以意大利语组织设备、销售及服务。", "https://www.sanyitalia.com/contact/"),
    site("https://www.sanypoland.com/pl/", "波兰及周边", "波兰语、英语", "三一波兰团队", "波兰产品与服务", "公布波兰团队和集团邮箱，便于询问本地机型与支持。", "https://www.sanypoland.com/pl/index.php/kontakt/"),
    site("https://www.sany.in/", "印度", "英语", "SANY Heavy Industry India", "印度制造、销售与经销", "本地制造背景、产品系列、经销和配件并列。", "https://www.sany.in/about-us/"),
    site("https://www.sanyamerica.com/", "美国及北美", "英语", "SANY America", "北美销售与服务", "机型目录、经销商和售后资源采用当地入口。", "https://www.sanyamerica.com/about/"),
    site("https://www.sanydobrasil.com/", "巴西", "巴西葡语", "SANY do Brasil", "巴西销售与服务", "巴葡产品页面与当地进出口企业和支持渠道对应。", "https://www.sanydobrasil.com/politica-de-privacidade/"),
    site("https://www.sanymexico.com/", "墨西哥", "西语", "三一墨西哥团队", "墨西哥采购与服务", "当地产品、地址和集团邮件供设备客户联系。", "https://sanymexico.com/nosotros"),
    site("https://www.sanycolombia.com/", "哥伦比亚", "西语", "三一哥伦比亚团队", "哥伦比亚销售与分支", "产品页和各地团队联系方式放在同一市场站。", "https://sanycolombia.com/nosotros"),
    site("https://www.sanyjapan.com/", "日本", "日语", "三一日本株式会社", "日本销售与联系", "以日语展示当地产品、公司资料与联系渠道。", "https://www.sanyjapan.com/about-sany/"),
    site("https://www.sanymalaysia.com/", "马来西亚", "英语", "三一马来西亚业务", "本地设备、经销与联系", "使用马来西亚设备目录和当地联系，站内链接集团国际站。", "https://www.sanymalaysia.com/about-sany/"),
    site("https://www.sanyoceania.com/service-parts", "澳大利亚、新西兰", "英语", "三一大洋洲团队（Putzmeister 业务体系）", "澳新销售与服务", "组织面向澳大利亚及新西兰的产品与支持内容。", "https://www.sanyoceania.com/service-parts"),
    site("https://www.sanyturkiye.com/maintenance-support", "土耳其", "土耳其语、英语", "Putzmeister Türkiye", "土耳其销售与服务", "本地团队负责三一设备销售和服务，提供两种正文语言。", "https://www.sanyturkiye.com/maintenance-support"),
    site("https://www.sanyexcavator.com/", "全球", "英语", "三一挖掘机业务", "挖掘机产品线", "独立展示挖掘机目录，报价入口转给集团官网。", parent),
    site("https://www.sanyconcretemachinery.com/", "欧洲", "英、德、法、西语", "三一欧洲混凝土机械业务", "混凝土机械产品线", "按泵送和搅拌等设备展示选型，与欧洲主站衔接。", "https://www.putzmeister.com/web/sanyconcretemachinery/company"),
    site("https://www.sanytruck.com/intl/", "全球", "英语；另有中文站内入口", "三一重卡", "重卡国际产品线", "以重卡产品为独立站主题，国际目录位于站内。", parent),
    site("https://www.sany-trucks.com/", "欧洲", "英、德、法、西语", "SANY Europe 重卡业务", "欧洲电动重卡", "面向欧洲展示电动重卡和联系窗口，欧洲官网明确链接。", "https://www.sanyeurope.com/"),
  ],
  pattern: "全球站覆盖通用型号和语言，国家站承接当地供应、保修、服务网点和零件，品类站围绕选型集中展示设备。同一设备可以在多个站被看到，下一步联系取决于所在市场和需求。",
  path: "以需要更换工地挖掘机的采购商为例，先在全球或挖掘机站确认吨位、工况和型号，再在印度、英国等实际销售地核对经销商和服务。跨国订单要看交付市场的保修与配件说明。",
  insight: "把型号、通用规格及图纸统一维护。只有当地有不同库存、型号、经销或质保责任时，才需要独立经营对应市场的页面和询盘。",
  boundary: "以三一集团入口、当地公司页和法律声明为依据。国家语言目录、单纯跳转的域和经销商自己的域都不计入本页清单。",
  sources: [
    source("三一集团业务入口", parent, "集团页链接区域公司和独立产品线。"),
    source("三一欧洲法律声明", "https://www.sanyeurope.com/impressum/", "列示欧洲站运营主体，并可由欧洲站返回各业务入口。"),
    source("Putzmeister 集团介绍", "https://www.putzmeister.com/web/americas/about-us", "供核对 Putzmeister 与三一的集团关系。"),
  ],
};
