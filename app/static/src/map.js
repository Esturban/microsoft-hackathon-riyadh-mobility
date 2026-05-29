import { LAYER_IDS, makeCirclePolygon } from "./layers.js";

const INTERNAL_KEYS = new Set([
  "_rid", "_self", "_etag", "_attachments", "_ts", "_azureMapsShapeId",
  "geo_point_2d", "comments", "commentsar", "index",
]);

function formatTimestamp(ts) {
  if (!ts) return null;
  try {
    return new Date(ts).toLocaleString("en-SA", { dateStyle: "medium", timeStyle: "short" });
  } catch (_) {
    return ts;
  }
}

function severityColor(severity) {
  if (severity === "high")   return "#dc2626";
  if (severity === "medium") return "#d97706";
  return "#2563eb";
}

function row(label, value) {
  return `<div class="popup-row"><span>${label}</span><strong>${value}</strong></div>`;
}

function badge(icon, text, color) {
  return `<div class="popup-badge" style="background:${color}22;color:${color}">${icon} ${text}</div>`;
}

function popupHtml(properties) {
  const p = properties;

  if (p.eventType) {
    const color = severityColor(p.severity);
    const ts = formatTimestamp(p.timestampUtc);
    return `<div class="popup-card">
      ${badge("&#9888;", `${p.eventType} &middot; ${p.severity || "unknown"}`, color)}
      <div class="popup-title">${p.routeId || "Unknown route"}</div>
      <div class="popup-rows">
        ${p.delayMinutes != null ? row("Delay", `${p.delayMinutes} min`) : ""}
        ${p.districtId ? row("District", p.districtId) : ""}
        ${ts ? row("Time", ts) : ""}
        ${p.source ? row("Source", p.source) : ""}
      </div>
    </div>`;
  }

  if (p.mode === "metro" || p.metroline) {
    const color = p.lineColor || p.m_linecolorcode || "#888";
    const terminals = p.metroterminalstations || "";
    return `<div class="popup-card">
      ${badge("&#9644;", "Metro line", color)}
      <div class="popup-title">${p.name || p.metrolinename || "Metro Line"}</div>
      ${p.metrolinenamear ? `<div class="popup-subtitle">${p.metrolinenamear}</div>` : ""}
      <div class="popup-rows">
        ${terminals ? row("Terminals", terminals) : ""}
        ${p.source ? row("Source", p.source) : ""}
      </div>
    </div>`;
  }

  if (p.mode === "bus" || p.busroutecode) {
    const origin = p.origin && p.origin !== "NA" ? p.origin : null;
    const dest   = p.destination && p.destination !== "NA" ? p.destination : null;
    return `<div class="popup-card">
      ${badge("&#9656;", "Bus route", "#ea580c")}
      <div class="popup-title">${p.name || p.busroutecode || "Bus Route"}</div>
      <div class="popup-rows">
        ${origin ? row("From", origin) : ""}
        ${dest   ? row("To",   dest)   : ""}
        ${p.direction != null ? row("Direction", p.direction) : ""}
      </div>
    </div>`;
  }

  const entries = Object.entries(p)
    .filter(([k, v]) => !INTERNAL_KEYS.has(k) && v !== null && v !== "" && v !== "NA");
  return `<div class="popup-card"><div class="popup-rows">
    ${entries.map(([k, v]) => row(k, v)).join("")}
  </div></div>`;
}

function fitRiyadhView(map, center) {
  map.setCamera({ center: [center.lon, center.lat], zoom: 10 });
}

export function createMap(config, domIds) {
  const hasAtlas = typeof atlas !== "undefined" && config.azureMapsEnabled;
  if (!hasAtlas) {
    document.getElementById(domIds.fallbackId).classList.remove("hidden");
    return createLeafletMap(config, domIds.mapId);
  }

  const map = new atlas.Map(domIds.mapId, {
    center: [config.riyadhCenter.lon, config.riyadhCenter.lat],
    zoom: 10,
    style: "road",
    authOptions: {
      authType: "subscriptionKey",
      subscriptionKey: window.__AZURE_MAPS_KEY__,
    },
  });

  const ready = new Promise((resolve) => {
    map.events.add("ready", () => {
      fitRiyadhView(map, config.riyadhCenter);
      resolve();
    });
  });

  return { engine: "atlas", instance: map, ready };
}

function installPopup(map) {
  const popup = new atlas.Popup({ closeButton: true, pixelOffset: [0, -18] });
  const layers = [LAYER_IDS.metroLayer, LAYER_IDS.busLayer, LAYER_IDS.eventsLayer]
    .map((layerId) => map.layers.getLayerById(layerId))
    .filter(Boolean);

  layers.forEach((layer) => {
    map.events.add("click", layer, (event) => {
      const shape = event.shapes?.[0];
      if (!shape) {
        return;
      }
      popup.setOptions({
        content: `<div style="padding:12px 14px">${popupHtml(shape.getProperties())}</div>`,
        position: event.position,
      });
      popup.open(map);
    });
  });
}

function createLeafletMap(config, mapId) {
  const map = L.map(mapId, {
    zoomControl: true,
    attributionControl: true,
  }).setView([config.riyadhCenter.lat, config.riyadhCenter.lon], 10);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  return {
    engine: "leaflet",
    instance: map,
    layers: {},
    ready: Promise.resolve(),
  };
}

async function waitForMapReady(map) {
  if (!map) {
    return;
  }
  await (map.ready ?? Promise.resolve());
}

export async function renderSources(map, data) {
  if (!map) {
    return;
  }

  await waitForMapReady(map);

  if (map.engine === "leaflet") {
    renderLeafletSources(map, data);
    return;
  }

  const atlasMap = map.instance;

  const addOrReplaceSource = (sourceId, payload) => {
    if (atlasMap.sources.getById(sourceId)) {
      atlasMap.sources.remove(sourceId);
    }
    const source = new atlas.source.DataSource(sourceId);
    atlasMap.sources.add(source);
    source.add(payload);
    return source;
  };

  addOrReplaceSource(LAYER_IDS.metroSource, data.metro.geojson);
  addOrReplaceSource(LAYER_IDS.busSource, data.bus.geojson);
  addOrReplaceSource(
    LAYER_IDS.districtSource,
    {
      type: "FeatureCollection",
      features: data.districts.items.map((item) => ({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [item.center.lon, item.center.lat],
        },
        properties: { name: item.name, districtId: item.districtId },
      })),
    }
  );
  addOrReplaceSource(
    LAYER_IDS.eventsSource,
    {
      type: "FeatureCollection",
      features: data.events.items.map((item) => ({
        type: "Feature",
        geometry: { type: "Point", coordinates: [item.lon, item.lat] },
        properties: item,
      })),
    }
  );
  addOrReplaceSource(
    LAYER_IDS.bufferSource,
    { type: "FeatureCollection", features: [] }
  );

  if (!atlasMap.layers.getLayerById(LAYER_IDS.metroLayer)) {
    atlasMap.layers.add(
      new atlas.layer.LineLayer(LAYER_IDS.metroSource, LAYER_IDS.metroLayer, {
        strokeColor: ["coalesce", ["get", "lineColor"], "#1f77b4"],
        strokeWidth: 6,
      })
    );
    atlasMap.layers.add(
      new atlas.layer.LineLayer(LAYER_IDS.busSource, LAYER_IDS.busLayer, {
        strokeColor: "#f97316",
        strokeWidth: 3,
        strokeDashArray: [2, 1],
      })
    );
    atlasMap.layers.add(
      new atlas.layer.BubbleLayer(LAYER_IDS.districtSource, LAYER_IDS.districtLayer, {
        radius: 6,
        color: "#111827",
        strokeWidth: 2,
        strokeColor: "#f8fafc",
      })
    );
    atlasMap.layers.add(
      new atlas.layer.BubbleLayer(LAYER_IDS.eventsSource, LAYER_IDS.eventsLayer, {
        radius: 8,
        color: "#dc2626",
        strokeColor: "#fff7ed",
        strokeWidth: 2,
      })
    );
    atlasMap.layers.add(
      new atlas.layer.PolygonLayer(LAYER_IDS.bufferSource, LAYER_IDS.bufferLayer, {
        fillColor: "rgba(37, 99, 235, 0.15)",
        strokeColor: "#2563eb",
        strokeWidth: 2,
      })
    );

    if (!atlasMap.__popupInstalled) {
      installPopup(atlasMap);
      atlasMap.__popupInstalled = true;
    }
  }
}

export async function setLayerVisibility(map, layerId, visible) {
  if (!map) {
    return;
  }

  await waitForMapReady(map);

  if (map.engine === "leaflet") {
    const layer = map.layers?.[layerId];
    if (!layer) {
      return;
    }
    if (visible) {
      layer.addTo(map.instance);
    } else {
      layer.remove();
    }
    return;
  }

  const atlasMap = map.instance;
  if (!atlasMap.layers.getLayerById(layerId)) {
    return;
  }
  atlasMap.layers.getLayerById(layerId).setOptions({ visible });
}

export async function focusDistrict(map, district, radiusKm) {
  if (!map || !district) {
    return;
  }

  await waitForMapReady(map);

  if (map.engine === "leaflet") {
    const leafletMap = map.instance;
    const layer = map.layers[LAYER_IDS.bufferLayer];
    if (layer) {
      layer.clearLayers();
      layer.addData(makeCirclePolygon(district.center, radiusKm));
    }
    leafletMap.setView([district.center.lat, district.center.lon], 12);
    return;
  }

  const atlasMap = map.instance;
  const source = atlasMap.sources.getById(LAYER_IDS.bufferSource);
  source.clear();
  source.add(makeCirclePolygon(district.center, radiusKm));
  atlasMap.setCamera({
    center: [district.center.lon, district.center.lat],
    zoom: 12,
  });
}

function renderLeafletSources(map, data) {
  const leafletMap = map.instance;
  const districtGeojson = {
    type: "FeatureCollection",
    features: data.districts.items.map((item) => ({
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [item.center.lon, item.center.lat],
      },
      properties: { name: item.name, districtId: item.districtId },
    })),
  };
  const eventsGeojson = {
    type: "FeatureCollection",
    features: data.events.items.map((item) => ({
      type: "Feature",
      geometry: { type: "Point", coordinates: [item.lon, item.lat] },
      properties: item,
    })),
  };

  const replaceLayer = (layerId, layer) => {
    if (map.layers[layerId]) {
      map.layers[layerId].remove();
    }
    map.layers[layerId] = layer;
    layer.addTo(leafletMap);
  };

  replaceLayer(
    LAYER_IDS.metroLayer,
    L.geoJSON(data.metro.geojson, {
      style: (feature) => ({
        color: feature.properties.lineColor || "#1f77b4",
        weight: 6,
      }),
      onEachFeature: (feature, layer) => {
        layer.bindPopup(popupHtml(feature.properties));
      },
    })
  );

  replaceLayer(
    LAYER_IDS.busLayer,
    L.geoJSON(data.bus.geojson, {
      style: () => ({
        color: "#f97316",
        weight: 3,
        dashArray: "8 4",
      }),
      onEachFeature: (feature, layer) => {
        layer.bindPopup(popupHtml(feature.properties));
      },
    })
  );

  replaceLayer(
    LAYER_IDS.districtLayer,
    L.geoJSON(districtGeojson, {
      pointToLayer: (_, latlng) =>
        L.circleMarker(latlng, {
          radius: 6,
          color: "#f8fafc",
          weight: 2,
          fillColor: "#111827",
          fillOpacity: 1,
        }),
      onEachFeature: (feature, layer) => {
        layer.bindPopup(popupHtml(feature.properties));
      },
    })
  );

  replaceLayer(
    LAYER_IDS.eventsLayer,
    L.geoJSON(eventsGeojson, {
      pointToLayer: (_, latlng) =>
        L.circleMarker(latlng, {
          radius: 8,
          color: "#fff7ed",
          weight: 2,
          fillColor: "#dc2626",
          fillOpacity: 1,
        }),
      onEachFeature: (feature, layer) => {
        layer.bindPopup(popupHtml(feature.properties));
      },
    })
  );

  replaceLayer(
    LAYER_IDS.bufferLayer,
    L.geoJSON(
      { type: "FeatureCollection", features: [] },
      {
        style: () => ({
          color: "#2563eb",
          weight: 2,
          fillColor: "#2563eb",
          fillOpacity: 0.15,
        }),
      }
    )
  );
}
