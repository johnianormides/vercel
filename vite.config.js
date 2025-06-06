import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";

export default defineConfig({
	plugins: [vue()],
	optimizeDeps: {
		include: ["@stackblitz/sdk"],
	},
	base: "/",
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
	},
	build: {
		rollupOptions: {
			input: {
				app: fileURLToPath(new URL("./index.html", import.meta.url)),
			},
		},
		outDir: "dist",
		assetsDir: "assets",
		sourcemap: true,
		emptyOutDir: true
	},
	server: {
		port: 3000,
		host: true,
		strictPort: true,
		proxy: {
			'/api': {
				target: process.env.VITE_API_URL || 'http://localhost:5000',
				changeOrigin: true,
				secure: false
			}
		}
	},
	define: {
		VUE_PROD_HYDRATION_MISMATCH_DETAILS: "false",
		VUE_PROD_DEVTOOLS: "false",
		"process.env": {},
		global: {},
	},
});
