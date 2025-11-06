import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type App,
  type Installation,
  type Token,
  type User,
} from "@/tipos";


export const findInstallation = (user: User): ResultAsync<Installation, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/installation`).then(async (response) => {
      if (!response.ok) {
        throw {
          type: 'NETWORK_ERROR', message: 'No Tokens....'
        };
      }

      const installResponse = await response.json();
      const installation = installResponse as Installation;

      console.log(installResponse);
      return installation;
    }),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

export const findApp = (user: User): ResultAsync<App, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'No Tokens....'
          };
        }
        const appResponse = await response.json();
        const gitApp = appResponse as App;

        console.log(appResponse);
        return gitApp;
      }),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

export const createGitToken = (user: User): ResultAsync<Token, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  // const params = JSON.stringify({ git_id: user.git_id });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/token`, {
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

