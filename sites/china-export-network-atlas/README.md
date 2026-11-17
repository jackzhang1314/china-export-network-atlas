# 中国外贸 B2B 站群案例库

按中国重点出口商品和制造业行业研究工厂及外贸公司的站群。只有可以核实至少 4 个独立网站的企业或集团才建案例页。企业详情从完整站点清单开始，品类页和案例索引也提供可点开的域名。使用当地非英语语言和对应国家域名的站点在网页标注，可从案例目录筛选。

## 网站地址与运行

[打开已发布的网站](https://china-export-network-atlas.1314jackzhang.workers.dev/)

- Cloudflare Workers 项目名为 `china-export-network-atlas`。
- Node.js 22 或更新版本可运行构建和预览。源码没有第三方构建依赖。
- `npm run check` 先生成静态网站，再核对四站门槛、逐站来源、内部链接与三份 CSV。
- `npm run preview` 在本机提供预览，默认地址为 `http://127.0.0.1:8787/`。
- 在已登录 Cloudflare 的环境中运行 `npm run deploy` 部署。该命令使用已安装的 Wrangler。发布目录为 `dist/`，部署设置位于 `wrangler.jsonc`。
- 部署后访问根页、案例详情、CSV 下载和一个不存在的路由，检查后者返回 HTTP 404。

## 内容维护

- `content/industries.mjs` 维护品类及统计来源。全国货物出口和 14 个重点商品项使用国家统计局 2025 年公报。行业协会或研究院的 4 个统计项按来源保留币种及范围。行业案例专项亦使用同一个品类目录。
- `content/networks.mjs` 是发布用的案例入口。既有行业数据与本次国家域名专题分别在对应的 `networks-*.mjs` 和 `network-sany.mjs` 维护。
- 补充网站时，核对最终页面、实际业务内容、法定主体或集团公开关系。每个独立注册域计一次。专用域名后缀规则位于 `network-schema.mjs`，若引入新的多段公共后缀先补规则。纯跳转域、第三方店铺与经销商自有站不计。
- 案例页先列完整网址、市场、语言、用途和运营方，再展示站群分工与采购路径。逐站归属可通过来源链接核对。
- 站点 CSV 一域一行，保留市场、运营方、用途与归属来源。`data/localized-country-sites.csv` 汇总当地语言和国家域名对应的入口。
- 首页的集装箱港口图为 ImageGen 生成的说明性图片，图像位于 `public/images/container-port.webp`。
