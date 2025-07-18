// vite.config.js
export default {
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: [
      "localhost",
      "127.0.0.1",
      "4133867a-6e54-44ee-b824-d3a7d29d8030-00-16cbyzffwq8v3.spock.replit.dev" // <- adicionado
    ],
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
}