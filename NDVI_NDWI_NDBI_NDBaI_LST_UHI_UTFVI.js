Map.addLayer(aoi);

var startDate = '1993-04-09';
var endDate = '1993-04-11';

function applyScaleFactors(image) {
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);
  return image.addBands(opticalBands, null, true)
              .addBands(thermalBands, null, true);
}

// Cloud mask function for Landsat 5
function maskL5sr(col) {
  var cloudShadowBitMask = (1 << 3);
  var cloudsBitMask = (1 << 5);
  var qa = col.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
               .and(qa.bitwiseAnd(cloudsBitMask).eq(0));
  return col.updateMask(mask);
}

// Filter the collection, first by the aoi, and then by date.
var image = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
  .filterDate(startDate, endDate)
  .filterBounds(aoi)
  .map(applyScaleFactors)
  .map(maskL5sr)
  .median();

var visualization = {
  bands: ['SR_B3', 'SR_B2', 'SR_B1'],
  min: 0.0,
  max: 0.3,
};

Map.addLayer(image, visualization, 'True Color (321)', false);

// NDVI
var ndvi  = image.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI');
Map.addLayer(ndvi, {min: -1, max: 1, palette: ['blue', 'white', 'green']}, 'NDVI', false);

// NDWI
var ndwi = image.normalizedDifference(['SR_B2', 'SR_B4']).rename('NDWI');
Map.addLayer(ndwi, {min: -1, max: 1, palette: ['blue', 'white', 'green']}, 'NDWI', false);

// NDBI
var ndbi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDBI');
Map.addLayer(ndbi, {min: -1, max: 1, palette: ['blue', 'white', 'red']}, 'NDBI', false);

// NDBaI
var ndbaI = image.normalizedDifference(['SR_B5', 'SR_B7']).rename('NDBaI');
Map.addLayer(ndbaI, {min: -1, max: 1, palette: ['blue', 'white', 'brown']}, 'NDBaI', false);

// LST Calculation
var ndvi_min = ee.Number(ndvi.reduceRegion({
  reducer: ee.Reducer.min(),
  geometry: aoi,
  scale: 30,
  maxPixels: 1e9
}).values().get(0));

var ndvi_max = ee.Number(ndvi.reduceRegion({
  reducer: ee.Reducer.max(),
  geometry: aoi,
  scale: 30,
  maxPixels: 1e9
}).values().get(0));

var fv = ndvi.subtract(ndvi_min).divide(ndvi_max.subtract(ndvi_min)).pow(ee.Number(2)).rename('FV');
var em = fv.multiply(ee.Number(0.004)).add(ee.Number(0.986)).rename('EM');
var thermal = image.select('ST_B6').rename('thermal');
var lst = thermal.expression(
  '(tb / (1 + (0.00115 * (tb / 0.48359547432)) * log(em))) - 273.15',
  {'tb': thermal.select('thermal'), 'em': em}
).rename('LST');
Map.addLayer(lst, {min: 25, max: 50, palette: [
  '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
  '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
  '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
  'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
  'ff0000', 'de0101', 'c21301', 'a71001', '911003'
]}, 'LST AOI');

// UHI
var lst_mean = ee.Number(lst.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: aoi,
  scale: 30,
  maxPixels: 1e9
}).values().get(0));

var lst_std = ee.Number(lst.reduceRegion({
  reducer: ee.Reducer.stdDev(),
  geometry: aoi,
  scale: 30,
  maxPixels: 1e9
}).values().get(0));

var uhi = lst.subtract(lst_mean).divide(lst_std).rename('UHI');
Map.addLayer(uhi, {min: -4, max: 4, palette: ['313695', '74add1', 'fed976', 'feb24c', 'fd8d3c', 'fc4e2a', 'e31a1c', 'b10026']}, 'UHI AOI');

// UTFVI
var utfvi = lst.subtract(lst_mean).divide(lst).rename('UTFVI');
Map.addLayer(utfvi, {min: -1, max: 0.3, palette: ['313695', '74add1', 'fed976', 'feb24c', 'fd8d3c', 'fc4e2a', 'e31a1c', 'b10026']}, 'UTFVI AOI');

// Export all layers to Drive
var layers = [
  {name: 'NDVI', image: ndvi},
  {name: 'NDWI', image: ndwi},
  {name: 'NDBI', image: ndbi},
  {name: 'NDBaI', image: ndbaI},
  {name: 'LST', image: lst},
  {name: 'UHI', image: uhi},
  {name: 'UTFVI', image: utfvi}
];

layers.forEach(function(layer) {
  Export.image.toDrive({
    image: layer.image.clip(aoi),
    description: layer.name + '_Export',
    scale: 30,
    region: aoi,
    fileFormat: 'GeoTIFF',
    maxPixels: 1e9
  });
});

// Export True Color as GeoTIFF
Export.image.toDrive({
  image: image.select(['SR_B3', 'SR_B2', 'SR_B1']).clip(aoi),
  description: 'TrueColor_Masked',
  scale: 30,
  region: aoi,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e9
});
