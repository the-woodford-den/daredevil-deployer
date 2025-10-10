import type { UUID } from "crypto";

export interface GithubApp {
  id: UUID;
  slug: string;
  nodeId: string;
  clientId: string;
  name: string;
  externalUrl: string;
  htmlUrl: string;
  createdAt: string;
  updatedAt: string;
  githubAppId: string;
}
