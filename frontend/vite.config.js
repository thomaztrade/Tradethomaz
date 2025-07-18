// vite.config.js
export default {
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: ["*"],
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
}