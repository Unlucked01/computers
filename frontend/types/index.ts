// Базовые типы
export interface ComponentCategory {
  id: string;
  name: string;
  slug: string;
  description?: string;
  order_priority: number;
  icon?: string;
}

export interface ComponentStock {
  status: 'in_stock' | 'expected' | 'out_of_stock';
  quantity: number;
  expected_date?: string;
  updated_at: string;
}

export interface Component {
  id: string;
  name: string;
  brand: string;
  model: string;
  description?: string;
  image_url?: string;
  price: number;
  currency?: string;
  category: ComponentCategory;
  specifications: Record<string, any>;
  compatibility_data?: Record<string, any>;
  form_factor?: string;
  power_consumption?: number;
  created_at: string;
  updated_at?: string;
  is_active: boolean;
  stock?: ComponentStock;
}

export interface ConfigurationItem {
  id: string;
  component: Component;
  quantity: number;
  price_snapshot?: number;
  order_priority: number;
  notes?: string;
  added_at: string;
}

export interface Configuration {
  id: string;
  name: string;
  description?: string;
  total_price: number;
  currency: string;
  status: 'draft' | 'completed' | 'exported';
  compatibility_status: 'compatible' | 'incompatible' | 'warning' | 'unknown';
  compatibility_issues?: any[];
  availability_status: 'available' | 'partial' | 'unavailable' | 'unknown';
  expected_delivery_date?: string;
  created_at: string;
  updated_at?: string;
  public_uuid?: string;
  items: ConfigurationItem[];
}

export interface CompatibilityIssue {
  type: string;
  severity: 'error' | 'warning' | 'info';
  message: string;
  component_ids: string[];
  suggestions?: string[];
}

export interface CompatibilityCheck {
  is_compatible: boolean;
  status: 'compatible' | 'incompatible' | 'warning' | 'unknown';
  issues: CompatibilityIssue[];
  total_power_consumption?: number;
  recommended_psu_wattage?: number;
}

// Фильтры
export interface ComponentFilter {
  category_slug?: string;
  brand?: string[];
  price_min?: number;
  price_max?: number;
  only_in_stock?: boolean;
  form_factor?: string[];
  power_max?: number;
  search?: string;
  socket?: string[];
  memory_type?: string[];
  interface?: string[];
  page?: number;
  limit?: number;
}

export interface FilterOptions {
  brands: string[];
  form_factors: string[];
  sockets: string[];
  memory_types: string[];
  interfaces: string[];
  price_range: {
    min: number;
    max: number;
  };
}

// Состояние конфигуратора
export interface ConfiguratorState {
  selectedComponents: Record<string, Component>;
  currentConfiguration?: Configuration;
  isLoading: boolean;
  error?: string;
}

// API ответы
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
} 