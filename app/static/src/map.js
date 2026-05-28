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
    return createFallbackMap(domIds.mapId);
  }

  const map = new atlas.Map(domIds.mapId, {
    center: [config.riyadhCenter.lon, config.riyadhCenter.lat],
    zoom: 10,
    style: "road",
    authOptions: {
      authType: "subscriptionKey",
      subscriptionKey: config.azureMapsKey,
    },
  });

  map.events.add("ready", () => {
    fitRiyadhView(map, config.riyadhCenter);
    installPopup(map);
  });

  return map;
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

function createFallbackMap(mapId) {
  const root = document.getElementById(mapId);
  root.classList.add("fallback-map");
  root.innerHTML = `
    <div class="fallback-inner">
      <h3>Map placeholder</h3>
      <p>Provide an Azure Maps key to render live tiles.</p>
      <p>The district selector, score API, and debug panel remain fully functional.</p>
    </div>
  `;
  return null;
}

export function renderSources(map, data) {
  if (!map) {
    return;
  }

  const addOrReplaceSource = (sourceId, payload) => {
    if (map.sources.getById(sourceId)) {
      map.sources.remove(sourceId);
    }
    const source = new atlas.source.DataSource(sourceId);
    map.sources.add(source);
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

  if (!map.layers.getLayerById(LAYER_IDS.metroLayer)) {
    map.layers.add(
      new atlas.layer.LineLayer(LAYER_IDS.metroSource, LAYER_IDS.metroLayer, {
        strokeColor: ["coalesce", ["get", "lineColor"], "#1f77b4"],
        strokeWidth: 6,
      })
    );
    map.layers.add(
      new atlas.layer.LineLayer(LAYER_IDS.busSource, LAYER_IDS.busLayer, {
        strokeColor: "#f97316",
        strokeWidth: 3,
        strokeDashArray: [2, 1],
      })
    );
    map.layers.add(
      new atlas.layer.BubbleLayer(LAYER_IDS.districtSource, LAYER_IDS.districtLayer, {
        radius: 6,
        color: "#111827",
        strokeWidth: 2,
        strokeColor: "#f8fafc",
      })
    );
    map.layers.add(
      new atlas.layer.BubbleLayer(LAYER_IDS.eventsSource, LAYER_IDS.eventsLayer, {
        radius: 8,
        color: "#dc2626",
        strokeColor: "#fff7ed",
        strokeWidth: 2,
      })
    );
    map.layers.add(
      new atlas.layer.PolygonLayer(LAYER_IDS.bufferSource, LAYER_IDS.bufferLayer, {
        fillColor: "rgba(37, 99, 235, 0.15)",
        strokeColor: "#2563eb",
        strokeWidth: 2,
      })
    );
  }
}

export function setLayerVisibility(map, layerId, visible) {
  if (!map || !map.layers.getLayerById(layerId)) {
    return;
  }
  map.layers.getLayerById(layerId).setOptions({ visible });
}

export function focusDistrict(map, district, radiusKm) {
  if (!map || !district) {
    return;
  }
  const source = map.sources.getById(LAYER_IDS.bufferSource);
  source.clear();
  source.add(makeCirclePolygon(district.center, radiusKm));
  map.setCamera({
    center: [district.center.lon, district.center.lat],
    zoom: 12,
  });
}
