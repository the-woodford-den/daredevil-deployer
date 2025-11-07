// Github Response Types 
import type { UUID } from './utility';

export interface App {
  id: UUID;
  clientId: string;
  description: string;
  events: string[];
  gitId: string;
  name: string;
  permissions: {};
  createdAt: string;
  updatedAt: string;
}

export interface Installation {
  id: UUID;
  appSlug: string;
  clientId: string;
  gitId: number;
  gitAppId: number;
  username: string;
}

