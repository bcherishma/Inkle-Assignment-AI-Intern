import { useEffect, useState } from 'react';
import { tourismAPI } from '../services/api';
import type { QueryHistory, QueryStats } from '../types';

export default function History() {
  const [history, setHistory] = useState<QueryHistory[]>([]);
  const [stats, setStats] = useState<QueryStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
    loadStats();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await tourismAPI.getHistory(10);
      setHistory(data);
    } catch (error: any) {
      // Silently fail for history - don't show error if backend is down
      if (error.code !== 'ERR_NETWORK' && error.message !== 'Network Error') {
        console.error('Failed to load history:', error);
      }
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await tourismAPI.getStats();
      setStats(data);
    } catch (error: any) {
      // Silently fail for stats - don't show error if backend is down
      if (error.code !== 'ERR_NETWORK' && error.message !== 'Network Error') {
        console.error('Failed to load stats:', error);
      }
    }
  };

  if (loading) {
    return <div className="history loading">Loading history...</div>;
  }

  return (
    <div className="history">
      {stats && (
        <div className="stats-section">
          <h3>📊 Statistics</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-value">{stats.total_queries}</span>
              <span className="stat-label">Total Queries</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{stats.successful_queries}</span>
              <span className="stat-label">Successful</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{stats.unique_places}</span>
              <span className="stat-label">Unique Places</span>
            </div>
          </div>
        </div>
      )}

      <div className="history-section">
        <h3>📜 Recent Queries</h3>
        {history.length === 0 ? (
          <p>No query history yet.</p>
        ) : (
          <div className="history-list">
            {history.map((item) => (
              <div key={item.id} className="history-item">
                <div className="history-header">
                  <span className="history-query">{item.query}</span>
                  <span className={`history-status ${item.success ? 'success' : 'error'}`}>
                    {item.success ? '✓' : '✗'}
                  </span>
                </div>
                {item.place_name && (
                  <div className="history-details">
                    <span className="history-place">📍 {item.place_name}</span>
                    {item.has_weather && (
                      <span className="history-badge">🌤️ Weather</span>
                    )}
                    {item.has_places && (
                      <span className="history-badge">📍 {item.places_count} Places</span>
                    )}
                  </div>
                )}
                <div className="history-time">
                  {new Date(item.created_at).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

