import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type GithubTokenResponse
} from "@/data";

export const getAccessTokenGithubApp = (clientId: string): ResultAsync<GithubTokenResponse, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    client_id: clientId
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/create-installation-token?${params}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          type: 'NETWORK_ERROR', message: 'No Tokens....'
        };
      }
      const tokenResponse = await response.json();
      const appObject = {
        clientId: clientId,
        token: tokenResponse.token,
        expires_at: tokenResponse.expires_at
      } as GithubTokenResponse;

      console.log(appObject);
      return appObject;
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
