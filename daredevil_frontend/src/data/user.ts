export interface User {
  id: string;
  accessToken?: string;
  clientId: string;
  deviceCode?: string;
  userCode?: string;
  verificationUri?: string;
  expiresIn?: string;
  interval?: string;
}
