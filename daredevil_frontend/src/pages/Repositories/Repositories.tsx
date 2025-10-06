import { useEffect, useState } from 'react';
import {
  Box,
  Flex,
  For,
  Stack,
  Text
} from '@chakra-ui/react';
import { getRepos, type ApiError } from '@/api/repositories'
import { type Repository } from '@/data/repository';
import { Alarm } from '@/components/Alarm';
import { Loading } from '@/components/Loading';
import './style.css';


export function Repositories() {
  const [data, setData] = useState<Repository[]>([]);
  const [error, setError] = useState<ApiError | null>(null);
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
          (err) => setError(err)
        );
        await delay();
        setLoading(false);
      };
      fetchRepos();
    }
  }, []);

  if (loading) {
    return (
      <>
        <Flex justify="center" pb="4">
          <Alarm
            status="info"
            title="In progress..."
            width="60%"
          >Loading Repositories</Alarm>
        </Flex>
        <Loading />
      </>
    );
  }

  return (
    <>
      {error && (
        <Alarm
          status="error"
          title={error.type}
          width="60%"
        >{error.message}</Alarm>
      )}
      <Stack>
        <For each={data}>
          {(item, index) => (
            <Box borderWidth=".1rem" key={index} p="4">
              <Text fontWeight="semibold">{item.full_name}</Text>
              <Text color="fg.muted">
                language: {item.language}, default branch: {item.default_branch}
              </Text>
              <Text color="fg.muted">
                visibility: {item.visibility}, updated: {item.pushed_at}
              </Text>
              <Text color="gold">{item.description}</Text>
            </Box>
          )}
        </For>
      </Stack>
    </>
  );
}

