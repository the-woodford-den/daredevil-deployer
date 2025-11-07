
export interface Repository {
  branchesUrl: string;
  defaultBranch: string;
  description: string;
  eventsUrl: string;
  fullName: string;
  gitId: string;
  gitUrl: string;
  homepage: string;
  hooksUrl: string;
  htmlUrl: string;
  language: string;
  name: string;
  notificationsUrl: string;
  private: boolean;
  pushedAt: string;
  size: number;
  sshUrl: string;
  subscribersCount: number;
  url: string;
  visibility: string;
  watchersCount: number;
};

export interface ReposState {
  repos: Set<Repository>;
  handleGetRepos: () => Promise<void>;
  hasError: boolean;
};

