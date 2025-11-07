import { ResultAsync } from "neverthrow";
import {
  type ErrorState,
  type User,
  type Token,
} from "@/tipos";
import { errorStore } from '@/state/errorStore';


const errorHelper = {
  setError: () => { Promise<void> },
  unsetError: () => { Promise<void> },
  isError: true,
}


export const createUser = (password: string, username: string): ResultAsync<User, ErrorState> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const setError = errorStore(
    (state) => state.setError
  );
  const params = JSON.stringify({
    username: username,
    password: password
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/user/create`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/json' }
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 404, detail: 'User not created!', isError: true,
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
        setError(err);
        return {
          ...err,
          ...errorHelper,
        } as ErrorState

      }
      return {
        ...errorHelper,
        status: 404,
        detail: "Cannot Create User Error!",
      } as ErrorState
    }
  );
};


export const signIn = (username: string, password: string): ResultAsync<Token, ErrorState> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const setError = errorStore((state) => state.setError);
  const params = JSON.stringify({
    username: username,
    password: password
  });


  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/user/create`, {
      method: 'POST',
      body: params,
      headers: { 'Content-Type': 'application/json' }
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 404, detail: 'Error SignIn!', isError: true,
        };
      }
      const tokenResponse = await response.json();
      console.log(tokenResponse);
      const token = tokenResponse as Token;

      return token;
    }
    ),
    (error) => {
      const err = error as ErrorState;
      if ('status' in err) {
        setError(err);
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
