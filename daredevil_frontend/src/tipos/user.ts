import type { UUID } from './utility';


export interface UserCookie {
  key: string;
  value: string;
  httponly: boolean;
  samesite: string;
  path: string;
  expires: string;
  secure?: boolean;
  domain?: string;
}

export interface User {
  id: UUID;
  clientId?: string;
  email: string;
  gitId?: string;
  cookie?: string;
  username: string;
}

export type UserState = {
  username: undefined | string;
  email: undefined | string;
  clientId: undefined | string;
  gitId: undefined | number;
  cookie: undefined | string;
  loading: boolean;
  handleSignIn: (
    user: User,
  ) => Promise<void>;
  handleSignOut: (
    username: string,
    password: string,
  ) => Promise<void>;
  createUser: (
    user: User,
  ) => Promise<void>;
}
