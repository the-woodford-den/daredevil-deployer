import { create } from 'zustand';
import { signIn, signOut, createUser } from '@/api';
import type { ErrorState, Token, UserState } from '@/tipos';

type Action = {
  updateUsername: (username: UserState['username']) => void;
  updatePermissions: (permissions: UserState['permissions']) => void;
  handleSignIn: (password: string, username: string) => Promise<void>;
  handleSignOut: () => Promise<void>;
  createUser: (password: string, email: string, username: string) => Promise<void>;
}

export const userStore = create<UserState & Action>(
  (set) => ({
    hasError: false,
    username: "ss",
    permissions: ['admin'],
    loading: false,
    updateUsername: (username) => set(() => ({ username: username })),
    updatePermissions: (permissions) => set(() => ({ permissions: permissions })),
    handleSignIn: async (
      password: string,
      username: string,
    ) => {
      set({
        hasError: false,
        loading: true,
        username: username,
      });
      const result = await signIn(password, username);
      result.match(
        (token: Token) => set({ username: token.username }),
        (err: ErrorState) => set({ hasError: err.isError }),
      );
    },
    createUser: async (
      password: string,
      email: string,
      username: string,
    ) => {
      const result = await createUser(password, email, username);
      result.match(
        (token) => set({ username: token.username }),
        (err) => set({ hasError: err.isError }),
      );
    },
    handleSignOut: async () => {
      set({
        hasError: false,
        loading: true,
      });
      const result = await signOut();
      result.match(
        () => set({ username: undefined, permissions: [], loading: false }),
        (err: ErrorState) => set({ hasError: err.isError, loading: false }),
      );
    },
    togglePermissions: () =>
      set((state) =>
        state.permissions?.length === 0
          ? { permissions: ['admin'] }
          : { permissions: [] },
      ),
  }),
);

