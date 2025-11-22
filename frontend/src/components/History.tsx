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
  }, []); // Empty deps - will reload when component remounts (via key prop)

  const loadHistory = async () => {
    try {
      const data = await tourismAPI.getHistory(10);
      setHistory(data);
    } catch (error: any) {
      // Silently fail for history - don't show error if backend is down
      console.error('Failed to load history:', error);
      setHistory([]); // Set empty array on error
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
      console.error('Failed to load stats:', error);
      // Don't set stats to null, just leave it as is
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
                  {new Date(item.created_at).toLocaleString('en-IN', {
                    timeZone: 'Asia/Kolkata',
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: true
                  })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

