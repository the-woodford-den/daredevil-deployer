/// <reference types="vitest" />

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '~': path.resolve(__dirname, './src/assets'),
      '@api': path.resolve(__dirname, './src/api'),
      '@components': path.resolve(__dirname, './src/components'),
      '@data': path.resolve(__dirname, './src/data'),
      '@pages': path.resolve(__dirname, './src/pages'),
    },
  },
  test: {
    deps: {
      moduleDirectories: ['node_modules', path.resolve('../../packages')],
    },
    globals: true,
  },
});
