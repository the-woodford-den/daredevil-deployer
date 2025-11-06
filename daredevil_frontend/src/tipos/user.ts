import { type UUID } from './utility';

export interface User {
  id: UUID;
  clientId: string;
  email: string;
  gitId: string;
  token: string;
  username: string;
}

export type UserState = {
  username: undefined | string;
  permissions: undefined | string[];
  loading: boolean;
  handleSignIn: () => Promise<void>;
  handleSignOut: () => Promise<void>;
  togglePermissions: () => void;
}
