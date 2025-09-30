import { useState } from 'react';

import { Box, For, Stack, Text } from '@chakra-ui/react';
import { type Repository } from './types';
import data from '~/data.json';
import './style.scss';

const repos: Repository[] = (data as Repository[]).map((x: Repository) => {
  return x;
});
export function Repositories() {
  const [data] = useState(repos);

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

