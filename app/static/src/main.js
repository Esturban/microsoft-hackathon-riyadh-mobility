import { api } from "./api.js";
import { LAYER_IDS } from "./layers.js";
import { createMap, focusDistrict, renderSources, setLayerVisibility } from "./map.js";
import { renderDebug, renderDistrictInfo, renderKpis, renderScore } from "./scoringPanel.js";

async function boot() {
  window.__AZURE_MAPS_KEY__ = document
    .querySelector('meta[name="azure-maps-key"]')
    ?.getAttribute("content");

  const [config, routes, metro, bus, districts, events, dataStatus] = await Promise.all([
    api.getConfig(),
    api.getRoutes(),
    api.getRouteGeojson("metro"),
    api.getRouteGeojson("bus"),
    api.getDistricts(),
    api.getLiveEvents(),
    api.getDataStatus(),
  ]);

  const map = createMap(config, { mapId: "map", fallbackId: "map-fallback" });
  await renderSources(map, { metro, bus, districts, events });
  renderKpis(routes.items);
  renderDebug(dataStatus);
  const dsCount = document.getElementById("hs-districts");
  if (dsCount) dsCount.textContent = String(districts.items.length);
  bindControls(map, config, districts.items);

  document.getElementById("maps-status-badge").textContent = config.azureMapsEnabled
    ? "Azure Maps"
    : "OpenStreetMap fallback";

  if (districts.items.length > 0) {
    await selectDistrict(map, config.accessBufferKm, districts.items[0]);
  }
}

function bindControls(map, config, districts) {
  const selector = document.getElementById("district-select");
  selector.innerHTML = districts
    .map((district) => `<option value="${district.districtId}">${district.name}</option>`)
    .join("");

  selector.addEventListener("change", async (event) => {
    const district = districts.find((item) => item.districtId === event.target.value);
    await selectDistrict(map, config.accessBufferKm, district);
  });

  document.getElementById("toggle-metro").addEventListener("change", (event) => {
    void setLayerVisibility(map, LAYER_IDS.metroLayer, event.target.checked);
  });
  document.getElementById("toggle-bus").addEventListener("change", (event) => {
    void setLayerVisibility(map, LAYER_IDS.busLayer, event.target.checked);
  });
  document.getElementById("toggle-events").addEventListener("change", (event) => {
    void setLayerVisibility(map, LAYER_IDS.eventsLayer, event.target.checked);
  });
}

async function selectDistrict(map, accessBufferKm, district) {
  if (!district) {
    return;
  }
  const score = await api.getScore(district.districtId);
  renderScore(score);
  renderDistrictInfo(district);
  await focusDistrict(map, district, accessBufferKm);
}

boot().catch((error) => {
  console.error(error);
  document.getElementById("debug-panel").textContent = error.stack || String(error);
});
