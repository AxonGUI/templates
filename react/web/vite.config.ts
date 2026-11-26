import { defineConfig } from "vite";
import { axonTypes } from "axon-gui/vite-plugin";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react(), axonTypes()],
  server: { port: 5173, strictPort: true },
});
