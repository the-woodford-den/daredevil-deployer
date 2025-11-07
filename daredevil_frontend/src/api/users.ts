import { ResultAsync } from "neverthrow";
import { errorStore } from '@/state';
import type {
  ErrorState,
  User,
} from "@/tipos";


const errorHelper = {
  setError: () => { Promise<void> },
  unsetError: () => { Promise<void> },
  isError: true,
}

export const createUser = async (password: string, username: string): Promise<ResultAsync<User, ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
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
      const setError = errorStore(
        (state) => state.setError
      );
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

