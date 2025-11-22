import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    // Allow all hosts (for Render deployment)
    allowedHosts: [
      'localhost',
      '.onrender.com', // Allow all Render subdomains
      '.railway.app',  // Allow Railway if needed
      '.vercel.app'    // Allow Vercel if needed
    ],
    proxy: {
      '/api': {
        target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: process.env.PORT ? parseInt(process.env.PORT) : 4173,
    // Allow all hosts for preview (production build)
    allowedHosts: [
      'localhost',
      '.onrender.com',
      '.railway.app',
      '.vercel.app'
    ]
  }
})

