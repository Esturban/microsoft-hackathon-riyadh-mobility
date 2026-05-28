export async function getJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Request failed for ${path}: ${response.status}`);
  }
  return response.json();
}

export const api = {
  getConfig: () => getJson("/api/config"),
  getRoutes: () => getJson("/api/routes"),
  getRouteGeojson: (mode) => getJson(`/api/routes/geojson?mode=${mode}`),
  getDistricts: () => getJson("/api/districts"),
  getScore: (districtId) => getJson(`/api/score?districtId=${districtId}`),
  getLiveEvents: () => getJson("/api/live-events"),
  getDataStatus: () => getJson("/api/data-status"),
};
