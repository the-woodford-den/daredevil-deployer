import { create } from 'zustand';
import { signIn, signOut, createUser } from '@/api';
import type { ErrorState, User, UserState } from '@/tipos';
import { ResultAsync } from "neverthrow";

type Action = {
  updateUsername: (username: UserState['username']) => Promise<ResultAsync<void, ErrorState>>;
  handleSignIn: (password: string, username: string) => Promise<ResultAsync<User, ErrorState>>;
  handleSignOut: (password: string, username: string) => Promise<ResultAsync<void, ErrorState>>;
  createUser: (password: string, email: string, username: string) => Promise<ResultAsync<User, ErrorState>>;
}

export const userStore = create<UserState & Action>(
  (set) => ({
    hasError: false,
    username: "ss",
    loading: false,
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
    handleSignIn: async (
      password: string,
      username: string,
    ) => {
      set({
        hasError: false,
        loading: true,
        username: username,
      });
      const result = await signIn(username, password);
      result.match(
        (data) => set({ username: data.username, loading: false, hasError: false }),
        (err: ErrorState) => set({ hasError: err.isError, loading: false }),
      );
      return result;
    },
    handleSignOut: async () => {
      set({
        hasError: false,
        loading: true,
      });
      const result = await signOut();
      result.match(
        (err: ErrorState) => set({ hasError: err.isError, loading: false }),
      );
    },
    updateUsername: (username) => set(() => ({ username: username })),
  }),
);

