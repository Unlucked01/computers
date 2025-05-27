-- Заполнение базы данных начальными данными для конфигуратора ПК
-- Таблицы должны быть созданы через Alembic миграции перед выполнением этого скрипта

-- Вставка категорий компонентов
INSERT INTO component_categories (id, name, slug, description, order_priority, icon) VALUES
(gen_random_uuid(), 'Процессоры', 'cpu', 'Центральные процессоры Intel и AMD', 1, 'cpu'),
(gen_random_uuid(), 'Материнские платы', 'motherboard', 'Материнские платы различных форм-факторов', 2, 'motherboard'),
(gen_random_uuid(), 'Оперативная память', 'ram', 'Модули оперативной памяти DDR4/DDR5', 3, 'memory'),
(gen_random_uuid(), 'Видеокарты', 'gpu', 'Дискретные видеокарты для игр и работы', 4, 'gpu'),
(gen_random_uuid(), 'Накопители', 'storage', 'SSD и HDD накопители', 5, 'storage'),
(gen_random_uuid(), 'Блоки питания', 'psu', 'Блоки питания различной мощности', 6, 'power'),
(gen_random_uuid(), 'Корпуса', 'case', 'Корпуса для сборки ПК', 7, 'case'),
(gen_random_uuid(), 'Кулеры', 'cooler', 'Системы охлаждения процессора', 8, 'fan'),
(gen_random_uuid(), 'Аксессуары', 'accessories', 'Мыши, клавиатуры, мониторы и другие аксессуары', 9, 'accessories');

-- Вставка процессоров
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'Intel Core i5-13600K', 'Intel', 'Core i5-13600K', 'Процессор Intel 13-го поколения', 25990, 
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "LGA1700", "cores": 14, "threads": 20, "base_freq": 3.5, "boost_freq": 5.1, "architecture": "Raptor Lake"}',
 null, 125, true),
 
(gen_random_uuid(), 'AMD Ryzen 5 7600X', 'AMD', 'Ryzen 5 7600X', 'Процессор AMD серии 7000', 23990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "AM5", "cores": 6, "threads": 12, "base_freq": 4.7, "boost_freq": 5.3, "architecture": "Zen 4"}',
 null, 105, true),

(gen_random_uuid(), 'Intel Core i7-13700K', 'Intel', 'Core i7-13700K', 'Высокопроизводительный процессор Intel', 35990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "LGA1700", "cores": 16, "threads": 24, "base_freq": 3.4, "boost_freq": 5.4, "architecture": "Raptor Lake"}',
 null, 125, true),

(gen_random_uuid(), 'AMD Ryzen 7 7700X', 'AMD', 'Ryzen 7 7700X', 'Процессор AMD для игр и контента', 31990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "AM5", "cores": 8, "threads": 16, "base_freq": 4.5, "boost_freq": 5.4, "architecture": "Zen 4"}',
 null, 105, true),

(gen_random_uuid(), 'Intel Core i9-13900K', 'Intel', 'Core i9-13900K', 'Топовый процессор Intel для энтузиастов', 49990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "LGA1700", "cores": 24, "threads": 32, "base_freq": 3.0, "boost_freq": 5.8, "architecture": "Raptor Lake"}',
 null, 125, true),

(gen_random_uuid(), 'AMD Ryzen 9 7900X', 'AMD', 'Ryzen 9 7900X', 'Мощный процессор AMD для профессионалов', 42990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "AM5", "cores": 12, "threads": 24, "base_freq": 4.7, "boost_freq": 5.6, "architecture": "Zen 4"}',
 null, 170, true),

(gen_random_uuid(), 'Intel Core i5-12600K', 'Intel', 'Core i5-12600K', 'Процессор Intel 12-го поколения', 21990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "LGA1700", "cores": 10, "threads": 16, "base_freq": 3.7, "boost_freq": 4.9, "architecture": "Alder Lake"}',
 null, 125, true),

(gen_random_uuid(), 'AMD Ryzen 5 5600X', 'AMD', 'Ryzen 5 5600X', 'Популярный процессор AMD предыдущего поколения', 18990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "AM4", "cores": 6, "threads": 12, "base_freq": 3.7, "boost_freq": 4.6, "architecture": "Zen 3"}',
 null, 65, true),

(gen_random_uuid(), 'Intel Core i3-13100F', 'Intel', 'Core i3-13100F', 'Бюджетный процессор Intel без встроенной графики', 12990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "LGA1700", "cores": 4, "threads": 8, "base_freq": 3.4, "boost_freq": 4.5, "architecture": "Raptor Lake"}',
 null, 58, true),

(gen_random_uuid(), 'AMD Ryzen 9 7950X', 'AMD', 'Ryzen 9 7950X', 'Флагманский процессор AMD', 59990,
 (SELECT id FROM component_categories WHERE slug = 'cpu'),
 '{"socket": "AM5", "cores": 16, "threads": 32, "base_freq": 4.5, "boost_freq": 5.7, "architecture": "Zen 4"}',
 null, 170, true);

-- Вставка материнских плат
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'ASUS PRIME Z790-P', 'ASUS', 'PRIME Z790-P', 'Материнская плата для Intel LGA1700', 15990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "LGA1700", "chipset": "Z790", "memory_type": ["DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 25, true),

(gen_random_uuid(), 'MSI MAG B650 TOMAHAWK', 'MSI', 'MAG B650 TOMAHAWK', 'Материнская плата для AMD AM5', 17990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "AM5", "chipset": "B650", "memory_type": ["DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 30, true),

(gen_random_uuid(), 'GIGABYTE Z790 AORUS ELITE', 'GIGABYTE', 'Z790 AORUS ELITE', 'Игровая материнская плата Intel', 18990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "LGA1700", "chipset": "Z790", "memory_type": ["DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 28, true),

(gen_random_uuid(), 'ASUS ROG STRIX X670E-E', 'ASUS', 'ROG STRIX X670E-E', 'Премиальная материнская плата AMD', 34990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "AM5", "chipset": "X670E", "memory_type": ["DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 35, true),

(gen_random_uuid(), 'MSI PRO B760M-A', 'MSI', 'PRO B760M-A', 'Компактная материнская плата Intel', 8990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "LGA1700", "chipset": "B760", "memory_type": ["DDR4", "DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["mATX"]}',
 'mATX', 20, true),

(gen_random_uuid(), 'GIGABYTE B550 AORUS ELITE', 'GIGABYTE', 'B550 AORUS ELITE', 'Материнская плата для AMD AM4', 12990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "AM4", "chipset": "B550", "memory_type": ["DDR4"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 25, true),

(gen_random_uuid(), 'ASUS TUF GAMING Z790-PLUS', 'ASUS', 'TUF GAMING Z790-PLUS', 'Надежная игровая материнская плата', 21990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "LGA1700", "chipset": "Z790", "memory_type": ["DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 30, true),

(gen_random_uuid(), 'MSI MPG X670E CARBON WIFI', 'MSI', 'MPG X670E CARBON WIFI', 'Высокопроизводительная плата AMD с Wi-Fi', 28990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "AM5", "chipset": "X670E", "memory_type": ["DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 32, true),

(gen_random_uuid(), 'ASUS PRIME B550M-A', 'ASUS', 'PRIME B550M-A', 'Бюджетная материнская плата AMD', 7990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "AM4", "chipset": "B550", "memory_type": ["DDR4"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["mATX"]}',
 'mATX', 18, true),

(gen_random_uuid(), 'GIGABYTE Z790 AORUS MASTER', 'GIGABYTE', 'Z790 AORUS MASTER', 'Флагманская материнская плата Intel', 42990,
 (SELECT id FROM component_categories WHERE slug = 'motherboard'),
 '{"socket": "LGA1700", "chipset": "Z790", "memory_type": ["DDR5"], "memory_slots": 4, "max_memory_gb": 128, "supported_form_factors": ["ATX"]}',
 'ATX', 40, true);

-- Вставка оперативной памяти
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'Corsair Vengeance LPX 16GB', 'Corsair', 'CMK16GX5M2B5600C36', 'DDR5-5600 16GB (2x8GB)', 8990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR5", "capacity_gb": 16, "frequency": 5600, "modules": 2, "cas_latency": 36}',
 'DIMM', 15, true),

(gen_random_uuid(), 'G.SKILL Trident Z5 32GB', 'G.SKILL', 'F5-6000J3636F16GX2-TZ5K', 'DDR5-6000 32GB (2x16GB)', 16990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR5", "capacity_gb": 32, "frequency": 6000, "modules": 2, "cas_latency": 36}',
 'DIMM', 20, true),

(gen_random_uuid(), 'Kingston FURY Beast 16GB', 'Kingston', 'KF556C40BBK2-16', 'DDR5-5600 16GB (2x8GB)', 7990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR5", "capacity_gb": 16, "frequency": 5600, "modules": 2, "cas_latency": 40}',
 'DIMM', 12, true),

(gen_random_uuid(), 'Corsair Vengeance LPX 32GB DDR4', 'Corsair', 'CMK32GX4M2E3200C16', 'DDR4-3200 32GB (2x16GB)', 11990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR4", "capacity_gb": 32, "frequency": 3200, "modules": 2, "cas_latency": 16}',
 'DIMM', 10, true),

(gen_random_uuid(), 'G.SKILL Ripjaws V 16GB DDR4', 'G.SKILL', 'F4-3600C16D-16GVKC', 'DDR4-3600 16GB (2x8GB)', 5990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR4", "capacity_gb": 16, "frequency": 3600, "modules": 2, "cas_latency": 16}',
 'DIMM', 8, true),

(gen_random_uuid(), 'Kingston FURY Beast 64GB DDR5', 'Kingston', 'KF560C40BBK4-64', 'DDR5-6000 64GB (4x16GB)', 32990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR5", "capacity_gb": 64, "frequency": 6000, "modules": 4, "cas_latency": 40}',
 'DIMM', 35, true),

(gen_random_uuid(), 'Corsair Dominator Platinum RGB 32GB', 'Corsair', 'CMT32GX5M2B5600C36', 'DDR5-5600 32GB (2x16GB) с RGB', 21990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR5", "capacity_gb": 32, "frequency": 5600, "modules": 2, "cas_latency": 36, "rgb": true}',
 'DIMM', 18, true),

(gen_random_uuid(), 'HyperX Predator 16GB DDR4', 'HyperX', 'HX436C17PB3K2/16', 'DDR4-3600 16GB (2x8GB)', 6990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR4", "capacity_gb": 16, "frequency": 3600, "modules": 2, "cas_latency": 17}',
 'DIMM', 9, true),

(gen_random_uuid(), 'G.SKILL Trident Z Neo 32GB DDR4', 'G.SKILL', 'F4-3600C16D-32GTZNC', 'DDR4-3600 32GB (2x16GB) для AMD', 13990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR4", "capacity_gb": 32, "frequency": 3600, "modules": 2, "cas_latency": 16, "optimized_for": "AMD"}',
 'DIMM', 12, true),

(gen_random_uuid(), 'Crucial Ballistix 8GB DDR4', 'Crucial', 'BL8G32C16U4B', 'DDR4-3200 8GB (1x8GB)', 2990,
 (SELECT id FROM component_categories WHERE slug = 'ram'),
 '{"memory_type": "DDR4", "capacity_gb": 8, "frequency": 3200, "modules": 1, "cas_latency": 16}',
 'DIMM', 5, true);

-- Вставка видеокарт
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'NVIDIA GeForce RTX 4070', 'NVIDIA', 'RTX 4070', 'Видеокарта для 1440p игр', 54990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 12, "memory_type": "GDDR6X", "interface": "PCIe 4.0", "display_ports": 3, "hdmi_ports": 1}',
 'Dual-slot', 200, true),

(gen_random_uuid(), 'AMD Radeon RX 7700 XT', 'AMD', 'RX 7700 XT', 'Высокопроизводительная видеокарта AMD', 49990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 12, "memory_type": "GDDR6", "interface": "PCIe 4.0", "display_ports": 4, "hdmi_ports": 1}',
 'Dual-slot', 245, true),

(gen_random_uuid(), 'NVIDIA GeForce RTX 4080', 'NVIDIA', 'RTX 4080', 'Топовая видеокарта для 4K', 89990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 16, "memory_type": "GDDR6X", "interface": "PCIe 4.0", "display_ports": 3, "hdmi_ports": 1}',
 'Triple-slot', 320, true),

(gen_random_uuid(), 'NVIDIA GeForce RTX 4090', 'NVIDIA', 'RTX 4090', 'Флагманская видеокарта NVIDIA', 149990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 24, "memory_type": "GDDR6X", "interface": "PCIe 4.0", "display_ports": 3, "hdmi_ports": 1}',
 'Triple-slot', 450, true),

(gen_random_uuid(), 'AMD Radeon RX 7800 XT', 'AMD', 'RX 7800 XT', 'Мощная видеокарта AMD для 1440p/4K', 59990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 16, "memory_type": "GDDR6", "interface": "PCIe 4.0", "display_ports": 4, "hdmi_ports": 1}',
 'Dual-slot', 263, true),

(gen_random_uuid(), 'NVIDIA GeForce RTX 4060', 'NVIDIA', 'RTX 4060', 'Видеокарта среднего класса для 1080p/1440p', 34990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 8, "memory_type": "GDDR6", "interface": "PCIe 4.0", "display_ports": 3, "hdmi_ports": 1}',
 'Dual-slot', 115, true),

(gen_random_uuid(), 'AMD Radeon RX 6700 XT', 'AMD', 'RX 6700 XT', 'Видеокарта предыдущего поколения AMD', 39990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 12, "memory_type": "GDDR6", "interface": "PCIe 4.0", "display_ports": 3, "hdmi_ports": 1}',
 'Dual-slot', 230, true),

(gen_random_uuid(), 'NVIDIA GeForce RTX 4070 Ti', 'NVIDIA', 'RTX 4070 Ti', 'Улучшенная версия RTX 4070', 69990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 12, "memory_type": "GDDR6X", "interface": "PCIe 4.0", "display_ports": 3, "hdmi_ports": 1}',
 'Dual-slot', 285, true),

(gen_random_uuid(), 'AMD Radeon RX 7900 XTX', 'AMD', 'RX 7900 XTX', 'Топовая видеокарта AMD', 99990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 24, "memory_type": "GDDR6", "interface": "PCIe 4.0", "display_ports": 4, "hdmi_ports": 1}',
 'Triple-slot', 355, true),

(gen_random_uuid(), 'NVIDIA GeForce RTX 4060 Ti', 'NVIDIA', 'RTX 4060 Ti', 'Улучшенная версия RTX 4060', 44990,
 (SELECT id FROM component_categories WHERE slug = 'gpu'),
 '{"memory_gb": 16, "memory_type": "GDDR6", "interface": "PCIe 4.0", "display_ports": 3, "hdmi_ports": 1}',
 'Dual-slot', 165, true);

-- Вставка накопителей
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'Samsung 980 PRO 1TB', 'Samsung', '980 PRO', 'NVMe SSD PCIe 4.0', 9990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 1000, "interface": "NVMe PCIe 4.0", "form_factor": "M.2 2280", "read_speed": 7000, "write_speed": 5000}',
 'M.2', 7, true),

(gen_random_uuid(), 'WD Black SN850X 2TB', 'Western Digital', 'WD Black SN850X', 'Игровой NVMe SSD', 17990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 2000, "interface": "NVMe PCIe 4.0", "form_factor": "M.2 2280", "read_speed": 7300, "write_speed": 6600}',
 'M.2', 8, true),

(gen_random_uuid(), 'Seagate Barracuda 2TB', 'Seagate', 'ST2000DM008', 'Жесткий диск для хранения данных', 5990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 2000, "interface": "SATA III", "form_factor": "3.5", "rpm": 7200, "cache_mb": 256}',
 '3.5"', 10, true),

(gen_random_uuid(), 'Samsung 980 PRO 2TB', 'Samsung', '980 PRO 2TB', 'Высокоскоростной NVMe SSD 2TB', 19990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 2000, "interface": "NVMe PCIe 4.0", "form_factor": "M.2 2280", "read_speed": 7000, "write_speed": 6900}',
 'M.2', 8, true),

(gen_random_uuid(), 'Crucial MX4 1TB', 'Crucial', 'CT1000MX4SSD1', 'SATA SSD для апгрейда', 7990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 1000, "interface": "SATA III", "form_factor": "2.5", "read_speed": 560, "write_speed": 510}',
 '2.5"', 5, true),

(gen_random_uuid(), 'WD Blue 4TB', 'Western Digital', 'WD40EZAZ', 'Надежный HDD для хранения', 8990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 4000, "interface": "SATA III", "form_factor": "3.5", "rpm": 5400, "cache_mb": 256}',
 '3.5"', 8, true),

(gen_random_uuid(), 'Kingston NV2 500GB', 'Kingston', 'SNV2S/500G', 'Бюджетный NVMe SSD', 3990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 500, "interface": "NVMe PCIe 4.0", "form_factor": "M.2 2280", "read_speed": 3500, "write_speed": 2100}',
 'M.2', 5, true),

(gen_random_uuid(), 'Seagate IronWolf 8TB', 'Seagate', 'ST8000VN004', 'NAS HDD для серверов', 24990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 8000, "interface": "SATA III", "form_factor": "3.5", "rpm": 7200, "cache_mb": 256, "nas_optimized": true}',
 '3.5"', 12, true),

(gen_random_uuid(), 'Samsung 970 EVO Plus 1TB', 'Samsung', '970 EVO Plus', 'Популярный NVMe SSD', 8990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 1000, "interface": "NVMe PCIe 3.0", "form_factor": "M.2 2280", "read_speed": 3500, "write_speed": 3300}',
 'M.2', 6, true),

(gen_random_uuid(), 'WD Black 1TB', 'Western Digital', 'WD1003FZEX', 'Высокопроизводительный HDD', 6990,
 (SELECT id FROM component_categories WHERE slug = 'storage'),
 '{"capacity_gb": 1000, "interface": "SATA III", "form_factor": "3.5", "rpm": 7200, "cache_mb": 64}',
 '3.5"', 9, true);

-- Вставка блоков питания
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'Corsair RM750x', 'Corsair', 'CP-9020199-EU', 'Модульный блок питания 750W 80+ Gold', 11990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 750, "efficiency": "80+ Gold", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 2, "8pin_pcie": 4}}',
 'ATX', 0, true),

(gen_random_uuid(), 'be quiet! Straight Power 11 650W', 'be quiet!', 'BN282', 'Тихий блок питания 650W 80+ Gold', 9990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 650, "efficiency": "80+ Gold", "modular": false, "connectors": {"24pin": 1, "8pin_cpu": 1, "8pin_pcie": 2}}',
 'ATX', 0, true),

(gen_random_uuid(), 'Seasonic Focus GX-850', 'Seasonic', 'SSR-850FX', 'Полумодульный БП 850W 80+ Gold', 13990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 850, "efficiency": "80+ Gold", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 2, "8pin_pcie": 4}}',
 'ATX', 0, true),

(gen_random_uuid(), 'Corsair HX1000i', 'Corsair', 'CP-9020074-EU', 'Премиальный модульный БП 1000W 80+ Platinum', 19990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 1000, "efficiency": "80+ Platinum", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 2, "8pin_pcie": 6}, "digital_monitoring": true}',
 'ATX', 0, true),

(gen_random_uuid(), 'EVGA SuperNOVA 550 G5', 'EVGA', '220-G5-0550-X1', 'Компактный БП 550W 80+ Gold', 7990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 550, "efficiency": "80+ Gold", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 1, "8pin_pcie": 2}}',
 'ATX', 0, true),

(gen_random_uuid(), 'be quiet! Dark Power Pro 12 1200W', 'be quiet!', 'BN312', 'Высокомощный БП 1200W 80+ Titanium', 24990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 1200, "efficiency": "80+ Titanium", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 2, "8pin_pcie": 8}}',
 'ATX', 0, true),

(gen_random_uuid(), 'Thermaltake Toughpower GF1 750W', 'Thermaltake', 'PS-TPD-0750FNFAGU-1', 'Игровой БП 750W 80+ Gold', 8990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 750, "efficiency": "80+ Gold", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 2, "8pin_pcie": 4}, "rgb": true}',
 'ATX', 0, true),

(gen_random_uuid(), 'Seasonic Prime TX-1000', 'Seasonic', 'SSR-1000TR', 'Топовый БП 1000W 80+ Titanium', 22990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 1000, "efficiency": "80+ Titanium", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 2, "8pin_pcie": 6}}',
 'ATX', 0, true),

(gen_random_uuid(), 'Cooler Master MWE Gold 650W', 'Cooler Master', 'MPY-6501-ACAAG-US', 'Бюджетный БП 650W 80+ Gold', 6990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 650, "efficiency": "80+ Gold", "modular": false, "connectors": {"24pin": 1, "8pin_cpu": 1, "8pin_pcie": 2}}',
 'ATX', 0, true),

(gen_random_uuid(), 'FSP Hydro G Pro 850W', 'FSP', 'HG2-850', 'Надежный БП 850W 80+ Gold', 10990,
 (SELECT id FROM component_categories WHERE slug = 'psu'),
 '{"wattage": 850, "efficiency": "80+ Gold", "modular": true, "connectors": {"24pin": 1, "8pin_cpu": 2, "8pin_pcie": 4}}',
 'ATX', 0, true);

-- Вставка корпусов
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'Fractal Design Define 7', 'Fractal Design', 'Define 7', 'Тихий корпус ATX', 12990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["ATX", "mATX", "Mini-ITX"], "max_gpu_length": 440, "drive_bays_35": 6, "drive_bays_25": 4, "fans_included": 2}',
 'ATX', 0, true),

(gen_random_uuid(), 'NZXT H7 Flow', 'NZXT', 'H7 Flow', 'Игровой корпус с RGB подсветкой', 15990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["ATX", "mATX", "Mini-ITX"], "max_gpu_length": 381, "drive_bays_35": 2, "drive_bays_25": 4, "fans_included": 3}',
 'ATX', 0, true),

(gen_random_uuid(), 'Lian Li PC-O11 Dynamic', 'Lian Li', 'PC-O11D', 'Корпус для водяного охлаждения', 13990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["ATX", "mATX", "Mini-ITX"], "max_gpu_length": 420, "drive_bays_35": 2, "drive_bays_25": 6, "fans_included": 0}',
 'ATX', 0, true),

(gen_random_uuid(), 'Corsair 4000D Airflow', 'Corsair', '4000D Airflow', 'Корпус с отличной вентиляцией', 9990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["ATX", "mATX", "Mini-ITX"], "max_gpu_length": 360, "drive_bays_35": 2, "drive_bays_25": 2, "fans_included": 2}',
 'ATX', 0, true),

(gen_random_uuid(), 'be quiet! Pure Base 500DX', 'be quiet!', 'Pure Base 500DX', 'Тихий корпус среднего класса', 8990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["ATX", "mATX", "Mini-ITX"], "max_gpu_length": 369, "drive_bays_35": 2, "drive_bays_25": 3, "fans_included": 3}',
 'ATX', 0, true),

(gen_random_uuid(), 'Cooler Master MasterBox Q300L', 'Cooler Master', 'Q300L', 'Компактный mATX корпус', 4990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["mATX", "Mini-ITX"], "max_gpu_length": 360, "drive_bays_35": 1, "drive_bays_25": 2, "fans_included": 1}',
 'mATX', 0, true),

(gen_random_uuid(), 'Phanteks Eclipse P400A', 'Phanteks', 'P400A', 'Стильный корпус с RGB', 7990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["ATX", "mATX", "Mini-ITX"], "max_gpu_length": 420, "drive_bays_35": 2, "drive_bays_25": 3, "fans_included": 2, "rgb": true}',
 'ATX', 0, true),

(gen_random_uuid(), 'Thermaltake Core P3', 'Thermaltake', 'Core P3', 'Открытый корпус для моддинга', 11990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["ATX", "mATX", "Mini-ITX"], "max_gpu_length": 500, "drive_bays_35": 2, "drive_bays_25": 2, "fans_included": 0, "open_frame": true}',
 'ATX', 0, true),

(gen_random_uuid(), 'Fractal Design Node 202', 'Fractal Design', 'Node 202', 'Компактный HTPC корпус', 8990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["Mini-ITX"], "max_gpu_length": 310, "drive_bays_35": 0, "drive_bays_25": 2, "fans_included": 1, "htpc": true}',
 'Mini-ITX', 0, true),

(gen_random_uuid(), 'Lian Li O11D Mini', 'Lian Li', 'O11D Mini', 'Компактная версия популярного корпуса', 10990,
 (SELECT id FROM component_categories WHERE slug = 'case'),
 '{"supported_form_factors": ["mATX", "Mini-ITX"], "max_gpu_length": 280, "drive_bays_35": 0, "drive_bays_25": 4, "fans_included": 0}',
 'mATX', 0, true);

-- Создание записей о наличии компонентов для первых 15 компонентов
INSERT INTO component_stock (id, component_id, status, quantity, updated_at) 
SELECT gen_random_uuid(), c.id, 'in_stock', 50, NOW() 
FROM components c 
LIMIT 15;

-- Создание записей о наличии компонентов для остальных компонентов (ожидается поставка)
INSERT INTO component_stock (id, component_id, status, quantity, expected_date, updated_at)
SELECT gen_random_uuid(), c.id, 'expected', 0, NOW() + INTERVAL '7 days', NOW() 
FROM components c 
WHERE c.id NOT IN (
    SELECT cs.component_id FROM component_stock cs
);

-- Добавление записей о наличии для аксессуаров
INSERT INTO component_stock (id, component_id, status, quantity, updated_at) 
SELECT gen_random_uuid(), c.id, 'in_stock', 25, NOW() 
FROM components c 
WHERE c.category_id = (SELECT id FROM component_categories WHERE slug = 'accessories')
AND c.id NOT IN (SELECT cs.component_id FROM component_stock cs);

-- Добавление записей о наличии для кулеров
INSERT INTO component_stock (id, component_id, status, quantity, updated_at) 
SELECT gen_random_uuid(), c.id, 'in_stock', 30, NOW() 
FROM components c 
WHERE c.category_id = (SELECT id FROM component_categories WHERE slug = 'cooler')
AND c.id NOT IN (SELECT cs.component_id FROM component_stock cs);

-- Вставка аксессуаров
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
-- Мыши
(gen_random_uuid(), 'Logitech G Pro X Superlight', 'Logitech', 'G Pro X Superlight', 'Беспроводная игровая мышь для киберспорта', 12990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "mouse", "connection": "wireless", "dpi": 25600, "buttons": 5, "weight_g": 63, "battery_hours": 70}',
 null, 0, true),

(gen_random_uuid(), 'Razer DeathAdder V3', 'Razer', 'DeathAdder V3', 'Эргономичная игровая мышь', 7990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "mouse", "connection": "wired", "dpi": 30000, "buttons": 8, "weight_g": 59, "cable_length_m": 1.8}',
 null, 0, true),

(gen_random_uuid(), 'SteelSeries Rival 650', 'SteelSeries', 'Rival 650', 'Игровая мышь с настраиваемым весом', 8990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "mouse", "connection": "wired", "dpi": 12000, "buttons": 7, "weight_g": 121, "customizable_weight": true}',
 null, 0, true),

-- Клавиатуры
(gen_random_uuid(), 'Corsair K95 RGB Platinum XT', 'Corsair', 'K95 RGB Platinum XT', 'Механическая игровая клавиатура', 18990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "keyboard", "connection": "wired", "switches": "Cherry MX Speed", "backlight": "RGB", "layout": "full-size", "macro_keys": 6}',
 null, 0, true),

(gen_random_uuid(), 'Keychron K8', 'Keychron', 'K8', 'Беспроводная механическая клавиатура', 9990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "keyboard", "connection": "wireless", "switches": "Gateron Red", "backlight": "RGB", "layout": "tenkeyless", "battery_hours": 240}',
 null, 0, true),

(gen_random_uuid(), 'HyperX Alloy FPS Pro', 'HyperX', 'Alloy FPS Pro', 'Компактная механическая клавиатура', 6990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "keyboard", "connection": "wired", "switches": "Cherry MX Red", "backlight": "red", "layout": "tenkeyless", "detachable_cable": true}',
 null, 0, true),

-- Мониторы
(gen_random_uuid(), 'ASUS ROG Swift PG279QM', 'ASUS', 'PG279QM', 'Игровой монитор 27" 1440p 240Hz', 54990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "monitor", "size_inch": 27, "resolution": "2560x1440", "refresh_rate": 240, "panel_type": "IPS", "response_time_ms": 1, "gsync": true}',
 null, 45, true),

(gen_random_uuid(), 'LG 27GP850-B', 'LG', '27GP850-B', 'Игровой монитор 27" 1440p 165Hz', 32990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "monitor", "size_inch": 27, "resolution": "2560x1440", "refresh_rate": 165, "panel_type": "Nano IPS", "response_time_ms": 1, "gsync_compatible": true}',
 null, 40, true),

(gen_random_uuid(), 'Samsung Odyssey G7 32"', 'Samsung', 'LC32G75TQSIXCI', 'Изогнутый игровой монитор 32" 1440p 240Hz', 49990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "monitor", "size_inch": 32, "resolution": "2560x1440", "refresh_rate": 240, "panel_type": "VA", "response_time_ms": 1, "curvature": "1000R", "hdr": true}',
 null, 50, true),

-- Наушники
(gen_random_uuid(), 'SteelSeries Arctis 7P', 'SteelSeries', 'Arctis 7P', 'Беспроводная игровая гарнитура', 14990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "headset", "connection": "wireless", "frequency_response": "20-20000", "impedance": 32, "battery_hours": 24, "microphone": "retractable"}',
 null, 0, true),

(gen_random_uuid(), 'HyperX Cloud II', 'HyperX', 'Cloud II', 'Проводная игровая гарнитура', 7990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "headset", "connection": "wired", "frequency_response": "15-25000", "impedance": 60, "drivers_mm": 53, "microphone": "detachable", "surround": "7.1"}',
 null, 0, true),

(gen_random_uuid(), 'Audio-Technica ATH-M50x', 'Audio-Technica', 'ATH-M50x', 'Профессиональные студийные наушники', 12990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "headphones", "connection": "wired", "frequency_response": "15-28000", "impedance": 38, "drivers_mm": 45, "foldable": true, "detachable_cable": true}',
 null, 0, true),

-- Веб-камеры
(gen_random_uuid(), 'Logitech C920 HD Pro', 'Logitech', 'C920', 'Веб-камера Full HD для стриминга', 5990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "webcam", "resolution": "1920x1080", "fps": 30, "autofocus": true, "microphone": "stereo", "connection": "USB-A"}',
 null, 0, true),

(gen_random_uuid(), 'Razer Kiyo', 'Razer', 'Kiyo', 'Веб-камера со встроенной подсветкой', 8990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "webcam", "resolution": "1920x1080", "fps": 30, "ring_light": true, "microphone": "built-in", "connection": "USB-A"}',
 null, 0, true),

-- Коврики для мыши
(gen_random_uuid(), 'SteelSeries QcK Heavy', 'SteelSeries', 'QcK Heavy', 'Игровой коврик для мыши', 2990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "mousepad", "size": "450x400x6", "material": "cloth", "base": "rubber", "stitched_edges": true}',
 null, 0, true),

(gen_random_uuid(), 'Corsair MM300 Extended', 'Corsair', 'MM300', 'Расширенный игровой коврик', 3990,
 (SELECT id FROM component_categories WHERE slug = 'accessories'),
 '{"type": "mousepad", "size": "930x300x3", "material": "cloth", "base": "rubber", "anti_fray": true, "extended": true}',
 null, 0, true);

-- Вставка систем охлаждения (кулеров)
INSERT INTO components (id, name, brand, model, description, price, category_id, specifications, form_factor, power_consumption, is_active) VALUES
(gen_random_uuid(), 'Noctua NH-D15', 'Noctua', 'NH-D15', 'Топовый воздушный кулер для процессора', 8990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "air", "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "height_mm": 165, "fans": 2, "tdp_rating": 220}',
 'Tower', 4, true),

(gen_random_uuid(), 'Corsair H100i RGB Platinum', 'Corsair', 'H100i RGB Platinum', 'Жидкостное охлаждение 240мм с RGB', 12990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "aio", "radiator_size": 240, "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "fans": 2, "rgb": true, "pump_speed": 2400}',
 'AIO', 15, true),

(gen_random_uuid(), 'be quiet! Dark Rock Pro 4', 'be quiet!', 'Dark Rock Pro 4', 'Тихий высокопроизводительный кулер', 7990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "air", "socket_support": ["LGA1700", "LGA1200", "AM4"], "height_mm": 163, "fans": 2, "tdp_rating": 250, "noise_level": 24.3}',
 'Tower', 3, true),

(gen_random_uuid(), 'Arctic Liquid Freezer II 280', 'Arctic', 'Liquid Freezer II 280', 'Эффективное жидкостное охлаждение 280мм', 9990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "aio", "radiator_size": 280, "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "fans": 2, "pump_speed": 2000}',
 'AIO', 12, true),

(gen_random_uuid(), 'Cooler Master Hyper 212 Black Edition', 'Cooler Master', 'Hyper 212 Black Edition', 'Популярный бюджетный кулер', 2990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "air", "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "height_mm": 158, "fans": 1, "tdp_rating": 150}',
 'Tower', 2, true),

(gen_random_uuid(), 'NZXT Kraken X63', 'NZXT', 'Kraken X63', 'Премиальное жидкостное охлаждение 280мм', 16990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "aio", "radiator_size": 280, "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "fans": 2, "rgb": true, "lcd_display": false, "pump_speed": 2800}',
 'AIO', 18, true),

(gen_random_uuid(), 'Scythe Fuma 2', 'Scythe', 'Fuma 2', 'Компактный двухбашенный кулер', 5990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "air", "socket_support": ["LGA1700", "LGA1200", "AM4"], "height_mm": 154, "fans": 2, "tdp_rating": 200}',
 'Tower', 3, true),

(gen_random_uuid(), 'Corsair H150i Elite Capellix', 'Corsair', 'H150i Elite Capellix', 'Топовое жидкостное охлаждение 360мм', 19990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "aio", "radiator_size": 360, "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "fans": 3, "rgb": true, "pump_speed": 2400}',
 'AIO', 20, true),

(gen_random_uuid(), 'Deepcool AK620', 'Deepcool', 'AK620', 'Мощный воздушный кулер с двумя башнями', 4990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "air", "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "height_mm": 160, "fans": 2, "tdp_rating": 220}',
 'Tower', 4, true),

(gen_random_uuid(), 'Thermaltake Floe DX RGB 240', 'Thermaltake', 'Floe DX RGB 240', 'Жидкостное охлаждение с RGB подсветкой', 8990,
 (SELECT id FROM component_categories WHERE slug = 'cooler'),
 '{"type": "aio", "radiator_size": 240, "socket_support": ["LGA1700", "LGA1200", "AM4", "AM5"], "fans": 2, "rgb": true, "pump_speed": 3200}',
 'AIO', 14, true); 