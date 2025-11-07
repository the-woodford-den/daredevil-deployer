import { signIn } from '@/api/auth/user';
import { create } from 'zustand';
import type { ErrorState, Token, UserState } from '@/tipos';

type Action = {
  updateUsername: (username: UserState['username']) => void;
  updatePermissions: (permissions: UserState['permissions']) => void;
  handleSignIn: (password: string, username: string) => Promise<void>;
}

export const userStore = create<UserState & Action>(
  (set) => ({
    hasError: undefined,
    username: undefined,
    permissions: undefined,
    loading: false,
    updateUsername: (username) => set(() => ({ username: username })),
    updatePermissions: (permissions) => set(() => ({ permissions: permissions })),
    handleSignIn: async (
      password: string,
      username: string,
    ) => {
      set({ loading: true });
      const result = await signIn(password, username);
      result.match(
        (token: Token) => set({ username: token.username }),
        (err: ErrorState) => set({ hasError: err.isError }),
      );
    },
    handleSignOut: async () => {
      // await signOut();
      set({
        username: undefined,
        permissions: undefined,
        loading: false,
      });
    },
    togglePermissions: () =>
      set((state) =>
        state.permissions?.length === 0
          ? { permissions: ['admin'] }
          : { permissions: [] },
      ),
  }),
);

