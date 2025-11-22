import { useState } from 'react';
import type { TourismRequest } from '../types';

interface QueryFormProps {
  onSubmit: (request: TourismRequest) => void;
  isLoading: boolean;
}

export default function QueryForm({ onSubmit, isLoading }: QueryFormProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit({ query: query.trim(), place: null });
      setQuery('');
    }
  };

  const exampleQueries = [
    "I'm going to go to Bangalore, let's plan my trip.",
    "I'm going to go to Bangalore, what is the temperature there?",
    "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?",
  ];

  const handleExampleClick = (example: string) => {
    setQuery(example);
  };

  return (
    <div className="query-form">
      <form onSubmit={handleSubmit} className="form-container">
        <div className="input-group">
          <label htmlFor="query">Ask about any place:</label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., I'm going to go to Bangalore, let's plan my trip."
            rows={3}
            disabled={isLoading}
            className="query-input"
          />
        </div>
        
        <button 
          type="submit" 
          disabled={!query.trim() || isLoading}
          className="submit-button"
        >
          {isLoading ? 'Processing...' : 'Get Tourism Info'}
        </button>
      </form>

      <div className="examples">
        <p className="examples-title">Example queries:</p>
        <div className="example-buttons">
          {exampleQueries.map((example, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleExampleClick(example)}
              disabled={isLoading}
              className="example-button"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

