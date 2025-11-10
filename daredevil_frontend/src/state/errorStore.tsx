import { create } from 'zustand';
import type { ErrorState } from '@/tipos';


type Action = {
  setError: (error: ErrorState) => Promise<void>;
  unsetError: (error: ErrorState) => Promise<void>;
}

export const errorStore = create<ErrorState & Action>(
  (set) => ({
    isError: false,
    status: undefined,
    detail: undefined,
    setError: async () => {
      set((error: ErrorState) => ({
        isError: error.isError,
        status: error.status,
        detail: error.detail,
      }));
    },
    unsetError: async () => {
      set({
        isError: false,
        status: undefined,
        detail: undefined,
      });
    },
  }),
);

