// Github Response Types 
import { type UUID } from './utility';

export interface App {
  id: UUID;
  gitId: string;
  name: string;
  description: string;
  createdAt: string;
  updatedAt: string;
  permissions: {};
  events: string[];
}

export interface Installation {
  id: UUID;
  appSlug: string;
  gitId: number;
  gitAppId: number;
  username: string;
}

export interface Token {
  token: string;
  expiresAt: string;
}
