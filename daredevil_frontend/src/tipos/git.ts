// Github Response Types 
import type { UUID } from './utility';

export interface App {
  id: UUID | undefined;
  clientId: string | undefined;
  description: string | undefined;
  events: string[] | [];
  gitId: string | undefined;
  name: string | undefined;
  permissions: {};
  createdAt: string | undefined;
  updatedAt: string | undefined;
}

export interface Installation {
  id: UUID;
  appSlug: string;
  clientId: string;
  gitId: number;
  gitAppId: number;
  username: string;
}

