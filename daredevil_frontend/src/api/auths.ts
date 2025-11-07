import { ResultAsync } from "neverthrow";
import { errorStore } from '@/state/errorStore';
import type {
  ErrorState,
  Token,
} from "@/tipos";


const errorHelper = {
  setError: () => { Promise<void> },
  unsetError: () => { Promise<void> },
  isError: true,
}


export const signIn = (username: string, password: string): ResultAsync<Token, ErrorState> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = JSON.stringify({
    username: username,
    password: password
  });


  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/user/login`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/json' }
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 404, detail: 'Error Logging In!', isError: true,
        };
      }
      const tokenResponse = await response.json();
      console.log(tokenResponse);
      const token = tokenResponse as Token;

      return token;
    }
    ),
    (error) => {
      const setError = errorStore((state) => state.setError);
      const err = error as ErrorState;
      setError(err);

      if ('status' in err) {
        return {
          ...err,
          ...errorHelper,
        } as ErrorState
      }

      return {
        status: 404,
        detail: "Cannot Create User Error!",
        ...errorHelper,
      } as ErrorState
    }
  );
};

export const signOut = (): ResultAsync<void, ErrorState> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/user/logout`, {
      method: 'POST',
      headers: {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        "Authorization": `Bearer ${jwt}`,
      }
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 404, detail: 'Error Logging In!', isError: true,
        };
      }
      const tokenResponse = await response.json();
      console.log(tokenResponse);

      return tokenResponse;
    }
    ),
    (error) => {
      const setError = errorStore((state) => state.setError);
      const err = error as ErrorState;
      setError(err);

      if ('status' in err) {
        return {
          ...err,
          ...errorHelper,
        } as ErrorState
      }

      return {
        status: 404,
        detail: "Cannot Create User Error!",
        ...errorHelper,
      } as ErrorState
    }
  );
};
