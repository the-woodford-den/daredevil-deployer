/// <reference types="vite/client" />
import type { TestingLibraryMatchers } from '@testing-library/jest-dom/matchers';

declare global {
  namespace jest {
    interface Matchers<R = void>
      extends TestingLibraryMatchers<typeof expect.stringContaining, R> { }
  }
}

declare module "*.json" {
  const value: any;
  export default value;
}
