import { create } from 'zustand';
import type { User, UserState } from '@/tipos';

type Action = {
  updateUsername: (user: User) => Promise<void>;
  handleSignIn: (user: User) => Promise<void>;
  handleSignOut: () => Promise<void>;
  createUser: (user: User) => Promise<void>;
}

export const userStore = create<UserState & Action>(
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
        clientId: user["clientId"],
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
        clientId: user["clientId"],
      });
    },
    handleSignOut: async () => {
      set({
        cookie: undefined
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
);

