import { create } from 'zustand';
import { getRepos } from '@/api';
import type { ErrorState, Repository, ReposState } from '@/tipos';


export const reposStore = create<ReposState>(
  (set) => ({
    repos: new Set([] as Repository[]),
    hasError: false,
    handleGetRepos: async () => {
      const results = await getRepos();
      results.match(
        (repos: Repository[]) => set({ repos: new Set(repos as Repository[]) }),
        (err: ErrorState) => set({ hasError: err.isError }),
      )
    },
  })
);



