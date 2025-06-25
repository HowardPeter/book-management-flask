import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth-api': {
        target: 'http://host.docker.internal:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/auth-api/, ''),
      },
      '/books-api': {
        target: 'http://host.docker.internal:5001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/books-api/, ''),
      }
    }
  }
})
