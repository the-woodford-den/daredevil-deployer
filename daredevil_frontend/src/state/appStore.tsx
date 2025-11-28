import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { App } from '@/tipos';

type Action = {
  updateApp: (app: App) => Promise<void>;
  createApp: (app: App) => Promise<void>;
}

export const appStore = create<App & Action>()(
  persist(
    (set) => ({
      id: undefined,
      clientId: undefined,
      description: undefined,
      events: [],
      gitId: undefined,
      name: undefined,
      permissions: {},
      createdAt: undefined,
      updatedAt: undefined,
      updateApp: async (
        app: App,
      ) => {
        set({
          id: app["id"],
          clientId: app["clientId"],
          description: app["description"],
          gitId: app["gitId"],
          name: app["name"],
        });
      },
      createApp: async (
        app: App,
      ) => {
        set({
          id: app["id"],
          clientId: app["clientId"],
          description: app["description"],
          gitId: app["gitId"],
          name: app["name"],
        });
      },
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);

