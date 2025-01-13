// Estimate MODIS Evapotranspiration (ET) Time Series Data using Earth Engine

// Visualize MODIS Evapotranspiration (ET) Data (Data provider: NASA LP DAAC at the USGS EROS Center)
var dataset = ee.ImageCollection('MODIS/061/MOD16A2')
                  .filter(ee.Filter.date('2023-01-01', '2023-05-01'))
                  .filterBounds(ROI);
var evapotranspiration = dataset.select('ET');

// Set visualization parameter
var evapotranspirationVis = {
  min: 0,
  max: 300,
  palette: [
    'ffffff', 'fcd163', '99b718', '66a000', '3e8601', '207401', '056201',
    '004c00', '011301'
  ],
};

Map.centerObject(ROI, 6);
Map.addLayer(evapotranspiration.mean().clip(ROI), evapotranspirationVis, 'Evapotranspiration');

// Import MODIS Evapotranspiration (EvT) Data for longer time series
var ET = ee.ImageCollection('MODIS/006/MOD16A2')
           .filter(ee.Filter.date('2018-01-01', '2023-12-31'))
           .filterBounds(ROI)
           .select('ET');

// Display ET annual variation
var chart = ui.Chart.image.doySeriesByYear(ET, 'ET', ROI, ee.Reducer.mean(), 500)
              .setOptions({
                title: 'Annual Variation of Evapotranspiration',
                hAxis: {title: 'Day of Year'},
                vAxis: {title: 'Evapotranspiration (mm)'},
                lineWidth: 1,
                pointSize: 3
              });
print(chart);

// Export the ET map for the defined ROI to Google Drive
var evapotranspirationExport = evapotranspiration.mean().clip(ROI);

Export.image.toDrive({
  image: evapotranspirationExport,
  description: 'ET_Map_ROI',
  scale: 500,
  region: ROI,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});
