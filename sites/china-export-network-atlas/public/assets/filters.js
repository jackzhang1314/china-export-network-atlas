const groupFilter = document.querySelector("[data-group-filter]");
const groupGrid = document.querySelector("[data-group-grid]");

if (groupFilter && groupGrid) {
  groupFilter.hidden = false;
  const choices = [...groupFilter.querySelectorAll("button[data-group-choice]")];
  const cards = [...groupGrid.querySelectorAll("[data-group]")];
  for (const button of choices) {
    button.addEventListener("click", () => {
      const selected = button.dataset.groupChoice;
      for (const choice of choices) choice.setAttribute("aria-pressed", String(choice === button));
      for (const card of cards) card.hidden = Boolean(selected && card.dataset.group !== selected);
    });
  }
}

const form = document.querySelector("[data-case-filter]");
const grid = document.querySelector("[data-case-grid]");
const count = document.querySelector("[data-result-count]");
const empty = document.querySelector("[data-empty]");

if (form && grid && count && empty) {
  form.hidden = false;
  const fields = ["q", "industry", "structure", "lead", "local"];
  const cards = [...grid.querySelectorAll("[data-index]")];

  function readQuery() {
    const params = new URLSearchParams(location.search);
    for (const field of fields) form.elements.namedItem(field).value = params.get(field) || "";
  }

  function refresh(writeQuery) {
    const data = new FormData(form);
    const terms = String(data.get("q") || "").trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    const filters = fields.slice(1).map(field => [field, data.get(field)]);
    let visible = 0;
    for (const card of cards) {
      const searchable = card.dataset.index.toLocaleLowerCase();
      const match = terms.every(term => searchable.includes(term)) && filters.every(([field, value]) => !value || card.dataset[field] === value);
      card.hidden = !match;
      visible += Number(match);
    }
    count.textContent = `显示 ${visible} 组站群，共 ${cards.length} 组`;
    empty.hidden = visible > 0;
    if (writeQuery) {
      const url = new URL(location.href);
      for (const field of fields) {
        const value = String(data.get(field) || "").trim();
        if (value) url.searchParams.set(field, value);
        else url.searchParams.delete(field);
      }
      history.replaceState(null, "", url);
    }
  }

  readQuery();
  refresh(false);
  form.addEventListener("input", () => refresh(true));
  form.addEventListener("submit", event => { event.preventDefault(); refresh(true); });
  form.addEventListener("reset", event => {
    event.preventDefault();
    for (const field of fields) form.elements.namedItem(field).value = "";
    refresh(true);
  });
  window.addEventListener("popstate", () => { readQuery(); refresh(false); });
}
