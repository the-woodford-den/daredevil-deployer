import * as Sentry from "@sentry/react";
import { ResultAsync } from "neverthrow";
import type {
  ErrorState,
  Token,
} from "@/tipos";


const errorHelper = {
  setError: () => { Promise<void> },
  unsetError: () => { Promise<void> },
  isError: true,
}

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;


export const signIn = async (username: string, password: string): Promise<ResultAsync<{ token: Token; setCookieHeader?: string }, ErrorState>> => {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  Sentry.logger.info("User API '/user/login' POST, triggered", { log_source: 'src/api/auths' })

  return ResultAsync.fromPromise(
    fetch(`${BACKEND_URL}/user/login`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      credentials: 'include'
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 404, detail: 'Error Logging In!', isError: true,
        };
      }

      const setCookieHeader = response.headers.get('set-cookie');
      const tokenResponse = await response.json();

      Sentry.logger.info("User API testing cookie if in response...", { log_source: 'src/api/auths' })

      const token = tokenResponse as Token;
      return { token, setCookieHeader: setCookieHeader || undefined };
    }
    ),
    (error) => {

      Sentry.logger.error(`User API error in login, creating cookie: ${error}`, { log_source: 'src/api/auths' })
      const err = error as ErrorState;

      if ('status' in err) {
        return {
          ...err,
          ...errorHelper,
        } as ErrorState
      }

      return {
        status: 401,
        detail: "Authentication Error!",
        ...errorHelper,
      } as ErrorState
    }
  );
};

export const signOut = async (): Promise<ResultAsync<void, ErrorState>> => {
  return ResultAsync.fromPromise(
    fetch(`${BACKEND_URL}/user/logout`, {
      credentials: 'include',
      method: 'DELETE',
      headers: {
        "Accept": "application/json",
        'Content-Type': 'application/json',
      }
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 404, detail: 'Error Logging In!', isError: true,
        };
      }
      const tokenResponse = await response.json();

      return tokenResponse;
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
        status: 500,
        detail: "Logout Error!",
        ...errorHelper,
      } as ErrorState
    }
  );
};
