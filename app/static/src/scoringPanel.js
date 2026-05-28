export function renderScore(scoreResponse) {
  const { item } = scoreResponse;
  document.getElementById("kpi-district").textContent = item.name;
  document.getElementById("kpi-score").textContent = `${item.accessibilityScore} (${item.accessibilityRating})`;
  document.getElementById("score-text").textContent =
    `${item.name} scores ${item.accessibilityScore} (${item.accessibilityRating}) from ` +
    `${item.nearbyMetroCount} nearby metro lines, ${item.nearbyBusCount} nearby bus routes, and ` +
    `${item.liveDelayPenalty} delay penalties inside the 1.5 km access buffer.`;
}

export function renderKpis(routeItems) {
  const metroCount = routeItems.filter((item) => item.mode === "metro").length;
  const busCount = routeItems.filter((item) => item.mode === "bus").length;
  document.getElementById("kpi-metro").textContent = String(metroCount);
  document.getElementById("kpi-bus").textContent = String(busCount);
}

export function renderDebug(dataStatus) {
  document.getElementById("debug-panel").textContent = JSON.stringify(dataStatus, null, 2);
  document.getElementById("data-status-badge").textContent = `Data mode: ${dataStatus.activeMode}`;
}
