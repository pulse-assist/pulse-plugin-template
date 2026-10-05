// Страница плагина. Работает во фрейме Пульса без доступа к cookie: все запросы — через window.pulse.
//   pulse.plugin(path, {method, params, body}) — свой сервер плагина
//   pulse.api(path, {params})                   — API Пульса в пределах прав из манифеста
//   pulse.command(name, args)                   — команда плагина
//   pulse.openCard(id), pulse.chat(text), pulse.setState("summary?x=1"), pulse.state

const LABELS = { task: "Задачи", signal: "Сигналы", knowledge: "Знания" };

async function load() {
  const tiles = document.getElementById("tiles");
  try {
    const data = await pulse.plugin("/summary");
    document.getElementById("title").textContent = `${data.greeting}! Вот сводка`;
    tiles.innerHTML = Object.entries(data.counts).map(([kind, n]) => `
      <div class="pl-card">
        <div class="pl-kpi-label">${LABELS[kind] ?? kind}</div>
        <div class="pl-kpi-value pl-type-${kind}">${n}</div>
      </div>`).join("");
  } catch (e) {
    tiles.innerHTML = `<div class="pl-error">Не удалось загрузить: ${e.message}</div>`;
  }
}

document.getElementById("check").addEventListener("click", async () => {
  const out = document.getElementById("result");
  out.textContent = "Проверяю…";
  try {
    const r = await pulse.command("check", {});
    out.textContent = r.signal ? `Открытых задач ${r.open_tasks} — завёл сигнал` : `Открытых задач ${r.open_tasks} — всё в порядке`;
    if (r.signal) pulse.openCard(r.signal);
  } catch (e) {
    out.textContent = `Ошибка: ${e.message}`;
  }
});

pulse.setState("summary");
load();
