# Tourism AI Frontend

React + TypeScript frontend for the Tourism AI Multi-Agent System.

## Features

-  Modern, responsive UI
-  Real-time query processing
-  Query history and statistics
-  Example queries for quick testing
-  Persistent query history

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Axios** - HTTP client

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

2. **Configure environment** (optional):
   ```bash
   cp .env.example .env.local
   # Edit .env.local if backend URL is different from http://localhost:8000
   ```

3. **Run development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Build for production**:
   ```bash
   npm run build
   # or
   yarn build
   ```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   │   ├── QueryForm.tsx    # Query input form
│   │   ├── Results.tsx      # Results display
│   │   └── History.tsx      # Query history
│   ├── services/        # API service layer
│   │   └── api.ts           # API client
│   ├── types/          # TypeScript types
│   │   └── index.ts         # Type definitions
│   ├── App.tsx         # Main app component
│   ├── App.css         # App styles
│   ├── main.tsx        # React entry point
│   └── index.css       # Global styles
├── public/             # Static assets
├── index.html          # HTML template
├── package.json        # Dependencies
├── vite.config.ts      # Vite config
└── tsconfig.json       # TypeScript config
```

## API Integration

The frontend communicates with the backend API through the service layer (`src/services/api.ts`). All API calls are centralized here for easy maintenance.

## Development

- The dev server runs on `http://localhost:5173` by default
- Hot module replacement (HMR) is enabled
- API proxy is configured in `vite.config.ts` to forward `/api/*` requests to the backend

