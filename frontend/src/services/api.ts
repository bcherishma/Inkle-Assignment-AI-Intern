import axios from 'axios';
import type { TourismRequest, TourismResponse, QueryHistory, QueryStats } from '../types';

// Use environment variable or default to localhost for development
// In Docker, VITE_API_BASE_URL will be set to http://backend:8000
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 900000, //timeout for Render free tier (wake-up can take 30-60 seconds, giving extra buffer)
});

export const tourismAPI = {
  /**
   * Query tourism information
   */
  async query(request: TourismRequest): Promise<TourismResponse> {
    const response = await apiClient.post<TourismResponse>('/query', request);
    return response.data;
  },

  /**
   * Get query history
   */
  async getHistory(limit: number = 10, days?: number): Promise<QueryHistory[]> {
    const params: { limit: number; days?: number } = { limit };
    if (days) params.days = days;
    
    const response = await apiClient.get<{
      success: boolean;
      count: number;
      history: QueryHistory[];
    }>('/history', { params });
    return response.data.history;
  },

  /**
   * Get query statistics
   */
  async getStats(): Promise<QueryStats> {
    const response = await apiClient.get<{
      success: boolean;
      stats: QueryStats;
    }>('/history/stats');
    return response.data.stats;
  },

  /**
   * Get history for a specific place
   */
  async getPlaceHistory(placeName: string, limit: number = 5): Promise<QueryHistory[]> {
    const response = await apiClient.get<{
      success: boolean;
      place_name: string;
      count: number;
      history: QueryHistory[];
    }>(`/history/place/${encodeURIComponent(placeName)}`, {
      params: { limit },
    });
    return response.data.history;
  },

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

