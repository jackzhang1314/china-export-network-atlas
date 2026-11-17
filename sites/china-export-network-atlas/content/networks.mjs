import { equipmentNetworks } from "./networks-equipment.mjs";
import { manufacturingNetworks } from "./networks-manufacturing.mjs";
import { countryManufacturers } from "./networks-country-manufacturers.mjs";
import { countryIndustryNetworks } from "./networks-country-industry.mjs";

const verifiedCountryDomains = new Map([
  ["xcmg.co.id", ".co.id"],
  ["zoomlion.com.tr", ".com.tr"],
  ["zoomlion.com.br", ".com.br"],
  ["liugongrussia.ru", ".ru"],
  ["hcrs.fr", ".fr"],
  ["yutong.fr", ".fr"],
  ["linglong.de", ".de"],
  ["boe.co.jp", ".co.jp"],
  ["clivet.de", ".de"],
]);

const existingCases = [...equipmentNetworks, ...manufacturingNetworks].map(item => ({
  ...item,
  sites: item.sites.map(site => verifiedCountryDomains.has(site.domain)
    ? { ...site, countrySuffix: verifiedCountryDomains.get(site.domain) }
    : site),
}));

export const newCountryCases = [...countryManufacturers, ...countryIndustryNetworks];
export const cases = [...existingCases, ...newCountryCases];
