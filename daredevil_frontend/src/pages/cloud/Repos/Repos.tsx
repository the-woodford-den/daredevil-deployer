import { reposStore } from '@/state';
import { Alarm, Loading } from '@/components';
import type { Repository } from '@/tipos';
import {
  Box,
  Flex,
  Heading,
  For,
  Stack,
  Text
} from '@chakra-ui/react';
import './style.css';

export function Repos() {

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
      <Flex justify="center" pb="4">
        {error ? (
          <Alarm
            status="error"
            title={error.type}
            width="60%"
          >{error.message}</Alarm>
        ) : (
          <Heading size="5xl" className="t-font">
            Repositories
          </Heading>
        )}
      </Flex>
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

