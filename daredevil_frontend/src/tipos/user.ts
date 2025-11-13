import type { ResultAsync } from 'neverthrow';
import type { ErrorState } from './error';
import type { UUID } from './utility';


export interface Token {
  expiresAt: string;
  token: string;
  username: undefined | string;
}

export interface User {
  id: UUID;
  clientId: string;
  email: string;
  gitId: string;
  token: string;
  username: string;
}

export type UserState = {
  hasError: undefined | boolean;
  username: undefined | string;
  cookie: undefined | string;
  loading: boolean;
  handleSignIn: (
    username: string,
    password: string,
  ) => Promise<ResultAsync<User, ErrorState>>;
  handleSignOut: (
    username: string,
    password: string,
  ) => Promise<ResultAsync<void, ErrorState>>;
  createUser: (
    username: string,
    email: string,
    password: string,
  ) => Promise<ResultAsync<User, ErrorState>>;
}
