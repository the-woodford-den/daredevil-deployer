import { signIn, signOut } from '@/api/auth';
import { create } from 'zustand';
import { type UserState } from '@/tipos';

export const userStore = create<UserState>(
  (set) => ({
    username: undefined,
    permissions: undefined,
    loading: false,
    handleSignIn: async () => {
      set({ loading: true });
      const user = await signIn();
      set({
        username: user.username,
        permissions: user.permissions,
        loading: false,
      });
    },
    handleSignOut: async () => {
      await signOut();
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

