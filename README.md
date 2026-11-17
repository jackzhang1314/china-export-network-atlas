# 中国外贸 B2B 站群研究

研究中国工厂、制造集团和外贸公司的独立站，按行业、市场和语言记录各站用途、采购入口与归属依据。仓库包含网站源码、逐站网址、研究报告、公开证据、可交互教学材料及项目交付记录。

[打开线上案例库](https://china-export-network-atlas.1314jackzhang.workers.dev/cases/) · [浏览小语种国家域名案例](https://china-export-network-atlas.1314jackzhang.workers.dev/cases/?local=1)

## 网站与数据

| 内容 | 入口 |
| --- | --- |
| 网站源码、样式与 Cloudflare 配置 | [sites/china-export-network-atlas](sites/china-export-network-atlas/) |
| 精简版源码与可部署静态站 | [下载 ZIP](output/site/中国外贸B2B站群案例库_精简版_源码与静态站.zip) |
| 28 组企业、159 个独立网站 | [完整网站 CSV](data/b2b-site-links.csv) |
| 33 个当地语言与国家域名对应的网站 | [小语种国家站 CSV](data/localized-country-sites.csv) |
| 18 项出口指标及来源 | [出口数据 CSV](data/export-metrics.csv) |

## 完整研究资料

| 内容 | 入口 |
| --- | --- |
| 125 组案例、1,552 条网址记录 | [案例总表](outputs/2026-11-14-wordpress-country-guide/案例研究资料包/01_125组案例总表.csv) · [完整网址表](outputs/2026-11-14-wordpress-country-guide/案例研究资料包/04_企业站群完整链接表.csv) |
| PDT R US / Design Media Service 包装站群 | [47 个核心关联域名与逐站证据](outputs/2026-11-05-site-network/站群域名与逐站证据.csv) · [深度研究报告](outputs/2026-11-05-site-network/企业独立站站群深度研究报告.md) · [60 个核验对象](outputs/2026-11-05-site-network/全部核验对象总表.csv) |
| 三一的全球站点、语言和地区入口 | [全球域名清单](outputs/2026-11-12-sany-global-network/三一全球站点与域名清单.csv) · [研究目录](outputs/2026-11-12-sany-global-network/) |
| 中国制造和跨行业国家站研究 | [中国制造补充研究](outputs/2026-11-12-china-b2b-country-networks/) · [工业与 B2B 研究](outputs/2026-11-12-b2b-multilingual-seo/) · [本地语言国家站证据](outputs/2026-11-17-localized-country-sites/) |
| 教学和可阅读交付 | [交互式案例 HTML](outputs/2026-11-06-teaching-case/站群案例教学.html) · [完整案例 PDF](output/pdf/AI外贸独立国家域名站群_125组案例与方案解读.pdf) · [案例研究资料包](output/pdf/AI外贸独立国家域名站群_案例研究资料包.zip) |
| 各阶段原表、证据、报告、图片与媒体 | [研究文件](outputs/) · [交付文件](output/) · [项目记录](process_docs/) |

旧研究表保留每条网址当时的证据分类、市场和观察时间。C086（RMC Polska）在案例总表中列有公开项目出处。PDT R US 的 47 个域名有共同运营关联的公开证据，股权和域名法律所有权使用原报告的查证范围。设计概念图中的工厂、设备和人物是示意素材。

## 构建与预览

用 Node.js 22 或更新版本运行以下命令。

```sh
cd sites/china-export-network-atlas
npm run check
npm run preview
```

本地预览地址为 `http://127.0.0.1:8787/`。构建后的站点位于 `sites/china-export-network-atlas/dist/`。部署配置及数据维护说明见[网站 README](sites/china-export-network-atlas/README.md)。

报告所引用的企业网站、外部报告与素材权利归相应权利人。出处随案例及证据提供。

公开归档副本遮盖了抓取页面中附带的第三方服务密钥和令牌。25 个调整后的证据文件可以按[公开副本校验表](data/公开证据副本校验.csv)核对。
