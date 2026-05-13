import path from "node:path"

import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

const REVIEW_API_PROXY_TARGET = process.env.REVIEW_API_PROXY_TARGET ?? "http://127.0.0.1:8889"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@web": path.resolve(__dirname, "../web/src"),
    },
  },
  server: {
    port: 5174,
    proxy: {
      "/api": {
        target: REVIEW_API_PROXY_TARGET,
        changeOrigin: true,
      },
    },
  },
  preview: {
    port: 5174,
  },
})
