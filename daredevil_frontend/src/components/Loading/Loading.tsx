import {
  HStack,
  Skeleton,
  Stack
} from '@chakra-ui/react';

export function Loading() {
  return (
    <HStack mb="5">
      <Stack flex="1">
        <Skeleton
          height="5"
          variant="shine"
        />
        <Skeleton
          height="5"
          variant="shine"
        />
        <Skeleton
          height="5"
          variant="shine"
          width="80%"
        />
        <Skeleton
          height="5"
          variant="shine"
          width="80%"
        />
        <Skeleton
          height="5"
          variant="shine"
          width="60%"
        />
        <Skeleton
          height="5"
          variant="shine"
          width="60%"
        />
      </Stack>
    </HStack>
  );
}

