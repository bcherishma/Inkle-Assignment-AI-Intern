import { useState } from 'react';
import QueryForm from './components/QueryForm';
import Results from './components/Results';
import History from './components/History';
import { tourismAPI } from './services/api';
import type { TourismRequest, TourismResponse } from './types';
import './App.css';

function App() {
  const [response, setResponse] = useState<TourismResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (request: TourismRequest) => {
    setIsLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await tourismAPI.query(request);
      setResponse(result);
    } catch (err: any) {
      // Better error handling for network errors
      let errorMessage = 'Failed to process query';
      if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
        errorMessage = 'Cannot connect to backend. Make sure the backend server is running on http://localhost:8000';
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
      setResponse({
        place_name: null,
        weather: null,
        places: null,
        message: errorMessage,
        error: 'API_ERROR',
        success: false,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Tourism AI Multi-Agent System</h1>
        <p>Get weather and tourist attraction information for any place</p>
      </header>

      <main className="app-main">
        <div className="main-content">
          <section className="query-section">
            <QueryForm onSubmit={handleSubmit} isLoading={isLoading} />
            <Results response={response} isLoading={isLoading} />
            {error && !response && (
              <div className="error-message">
                <p>Error: {error}</p>
              </div>
            )}
          </section>

          <aside className="history-section">
            <History />
          </aside>
        </div>
      </main>

      <footer className="app-footer">
        <p>Tourism AI v1.0.0 - Multi-Agent System</p>
      </footer>
    </div>
  );
}

export default App;

