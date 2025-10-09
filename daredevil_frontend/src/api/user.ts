import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type User
} from "@/data";

export const createToken = (clientId: string): ResultAsync<User, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    client_id: clientId
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/create-token?${params}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          type: 'NETWORK_ERROR', message: 'Could not create token....'
        };
      }
      const userResponse = await response.json();
      const userObject = {
        clientId: clientId,
        deviceCode: userResponse.device_code,
        userCode: userResponse.user_code,
        verificationUri: userResponse.verification_uri,
        id: userResponse.id
      } as User;
      console.log(userResponse);

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


