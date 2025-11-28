import * as Sentry from "@sentry/react";
import { ResultAsync } from "neverthrow";
import type {
  App,
  ErrorState,
  Installation,
} from "@/tipos";

const errorHelper = {
  setError: () => { Promise<void> },
  unsetError: () => { Promise<void> },
  isError: true,
}

export const getInstall = async (cookieHeader?: string): Promise<ResultAsync<Installation, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (cookieHeader) {
    headers['Cookie'] = cookieHeader;
  }


  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/installation`, {
      credentials: 'include',
      method: 'GET',
      headers
    })
      .then(async (response) => {
        if (!response.ok) {
          throw {
            stauts: 404, detail: 'No GitApp Installation Found.'
          };
        }

        const installResponse = await response.json();
        const installation = installResponse as Installation;

        return installation;
      }),
    (error) => {
      const err = error as ErrorState;

      if ('status' in err) {
        return {
          ...err,
          ...errorHelper,
        } as ErrorState
      }

      return {
        status: 404,
        detail: "Cannot Grab User Installation!",
        ...errorHelper,
      } as ErrorState
    }
  );
};

export const getApp = async (cookieHeader?: string): Promise<ResultAsync<App, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (cookieHeader) {
    headers['Cookie'] = cookieHeader;
  }

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git_app/`, {
      method: 'GET',
      headers,
      credentials: 'include',
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 422, detail: 'No GitApp Found.'
        };
      }
      console.log(response, "INITIAL");
      const appResponse = await response.json();
      console.log(appResponse, "JSON");
      const gitApp = appResponse as App;
      console.log(gitApp, "APP");
      return gitApp;
    }),
    (error) => {
      const err = error as ErrorState;

      if ('status' in err) {
        return {
          ...err,
          ...errorHelper,
        } as ErrorState
      }

      return {
        status: 404,
        detail: "Cannot Grab GitApp.",
        ...errorHelper,
      } as ErrorState
    }
  );
};

export const createApp = async (
  clientId: string,
  cookieHeader?: string,
): Promise<ResultAsync<App, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = JSON.stringify({
    clientId: clientId,
  });
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (cookieHeader) {
    headers['Cookie'] = cookieHeader;
  }

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git_app/create`, {
      method: 'POST',
      body: params,
      headers: headers,
      credentials: 'include'
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: response.status,
          detail: 'Git App not created!',
          isError: true,
        };
      }
      const appResponse = await response.json();
      console.log(response, "INITIAL");
      const app = appResponse as App;
      console.log(appResponse, "JSON");
      console.log(app, "APP");

      return app;
    }
    ),
    (error) => {
      const err = error as ErrorState;

      if ('status' in err) {
        return {
          ...err,
          ...errorHelper,
        } as ErrorState

      }

      return {
        ...errorHelper,
        status: 500,
        detail: "Cannot Create Git App.",
      } as ErrorState
    }
  );
};
