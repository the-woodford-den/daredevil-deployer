import { ResultAsync } from 'neverthrow';
import type {
  ErrorState,
  Repository,
} from '@/tipos';

const errorHelper = {
  setError: () => { Promise<void> },
  unsetError: () => { Promise<void> },
  isError: true,
}


export const getRepos = async (): Promise<ResultAsync<Repository[], ErrorState>> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/repos`, {
      credentials: 'include',
      method: 'GET',
      headers: {
        "Accept": "application/json",
        'Content-Type': 'application/json',
      },
    }).then(async (response) => {
      if (!response.ok) {
        throw {
          status: 404, detail: 'Could not fetch Repositories.'
        };
      }
      return (await response.json()) as Repository[];
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
        status: 404,
        detail: "Cannot Grab User Repos!",
        ...errorHelper,
      } as ErrorState
    }
  );
};
