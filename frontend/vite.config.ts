import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  root: path.resolve(__dirname, 'src'),
  base: '/',
  server: {
    port: 3000,
    strictPort: true,
    cors: true,
  },
  build: {
    manifest: true,
    outDir: path.resolve(__dirname, '../backend/static'),
    rollupOptions: {
      input: path.resolve(__dirname, 'src/main.tsx'),  // Note: Changed to .tsx
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
})