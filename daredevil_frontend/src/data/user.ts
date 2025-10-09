export interface User {
  accessToken?: string;
  clientId: string;
  deviceCode?: string;
  userCode?: string;
  verificationUri?: string;
  expiresIn?: string;
  interval?: string;
}

// clientId: client_id
//
// deviceCode: device_code
// userCode: user_code
// verificationUri: verification_uri
// expiresIn: expires_in
// interval: interval
