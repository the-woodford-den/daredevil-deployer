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


export const findInstallation = async (): Promise<ResultAsync<Installation, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  // request.headers.get("Cookie")

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    // 'Cookie' = cookieHeader,
  };


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

export const findApp = async (): Promise<ResultAsync<App, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    //    headers['Cookie'] = cookieHeader;
  };


  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/git/app/`, {
      credentials: 'include',
      method: 'GET',
      headers
    })
      .then(async (response) => {
        if (!response.ok) {
          throw {
            status: 422, detail: 'No GitApp Found.'
          };
        }
        console.log(response)
        const appResponse = await response.json();
        console.log(appResponse)
        const gitApp = appResponse as App;
        console.log(gitApp)

        console.log(appResponse);
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
        detail: "Cannot Grab GitApp!",
        ...errorHelper,
      } as ErrorState
    }
  );
};

