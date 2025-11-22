export interface TourismRequest {
  query: string;
  place?: string | null;
}

export interface WeatherResponse {
  temperature: number;
  rain_probability: number;
  place_name: string;
}

export interface PlaceInfo {
  name: string;
  type: string;
  description?: string | null;
}

export interface TourismResponse {
  place_name: string | null;
  weather: WeatherResponse | null;
  places: PlaceInfo[] | null;
  message: string;
  error: string | null;
  success: boolean;
}

export interface QueryHistory {
  id: number;
  query: string;
  place_name: string | null;
  user_ip: string | null;
  has_weather: boolean;
  has_places: boolean;
  weather_temp: number | null;
  weather_rain_prob: number | null;
  places_count: number;
  error: string | null;
  success: boolean;
  created_at: string;
}

export interface QueryStats {
  total_queries: number;
  successful_queries: number;
  unique_places: number;
}

