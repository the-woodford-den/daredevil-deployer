import { useEffect, useState } from 'react';

import {
  Box,
  For,
  HStack,
  Skeleton,
  SkeletonCircle,
  Stack,
  Text
} from '@chakra-ui/react';
import { type Repository } from '@/data/repository';
import { getRepos } from '@/api/repositories'
import { Loading } from '@/components/Loading';
import './style.css';
// import data from '~/data.json';
// const repos: Repository[] = (data as Repository[]).map((x: Repository) => {
//   return x;
// });


export function Repositories() {
  const [data, setData] = useState<Repository[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<Boolean>(true);

  useEffect(() => {
    const token = import.meta.env.VITE_GITHUB_USER_TOKEN;

    async function delay() {
      await new Promise((resolve) =>
        setTimeout(resolve, 3000),
      );
    }

    if (token) {
      const fetchRepos = async () => {
        const result = await getRepos(token);
        result.match(
          (repos) => setData(repos),
          (err) => setError(err.message)
        );
        await delay();
        setLoading(false);
      };
      fetchRepos();
    }
  }, []);

  if (loading) {
    return (
      <Loading />
    );
  }

  return (
    <Stack>
      <For each={data}>
        {(item, index) => (
          <Box borderWidth=".1rem" key={index} p="4">
            <Text fontWeight="semibold">{item.fullName}</Text>
            <Text color="fg.muted">
              private: {item.private}, language: {item.language}, branch: {item.defaultBranch}
            </Text>
            <Text color="fg.muted">
              visibility: {item.visibility}, updated: {item.pushedAt}
            </Text>
            <Text color="gold">{item.description}</Text>
          </Box>
        )}
      </For>
    </Stack>
  );
}

