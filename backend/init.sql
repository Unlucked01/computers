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
(gen_random_uuid(), 'Кулеры', 'cooler', 'Системы охлаждения процессора', 8, 'fan');

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
 null, 105, true);

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
 'ATX', 28, true);

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
 'DIMM', 12, true);

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
 'Triple-slot', 320, true);

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
 '3.5"', 10, true);

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
 'ATX', 0, true);

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