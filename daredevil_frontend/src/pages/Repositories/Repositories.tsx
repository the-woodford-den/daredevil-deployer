import { useEffect, useState } from 'react';

import { Box, For, Stack, Text } from '@chakra-ui/react';
import { type Repository } from '@/data/repository';
import { getRepos } from '@/api/repositories'
import './style.css';
// import data from '~/data.json';
// const repos: Repository[] = (data as Repository[]).map((x: Repository) => {
//   return x;
// });


export function Repositories() {
  useEffect(() => {
    async function reposGrab() {
      const token = import.meta.env.VITE_GITHUB_USER_TOKEN;
      if (token) {
        const repos = await getRepos(token);
        setData(repos);
      }
    }
    reposGrab();

  }, [])

  const [data, setData] = useState<Repository[]>();

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

