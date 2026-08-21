import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: [
        'src/components/**/*.ts',
        'src/components/**/*.tsx',
        'src/features/**/*.ts',
        'src/features/**/*.tsx',
        'src/hooks/**/*.ts',
        'src/services/**/*.ts',
        'src/utils/**/*.ts',
      ],
    },
  },
});
