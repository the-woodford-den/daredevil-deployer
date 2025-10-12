// Github Response Types 

export interface GithubAppResponse {
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

interface GithubInstallAccount {
  name?: string;
  email?: string;
  login: string;
  id: number;
}


export interface GithubInstallResponse {
  id: number;
  account: GithubInstallAccount;
  events: string[];
  appId: number;
  appSlug: string;
  accessTokensUrl: string;
  htmlUrl: string;
  repositoriesUrl: string;
}

export interface GithubTokenResponse {
  clientId?: string;
  installId?: string;
  token: string;
  expires_at: string;
}
