import researchArchive from "./research-archive.json" with { type: "json" };
import packagingSites from "./pdt-core-sites.json" with { type: "json" };

export { researchArchive, packagingSites };
export const packagingResearch = researchArchive.find(item => item.id === "C002");

export function researchPath(item) {
  return item.id === "C002" ? "/cases/pdtrus/" : `/research/${item.id.toLowerCase()}/`;
}
