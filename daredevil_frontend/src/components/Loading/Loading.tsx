import {
  HStack,
  Skeleton,
  SkeletonCircle,
  Stack
} from '@chakra-ui/react';

export function Loading() {
  return (
    <HStack mb="5">
      <SkeletonCircle
        size="12"
        css={{
          "--start-color": "colors.teal.500",
          "--end-color": "colors.green.500",
        }}
        variant="shine"
      />
      <Stack flex="1">
        <Skeleton
          height="5"
          css={{
            "--start-color": "colors.teal.500",
            "--end-color": "colors.green.500",
          }}
          variant="shine"
        />
        <Skeleton
          height="5"
          css={{
            "--start-color": "colors.teal.500",
            "--end-color": "colors.green.500",
          }}
          variant="shine"
        />
        <Skeleton
          height="5"
          css={{
            "--start-color": "colors.teal.500",
            "--end-color": "colors.green.500",
          }}
          variant="shine"
          width="80%"
        />
        <Skeleton
          height="5"
          css={{
            "--start-color": "colors.teal.500",
            "--end-color": "colors.green.500",
          }}
          variant="shine"
          width="60%"
        />
      </Stack>
    </HStack>
  );
}

