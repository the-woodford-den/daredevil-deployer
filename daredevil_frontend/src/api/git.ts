import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type App,
  type Installation,
  type Token
} from "@/data";


export const searchGitInstalls = (username: string): ResultAsync<Installation, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    username: username
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/installs/search/${username}`).then(async (response) => {
      if (!response.ok) {
        throw {
          type: 'NETWORK_ERROR', message: 'No Tokens....'
        };
      }

      const installResponse = await response.json();
      const installObject = installResponse as Installation;

      console.log(installResponse);
      return installObject;
    }),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

export const searchGitApps = (slug: string): ResultAsync<App, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/search/${slug}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'No Tokens....'
          };
        }
        const appResponse = await response.json();
        const appObject = appResponse as App;

        console.log(appResponse);
        return appObject;
      }),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

export const createGitInstallToken = (id: number): ResultAsync<Token, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = JSON.stringify({ id });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/install/token`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/json' }
    })
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'No Token.....'
          };
        }
        const tokenResponse = await response.json();
        const tokenObject = tokenResponse as Token;

        console.log(tokenResponse);
        return tokenObject;
      }),
    (error) => {
      if (error && typeof error == 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

