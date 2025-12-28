// globals.d.ts
export {}; // ensures this file is a module

declare global {
  interface Window {
    __API_URL__: string;
  }
}