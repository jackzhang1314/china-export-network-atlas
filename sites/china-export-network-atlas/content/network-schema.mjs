const multiLabelSuffixes = new Set([
  "com.au", "com.br", "com.cn", "com.tr", "co.id", "co.jp", "co.th", "co.uk",
  "net.au", "org.uk", "com.ar", "co.za", "co.kr", "co.in", "com.eg", "com.mx", "com.ru", "ind.br",
]);

export const minimumSites = 4;

export function registeredDomain(url) {
  const parts = new URL(url).hostname.split(".");
  const suffix = parts.slice(-2).join(".");
  return multiLabelSuffixes.has(suffix) ? parts.slice(-3).join(".") : suffix;
}

export function website(url, market, language, operator, role, observation, evidenceUrl, accessNote = "") {
  return { domain: registeredDomain(url), url, market, language, operator, role, observation, evidenceUrl, accessNote };
}

export function localWebsite(countrySuffix, ...fields) {
  return { ...website(...fields), countrySuffix };
}
