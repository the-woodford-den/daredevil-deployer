import * as Sentry from "@sentry/react";
import { ResultAsync } from "neverthrow";
import type {
  ErrorState,
  User,
} from "@/tipos";


const errorHelper = {
  setError: () => { Promise<void> },
  unsetError: () => { Promise<void> },
  isError: true,
}

export const createUser = async (
  password: string,
  email: string,
  username: string
): Promise<ResultAsync<User, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = JSON.stringify({
    username: username,
    password: password,
    email: email
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/user/create`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include'
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: response.status,
          detail: 'User not created!',
          isError: true,
        };
      }
      const userResponse = await response.json();
      const user = userResponse as User;

      return user;
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
        detail: "Cannot Create User Error!",
      } as ErrorState
    }
  );
};


export const getCurrentUser = async (cookieHeader?: string): Promise<ResultAsync<User, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (cookieHeader) {
    headers['Cookie'] = cookieHeader;
  }

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/user/me`, {
      method: 'GET',
      headers,
      credentials: 'include',
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: response.status,
          detail: 'Failed to verify user session!',
          isError: true,
        };
      }
      Sentry.logger.info("User session verified from token", { log_source: 'src/api/users' });
      const userResponse = await response.json();
      const user = userResponse as User;

      return user;
    }),
    (error) => {
      Sentry.logger.error(`Error verifying user session: ${error}`, { log_source: 'src/api/users' });
      const err = error as ErrorState;

      if ('status' in err) {
        return {
          ...err,
          ...errorHelper,
        } as ErrorState;
      }

      return {
        ...errorHelper,
        status: 401,
        detail: "Authentication Error!",
      } as ErrorState;
    }
  );
};

