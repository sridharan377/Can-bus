import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // Ensure the alias is correctly set
    },
  },
  server: {
    host: '0.0.0.0',  // Expose to network (optional)
    port: 5173,       // Keep the port
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://192.168.43.245:5000', // Your Flask backend URL
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
