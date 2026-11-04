-- ====================================================================
-- Agricultural Crop Production Analysis System
-- Synthetic Database Seed Script (MySQL 8.0+)
-- ====================================================================

USE crop_analysis_db;

-- Clear previous data in correct foreign key order
DELETE FROM crop_records;
DELETE FROM crops;
DELETE FROM regions;

-- --------------------------------------------------------------------
-- Seed Regions
-- --------------------------------------------------------------------
INSERT INTO regions (id, name, state, climate_zone) VALUES
(1, 'Punjab', 'Punjab', 'Subtropical Humid'),
(2, 'Maharashtra', 'Maharashtra', 'Tropical Semi-Arid'),
(3, 'Karnataka', 'Karnataka', 'Tropical Wet and Dry');

-- --------------------------------------------------------------------
-- Seed Crops
-- --------------------------------------------------------------------
INSERT INTO crops (id, name, category, default_unit) VALUES
(1, 'Wheat', 'Cereal', 'Metric Tonnes'),
(2, 'Rice', 'Cereal', 'Metric Tonnes'),
(3, 'Maize', 'Cereal', 'Metric Tonnes'),
(4, 'Cotton', 'Commercial', 'Metric Tonnes'),
(5, 'Sugarcane', 'Commercial', 'Metric Tonnes');

-- --------------------------------------------------------------------
-- Seed Crop Records (Synthetic 5-Year Time Series 2019-2023)
-- --------------------------------------------------------------------
INSERT INTO crop_records (crop_id, region_id, year, area_cultivated, area_unit, production_quantity, production_unit, annual_rainfall, notes) VALUES
-- 2019
(1, 1, 2019, 3500.0, 'Hectares', 16800.0, 'Metric Tonnes', 610.5, 'Adequate canal irrigation'),
(2, 1, 2019, 3100.0, 'Hectares', 12400.0, 'Metric Tonnes', 650.0, 'Normal monsoon onset'),
(3, 1, 2019, 1200.0, 'Hectares', 4560.0, 'Metric Tonnes', 580.0, 'Kharif crop'),
(4, 1, 2019, 1800.0, 'Hectares', 3960.0, 'Metric Tonnes', NULL, 'Rainfall unrecorded'),
(5, 1, 2019, 950.0, 'Hectares', 76000.0, 'Metric Tonnes', 620.0, 'High water table harvest'),

(1, 2, 2019, 2200.0, 'Hectares', 6600.0, 'Metric Tonnes', 890.0, 'Rabi crop in Vidarbha'),
(2, 2, 2019, 3800.0, 'Hectares', 11400.0, 'Metric Tonnes', 1250.5, 'Konkan coastal belt'),
(3, 2, 2019, 1900.0, 'Hectares', 6270.0, 'Metric Tonnes', NULL, 'Sensor maintenance'),
(4, 2, 2019, 3200.0, 'Hectares', 6400.0, 'Metric Tonnes', 920.0, 'Black cotton soil tract'),
(5, 2, 2019, 1600.0, 'Hectares', 136000.0, 'Metric Tonnes', 1100.0, 'Western Maharashtra cooperative'),

(1, 3, 2019, 1400.0, 'Hectares', 3920.0, 'Metric Tonnes', 750.0, 'Northern dry zone'),
(2, 3, 2019, 2900.0, 'Hectares', 9860.0, 'Metric Tonnes', 1180.0, 'Tunga-Bhadra basin'),
(3, 3, 2019, 2100.0, 'Hectares', 7770.0, 'Metric Tonnes', 810.0, 'Davangere grain belt'),
(4, 3, 2019, 1650.0, 'Hectares', 3300.0, 'Metric Tonnes', 730.0, 'Dharwad hybrid cotton'),
(5, 3, 2019, 1200.0, 'Hectares', 98400.0, 'Metric Tonnes', NULL, 'Missing meteorological record'),

-- 2020
(1, 1, 2020, 3550.0, 'Hectares', 17395.0, 'Metric Tonnes', 590.0, 'Favorable cold spell'),
(2, 1, 2020, 3150.0, 'Hectares', 12915.0, 'Metric Tonnes', 640.0, 'Direct seeded rice trials'),
(3, 1, 2020, 1250.0, 'Hectares', 4875.0, 'Metric Tonnes', NULL, 'Gauges missed in zone'),
(4, 1, 2020, 1750.0, 'Hectares', 3675.0, 'Metric Tonnes', 560.0, 'Mild whitefly impact'),
(5, 1, 2020, 980.0, 'Hectares', 79380.0, 'Metric Tonnes', 610.0, 'Good ratoon crop'),

(1, 2, 2020, 2300.0, 'Hectares', 7130.0, 'Metric Tonnes', 960.0, 'Abundant dew'),
(2, 2, 2020, 3850.0, 'Hectares', 12320.0, 'Metric Tonnes', 1320.0, 'Heavy monsoon showers'),
(3, 2, 2020, 2000.0, 'Hectares', 6800.0, 'Metric Tonnes', 940.0, 'Marathwada harvest'),
(4, 2, 2020, 3300.0, 'Hectares', 6930.0, 'Metric Tonnes', 980.0, 'Extended picking cycle'),
(5, 2, 2020, 1650.0, 'Hectares', 143550.0, 'Metric Tonnes', 1150.0, 'Kolhapur bumper yield'),

(1, 3, 2020, 1450.0, 'Hectares', 4205.0, 'Metric Tonnes', 780.0, 'Belagavi plateau'),
(2, 3, 2020, 2950.0, 'Hectares', 10325.0, 'Metric Tonnes', 1240.0, 'Cauvery delta support'),
(3, 3, 2020, 2200.0, 'Hectares', 8360.0, 'Metric Tonnes', NULL, 'Station offline'),
(4, 3, 2020, 1700.0, 'Hectares', 3570.0, 'Metric Tonnes', 760.0, 'Raichur black soil'),
(5, 3, 2020, 1250.0, 'Hectares', 105000.0, 'Metric Tonnes', 1020.0, 'Mandya sugarcane corridor'),

-- 2021
(1, 1, 2021, 3600.0, 'Hectares', 18000.0, 'Metric Tonnes', 570.0, 'High yielding variety PBW'),
(2, 1, 2021, 3200.0, 'Hectares', 13440.0, 'Metric Tonnes', 680.0, 'Basmati export share'),
(3, 1, 2021, 1300.0, 'Hectares', 5330.0, 'Metric Tonnes', 590.0, 'Diversified grain production'),
(4, 1, 2021, 1700.0, 'Hectares', 3400.0, 'Metric Tonnes', 550.0, 'Pink bollworm alert'),
(5, 1, 2021, 1000.0, 'Hectares', 82000.0, 'Metric Tonnes', 630.0, 'Stable mill crushing'),

(1, 2, 2021, 2350.0, 'Hectares', 7520.0, 'Metric Tonnes', 1020.0, 'Good reservoir storage'),
(2, 2, 2021, 3900.0, 'Hectares', 12870.0, 'Metric Tonnes', 1400.0, 'Substantial precipitation'),
(3, 2, 2021, 2050.0, 'Hectares', 7380.0, 'Metric Tonnes', 990.0, 'Poultry feed demand'),
(4, 2, 2021, 3400.0, 'Hectares', 7480.0, 'Metric Tonnes', NULL, 'Station gauge broken'),
(5, 2, 2021, 1700.0, 'Hectares', 151300.0, 'Metric Tonnes', 1210.0, 'High sugar recovery'),

(1, 3, 2021, 1500.0, 'Hectares', 4500.0, 'Metric Tonnes', 810.0, 'Bagalkot irrigated sector'),
(2, 3, 2021, 3000.0, 'Hectares', 10800.0, 'Metric Tonnes', 1290.0, 'Shimoga malnad belt'),
(3, 3, 2021, 2300.0, 'Hectares', 9200.0, 'Metric Tonnes', 840.0, 'Hybrid seed dominance'),
(4, 3, 2021, 1750.0, 'Hectares', 3850.0, 'Metric Tonnes', 790.0, 'Ballari district'),
(5, 3, 2021, 1300.0, 'Hectares', 111800.0, 'Metric Tonnes', 1060.0, 'Kaveri basin mills'),

-- 2022
(1, 1, 2022, 3650.0, 'Hectares', 17885.0, 'Metric Tonnes', 540.0, 'Early March heatwave'),
(2, 1, 2022, 3220.0, 'Hectares', 13846.0, 'Metric Tonnes', 660.0, 'Stable water pump delivery'),
(3, 1, 2022, 1320.0, 'Hectares', 5544.0, 'Metric Tonnes', 570.0, 'Spring maize crop'),
(4, 1, 2022, 1650.0, 'Hectares', 3135.0, 'Metric Tonnes', NULL, 'Sensor outage'),
(5, 1, 2022, 1020.0, 'Hectares', 84660.0, 'Metric Tonnes', 600.0, 'Variety Co-0238'),

(1, 2, 2022, 2400.0, 'Hectares', 7440.0, 'Metric Tonnes', 910.0, 'Dry spell in February'),
(2, 2, 2022, 3950.0, 'Hectares', 13035.0, 'Metric Tonnes', 1280.0, 'Moderate monsoon phase'),
(3, 2, 2022, 2100.0, 'Hectares', 7560.0, 'Metric Tonnes', 920.0, 'Steady regional pricing'),
(4, 2, 2022, 3450.0, 'Hectares', 7245.0, 'Metric Tonnes', 930.0, 'Bt cotton cultivation'),
(5, 2, 2022, 1750.0, 'Hectares', 154000.0, 'Metric Tonnes', 1170.0, 'Drip irrigation expansion'),

(1, 3, 2022, 1520.0, 'Hectares', 4408.0, 'Metric Tonnes', 760.0, 'Koppal district'),
(2, 3, 2022, 3050.0, 'Hectares', 10980.0, 'Metric Tonnes', 1220.0, 'Krishna basin water release'),
(3, 3, 2022, 2350.0, 'Hectares', 9165.0, 'Metric Tonnes', 800.0, 'Fodder and grain utility'),
(4, 3, 2022, 1800.0, 'Hectares', 3780.0, 'Metric Tonnes', 750.0, 'Haveri market yard'),
(5, 3, 2022, 1320.0, 'Hectares', 112200.0, 'Metric Tonnes', NULL, 'Station offline'),

-- 2023
(1, 1, 2023, 3700.0, 'Hectares', 18870.0, 'Metric Tonnes', 620.0, 'Cold winter favorable'),
(2, 1, 2023, 3250.0, 'Hectares', 14300.0, 'Metric Tonnes', 710.0, 'Peak summer sowing'),
(3, 1, 2023, 1350.0, 'Hectares', 5805.0, 'Metric Tonnes', 600.0, 'Intercropped fields'),
(4, 1, 2023, 1680.0, 'Hectares', 3528.0, 'Metric Tonnes', 580.0, 'Controlled pest management'),
(5, 1, 2023, 1050.0, 'Hectares', 88200.0, 'Metric Tonnes', 640.0, 'Highest cane yield'),

(1, 2, 2023, 2450.0, 'Hectares', 8085.0, 'Metric Tonnes', 970.0, 'Nashik farm clusters'),
(2, 2, 2023, 4000.0, 'Hectares', 13600.0, 'Metric Tonnes', 1340.0, 'Heavy coastal monsoon'),
(3, 2, 2023, 2150.0, 'Hectares', 8170.0, 'Metric Tonnes', 960.0, 'Starch manufacturing sales'),
(4, 2, 2023, 3500.0, 'Hectares', 7700.0, 'Metric Tonnes', 990.0, 'Nagpur textile belt'),
(5, 2, 2023, 1800.0, 'Hectares', 162000.0, 'Metric Tonnes', 1230.0, 'Record crushing season'),

(1, 3, 2023, 1550.0, 'Hectares', 4805.0, 'Metric Tonnes', 830.0, 'Vijayapura black soil'),
(2, 3, 2023, 3100.0, 'Hectares', 11470.0, 'Metric Tonnes', 1310.0, 'Bhadra canal supply'),
(3, 3, 2023, 2400.0, 'Hectares', 9840.0, 'Metric Tonnes', 860.0, 'High productivity hybrid'),
(4, 3, 2023, 1850.0, 'Hectares', 4070.0, 'Metric Tonnes', 800.0, 'Gadag market'),
(5, 3, 2023, 1350.0, 'Hectares', 117450.0, 'Metric Tonnes', 1090.0, 'Belagavi sugar mills');
