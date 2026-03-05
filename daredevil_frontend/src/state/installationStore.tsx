import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { Installation } from '@/tipos';

type InstallationState = Partial<Installation>;

type Action = {
  updateInstallation: (installation: Installation) => Promise<void>;
  createInstallation: (installation: Installation) => Promise<void>;
}

export const installationStore = create<InstallationState & Action>()(
  persist(
    (set) => ({
      id: undefined,
      appSlug: undefined,
      clientId: undefined,
      gitId: undefined,
      gitAppId: undefined,
      username: undefined,
      updateInstallation: async (installation: Installation) => {
        set({
          id: installation.id,
          appSlug: installation.appSlug,
          clientId: installation.clientId,
          gitId: installation.gitId,
          gitAppId: installation.gitAppId,
          username: installation.username,
        });
      },
      createInstallation: async (installation: Installation) => {
        set({
          id: installation.id,
          appSlug: installation.appSlug,
          clientId: installation.clientId,
          gitId: installation.gitId,
          gitAppId: installation.gitAppId,
          username: installation.username,
        });
      },
    }),
    {
      name: 'installation-storage',
      storage: createJSONStorage(() => typeof window !== 'undefined' ? localStorage : ({
        getItem: () => null,
        setItem: () => {},
        removeItem: () => {},
      } as any)),
    }
  )
);
