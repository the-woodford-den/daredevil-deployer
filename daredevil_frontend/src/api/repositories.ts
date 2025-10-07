import { ResultAsync } from 'neverthrow';
import { type Repository } from '@/models/repository';
import { type ApiError } from '@/models/error';


export const getRepos = (token: string): ResultAsync<Repository[], ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    user_token: token
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/repos?${params}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'Could not fetch Repositories.'
          };
        }
        return (await response.json()) as Repository[];
      }
      ),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};
