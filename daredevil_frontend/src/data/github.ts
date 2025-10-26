// Github Response Types 

export interface App {
  id: string;
  clientId: string;
  nodeId: string;
  owner: {};
  name: string;
  description: string;
  externalUrl: string;
  htmlUrl: string;
  createdAt: string;
  updatedAt: string;
  permissions: {};
  events: string[];
}

interface InstallRecordAccount {
  name?: string;
  email?: string;
  login: string;
  id: number;
}


export interface Installation {
  id: number;
  account: InstallRecordAccount;
  events: string[];
  appId: number;
  appSlug: string;
  accessTokensUrl: string;
  htmlUrl: string;
  repositoriesUrl: string;
}

export interface Token {
  token: string;
  expiresAt: string;
}
