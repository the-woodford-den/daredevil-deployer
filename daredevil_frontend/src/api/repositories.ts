import { type Repository } from '@/pages/Repositories';
import { ResultAsync } from 'neverthrow';

type ApiError =
  | { type: 'NETWORK_ERROR'; message: string }
  | { type: 'NOT_FOUND'; message: string }
  | { type: 'UNAUTHORIZED'; message: string }
  | { type: 'UNKNOWN_ERROR'; message: string };

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
