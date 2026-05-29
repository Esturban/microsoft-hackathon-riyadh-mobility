import { LAYER_IDS, makeCirclePolygon } from "./layers.js";

function popupHtml(properties) {
  return Object.entries(properties)
    .map(([key, value]) => `<div><strong>${key}</strong>: ${value}</div>`)
    .join("");
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
      installPopup(map);
      resolve();
    });
  });

  return { engine: "atlas", instance: map, ready };
}

function installPopup(map) {
  const popup = new atlas.Popup({ closeButton: true, pixelOffset: [0, -18] });
  [LAYER_IDS.metroLayer, LAYER_IDS.busLayer, LAYER_IDS.eventsLayer].forEach((layerId) => {
    map.events.add("click", layerId, (event) => {
      const shape = event.shapes?.[0];
      if (!shape) {
        return;
      }
      popup.setOptions({
        content: `<div class="popup">${popupHtml(shape.getProperties())}</div>`,
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
