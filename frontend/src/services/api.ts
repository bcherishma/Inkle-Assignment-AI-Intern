import axios from 'axios';
import type { TourismRequest, TourismResponse, QueryHistory, QueryStats } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
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

