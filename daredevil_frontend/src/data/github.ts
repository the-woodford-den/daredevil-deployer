// import type { UUID } from "crypto";

export interface GithubTokenResponse {
  clientId?: string;
  installId?: string;
  token: string;
  expires_at: string;
}
