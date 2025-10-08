import { ResultAsync } from "neverthrow";
import { type ApiError } from "@/models/error";
import { type User } from "@/models/user";

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
            type: 'NETWORK_ERROR', message: 'Could not create token....'
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


