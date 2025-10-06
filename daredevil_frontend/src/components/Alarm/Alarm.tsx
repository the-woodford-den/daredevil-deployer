import type { PropsWithChildren } from 'react';
import { Alert, Spinner, Stack } from '@chakra-ui/react';
import { LuAlarmSmoke } from 'react-icons/lu';

type Params = {
  status: "info" | "warning" | "success" | "error" | "neutral";
  title: string;
  width: string;
} & PropsWithChildren

const indicators = {
  error: <LuAlarmSmoke />,
  info: <Spinner size="sm" />
}

export function Alarm({
  children,
  status,
  title,
  width,
}: Params) {
  return (
    <Stack width={width}>
      <Alert.Root status={status}>
        <Alert.Indicator>
          {indicators[status as keyof typeof indicators]}
        </Alert.Indicator>
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
