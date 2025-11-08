/// <reference types="vitest" />

import { defineConfig } from 'vite';
import { reactRouter } from "@react-router/dev/vite";
import tsconfigPaths from 'vite-tsconfig-paths';
import path from 'path';

export default defineConfig({
  plugins: [
    reactRouter(),
    tsconfigPaths()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '~': path.resolve(__dirname, './src/assets'),
      '!': path.resolve(__dirname, './tests'),
    },
  },
  server: {
    proxy: {
      '/user': {
        target: 'http://127.0.0.1:4000',
        changeOrigin: true,
      },
      '/git': {
        target: 'http://127.0.0.1:4000',
        changeOrigin: true,
      },
      '/github': {
        target: 'http://127.0.0.1:4000',
        changeOrigin: true,
      },
    },
  },
  test: {
    deps: {
      moduleDirectories: ['node_modules', path.resolve('../../packages')],
    },
    environment: "jsdom",
    globals: true,
    setupFiles: "./tests/setup.ts",
  },
});
