import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type App,
  type Installation,
  type Token,
  // type User,
} from "@/tipos";


export const findInstallation = (token: string, username: string): ResultAsync<Installation, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = JSON.stringify({ username, token });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/installation`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/json' }
    })
      .then(async (response) => {
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

export const findApp = (token: string, username: string): ResultAsync<App, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = JSON.stringify({ username, token });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/json' }
    })
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

export const createGitToken = (gitId: string): ResultAsync<Token, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = JSON.stringify({ installation_id: gitId });

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

