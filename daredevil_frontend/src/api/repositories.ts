import { type Repository } from '@/pages/Repositories';

export const getRepos = async (token: string): Promise<Repository[]> => {
  const options = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  };

  const params = new URLSearchParams({
    user_token: token
  });

  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const response = await fetch(
    `${backendUrl}/github/repos?${params}`
  );
  if (!response.ok) {
    throw new Error('Could not fetch Repositories.');
  }

  const data = (await response.json()) as Repository[];
  return data;
};
