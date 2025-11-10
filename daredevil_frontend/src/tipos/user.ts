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
  permissions: undefined | string[];
  loading: boolean;
  handleSignIn: (
    username: string,
    password: string,
  ) => Promise<any>;
  createUser: (
    username: string,
    email: string,
    password: string,
  ) => Promise<void>;
  togglePermissions: () => void;
}
