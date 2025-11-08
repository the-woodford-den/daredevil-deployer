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


export const signIn = async (username: string, password: string): Promise<ResultAsync<Token, ErrorState>> => {
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
      const cookie = response.headers.get('Cookie')
      const set_cookie = response.headers.get('Set-Cookie')
      console.log(cookie)
      console.log(set_cookie)
      const tokenResponse = await response.json();
      const acookie = tokenResponse.headers.get('Cookie')
      const aset_cookie = tokenResponse.headers.get('Set-Cookie')
      console.log(acookie)
      console.log(aset_cookie)
      const token = tokenResponse as Token;

      return token;
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
        status: 401,
        detail: "Authentication Error!",
        ...errorHelper,
      } as ErrorState
    }
  );
};

export const signOut = async (): Promise<ResultAsync<void, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/user/logout`, {
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
