function ratingClass(rating) {
  if (rating === "High") return "rating-high";
  if (rating === "Medium") return "rating-medium";
  return "rating-low";
}

function barRow(label, value, maxValue, color) {
  const pct = maxValue > 0 ? Math.min(100, (value / maxValue) * 100) : 0;
  return `
    <div class="score-bar-row">
      <div class="score-bar-label">
        <span>${label}</span>
        <span><strong>${value}</strong></span>
      </div>
      <div class="score-bar-track">
        <div class="score-bar-fill" style="width:${pct}%;background:${color}"></div>
      </div>
    </div>`;
}

export function renderScore(scoreResponse) {
  const { item } = scoreResponse;
  const rating = item.accessibilityRating;
  const maxScore = 24;

  document.getElementById("kpi-district").textContent = item.name;
  document.getElementById("kpi-score").textContent =
    `${item.accessibilityScore} · ${rating}`;

  document.getElementById("score-text").classList.add("hidden");

  const detail = document.getElementById("score-detail");
  detail.classList.remove("hidden");

  document.getElementById("score-bars").innerHTML = `
    <div class="score-bar-row">
      <div class="score-bar-label">
        <span>
          Total score: <strong>${item.accessibilityScore}</strong>
          &ensp;<span class="rating-badge ${ratingClass(rating)}">${rating}</span>
        </span>
        <span style="font-size:0.73rem;color:var(--muted)">of ~${maxScore} max</span>
      </div>
      <div class="score-bar-track">
        <div class="score-bar-fill" style="width:${Math.min(100, (item.accessibilityScore / maxScore) * 100)}%;background:var(--blue)"></div>
      </div>
    </div>
    ${barRow("Nearby metro lines (×3 pts)", item.nearbyMetroCount, 4, "#00ade5")}
    ${barRow("Nearby bus routes (×1 pt)", item.nearbyBusCount, 12, "#f97316")}
    ${item.liveDelayPenalty > 0 ? barRow("Delay events (−1 pt each)", item.liveDelayPenalty, 5, "#dc2626") : ""}
  `;

  const f = typeof item.formula === "object" && item.formula
    ? item.formula
    : { nearbyMetroCount: item.nearbyMetroCount, nearbyBusCount: item.nearbyBusCount, liveDelayPenalty: item.liveDelayPenalty };
  document.getElementById("formula-text").textContent =
    `score = (${f.nearbyMetroCount ?? item.nearbyMetroCount} × 3) + ${f.nearbyBusCount ?? item.nearbyBusCount} − ${f.liveDelayPenalty ?? item.liveDelayPenalty} = ${item.accessibilityScore}`;
}

export function renderKpis(routeItems) {
  const metroCount = routeItems.filter((item) => item.mode === "metro").length;
  const busCount = routeItems.filter((item) => item.mode === "bus").length;
  document.getElementById("kpi-metro").textContent = String(metroCount);
  document.getElementById("kpi-bus").textContent = String(busCount);
  document.getElementById("hs-metro").textContent = String(metroCount);
  document.getElementById("hs-bus").textContent = String(busCount);
}

export function renderDebug(dataStatus) {
  document.getElementById("debug-panel").textContent =
    JSON.stringify(dataStatus, null, 2);
  document.getElementById("data-status-badge").textContent =
    `Data: ${dataStatus.activeMode}`;
}

export function renderDistrictInfo(district) {
  const panel = document.getElementById("district-info");
  if (!district) {
    panel.classList.add("hidden");
    return;
  }
  panel.classList.remove("hidden");
  document.getElementById("district-info-name").textContent = district.name;
  const arEl = document.getElementById("district-info-ar");
  arEl.textContent = district.nameAr || "";
  arEl.style.display = district.nameAr ? "" : "none";
  document.getElementById("district-info-desc").textContent =
    district.description || "";
}
