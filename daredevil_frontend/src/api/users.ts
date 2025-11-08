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
      headers: { 'Content-Type': 'application/json' }
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

