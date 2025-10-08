import { ResultAsync } from 'neverthrow';
import { type Repository } from '@/models/repository';
import { type User } from '@/models/user';
import { type ApiError } from '@/models/error';

// clientId: client_id
// deviceCode: device_code
// userCode: user_code
// verificationUri: verification_uri
// expiresIn: expires_in
// interval: interval

export const createToken = (clientId: string): ResultAsync<User, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    client_id: clientId
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/create-token?${params}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'Could not create token'
          };
        }
        const userResponse = await response.json();
        const userObject = {
          clientId: clientId,
          deviceCode: userResponse.device_code,
          userCode: userResponse.user_code,
          verificationUri: userResponse.verification_uri,
        } as User;

        return userObject;
      }
      ),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

export const getRepos = (token: string): ResultAsync<Repository[], ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    user_token: token
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/repos?${params}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'Could not fetch Repositories.'
          };
        }
        return (await response.json()) as Repository[];
      }
      ),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};
