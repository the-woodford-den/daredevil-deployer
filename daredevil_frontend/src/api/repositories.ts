import { type Repository } from '@/pages/Repositories';

export const getRepos = async (token: string): Promise<Repository[]> => {
  const params = new URLSearchParams({
    user_token: token,
  });

  const response = await fetch(`${import.meta.env.BACKEND_URL}github/repos?${params.toString()}`);
  if (!response.ok) {
    throw new Error('Could not fetch Repositories.');
  }

  const data = (await response.json()) as Repository[];
  return data;
};
