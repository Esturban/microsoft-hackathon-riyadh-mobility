export const LAYER_IDS = {
  metroSource: "metro-source",
  busSource: "bus-source",
  districtSource: "district-source",
  eventsSource: "events-source",
  bufferSource: "buffer-source",
  metroLayer: "metro-layer",
  busLayer: "bus-layer",
  districtLayer: "district-layer",
  eventsLayer: "events-layer",
  bufferLayer: "buffer-layer",
};

export function makeCirclePolygon(center, radiusKm, steps = 48) {
  const earthRadiusKm = 6371;
  const points = [];
  const latRadians = (center.lat * Math.PI) / 180;
  const lonRadians = (center.lon * Math.PI) / 180;
  const angularDistance = radiusKm / earthRadiusKm;

  for (let i = 0; i <= steps; i += 1) {
    const bearing = (2 * Math.PI * i) / steps;
    const lat2 = Math.asin(
      Math.sin(latRadians) * Math.cos(angularDistance) +
        Math.cos(latRadians) * Math.sin(angularDistance) * Math.cos(bearing)
    );
    const lon2 =
      lonRadians +
      Math.atan2(
        Math.sin(bearing) * Math.sin(angularDistance) * Math.cos(latRadians),
        Math.cos(angularDistance) - Math.sin(latRadians) * Math.sin(lat2)
      );
    points.push([(lon2 * 180) / Math.PI, (lat2 * 180) / Math.PI]);
  }

  return {
    type: "Feature",
    geometry: { type: "Polygon", coordinates: [points] },
    properties: {},
  };
}
