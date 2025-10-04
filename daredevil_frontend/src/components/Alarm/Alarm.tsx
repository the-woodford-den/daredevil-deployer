import type { PropsWithChildren } from 'react';
import { Alert, Stack } from '@chakra-ui/react';

type Params = {
  status: "info" | "warning" | "success" | "error" | "neutral";
  title: string;
  width: string;
} & PropsWithChildren


export function Alarm({
  children,
  status,
  title,
  width,
}: Params) {
  return (
    <Stack width={width}>
      <Alert.Root status={status}>
        <Alert.Indicator />
        <Alert.Content>
          <Alert.Title>{title}</Alert.Title>
          <Alert.Description>
            {children}
          </Alert.Description>
        </Alert.Content>
      </Alert.Root>
    </Stack>
  );
}
