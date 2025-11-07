
export interface AccessToken {
  expiresAt: string;
  token: string;
}

export interface RefreshToken {
  expiresAt: string;
  token: string;
}

export interface UserTokens {
  accessJwt: AccessToken;
  refreshJwt: RefreshToken;
  username: string;
}

