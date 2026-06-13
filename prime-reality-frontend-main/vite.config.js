import { defineConfig } from "vite";

import react from "@vitejs/plugin-react";

// vite configuration
// aliases aur dev server config yahan manage hoga

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      "@": "/src",
    },
  },

  server: {
    port: 5173,

    open: true,
  },
});