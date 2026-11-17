export const structures = {
  country: { name: "独立国家或区域域名", detail: "同一集团的多个市场入口使用不同注册域。区域域名和国家域名在案例中按实标注。" },
  paths: { name: "同域国家与语言目录", detail: "以主域下的路径或子域经营地区与语言版本，产品资料可集中维护。" },
  brands: { name: "品牌、工厂或业务分站", detail: "按品牌、技术、工厂或销售角色分出不同网站，国家范围随业务而定。" },
  channels: { name: "厂家与当地渠道站", detail: "厂家入口与进口、分销、经销网络配合。网页明确标注观察到的运营方。" },
  central: { name: "集中官网对照", detail: "集中展示全球产品、工厂或销售网络，用来判断业务覆盖是否需要分成多个站。" },
  hybrid: { name: "多种结构并用", detail: "同时看到主域地区路径、不同域名或渠道分工，按每个入口的实际作用判断。" },
};

export const leadTypes = {
  rfq: "询价与项目",
  channel: "经销与渠道",
  sample: "定制与打样",
  technical: "选型与支持",
};

export const evidenceLevels = {
  primary: "官方链接或主体声明",
  bounded: "公开链路样本",
  reference: "对照案例",
};

export function site(label, url, market, language, role, observation) {
  return { label, url, market, language, role, observation };
}

export function source(label, url, note) {
  return { label, url, note };
}
