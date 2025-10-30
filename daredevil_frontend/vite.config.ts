/// <reference types="vitest" />

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '~': path.resolve(__dirname, './src/assets'),
      '!': path.resolve(__dirname, './tests'),
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
