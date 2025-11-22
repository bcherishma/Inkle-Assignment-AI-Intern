import type { TourismResponse } from '../types';

interface ResultsProps {
  response: TourismResponse | null;
  isLoading: boolean;
}

export default function Results({ response, isLoading }: ResultsProps) {
  if (isLoading) {
    return (
      <div className="results loading">
        <div className="spinner"></div>
        <p>Processing your query...</p>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="results empty">
        <p>Enter a query above to get tourism information.</p>
      </div>
    );
  }

  if (!response.success && response.error) {
    return (
      <div className="results error">
        <h3>Error</h3>
        <p>{response.message || response.error}</p>
      </div>
    );
  }

  return (
    <div className="results">
      <div className="result-content">
        {response.weather && (
          <div className="weather-section">
            <h3>🌤️ Weather Information</h3>
            <div className="weather-details">
              <p>
                <strong>Temperature:</strong> {response.weather.temperature}°C
              </p>
              <p>
                <strong>Rain Probability:</strong> {response.weather.rain_probability}%
              </p>
            </div>
          </div>
        )}

        {response.places && response.places.length > 0 && (
          <div className="places-section">
            <h3>📍 Tourist Attractions</h3>
            <ul className="places-list">
              {response.places.map((place, idx) => (
                <li key={idx} className="place-item">
                  <strong>{place.name}</strong>
                  {place.type && <span className="place-type">({place.type})</span>}
                  {place.description && <p className="place-description">{place.description}</p>}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="message-section">
          <h3>Response</h3>
          <p className="message-text">{response.message}</p>
        </div>
      </div>
    </div>
  );
}

