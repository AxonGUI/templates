import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";
import { axonTypes } from "axon-gui/vite-plugin";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), axonTypes({ args: ["--controllers", "../controller", "--out", "src/axon.generated.ts"] })],
  server: {
    host: "127.0.0.1",
    port: 5173,
  },
});
