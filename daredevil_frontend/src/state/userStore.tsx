import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User, UserState } from '@/tipos';

type Action = {
  updateUsername: (user: User) => Promise<void>;
  handleSignIn: (user: User) => Promise<void>;
  handleSignOut: () => Promise<void>;
  createUser: (user: User) => Promise<void>;
}

export const userStore = create<UserState & Action>()(
  persist(
    (set) => ({
      username: undefined,
      email: undefined,
      clientId: undefined,
      cookie: undefined,
      loading: false,
      gitId: undefined,
      createUser: async (
        user: User,
      ) => {
        set({
          username: user["username"],
          email: user["email"],
          gitId: Number(user["gitId"]),
        });
      },
      handleSignIn: async (
        user: User,
      ) => {
        set({
          cookie: user["cookie"],
          gitId: Number(user["gitId"]),
          username: user["username"],
          email: user["email"],
        });
      },
      handleSignOut: async () => {
        set({
          username: undefined,
          email: undefined,
          cookie: undefined,
          gitId: undefined,
        });
      },
      updateUsername: async (
        user: User
      ) => {
        set({
          username: user["username"]
        })
      },
    }),
    {
      name: 'user-storage',
      storage: createJSONStorage(() => typeof window !== 'undefined' ? localStorage : ({
        getItem: () => null,
        setItem: () => {},
        removeItem: () => {},
      } as any)),
    }
  )
);

