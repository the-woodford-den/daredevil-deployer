import { Flex, Separator } from '@chakra-ui/react';
import { Alarm } from '@/components/Alarm';
import { errorStore } from '@/state/errorStore';
import { userStore } from '@/state/userStore';


export function Main({ children }: { children?: React.ReactNode }) {
  const hasError = userStore(
    (state) => state.hasError
  );

  const errorStatus = errorStore((state) => state.status);
  const errorDetail = errorStore((state) => state.detail);

  return (
    <Flex justify="center" p="3">
      {hasError ? (
        <Alarm
          status="error"
          title={`${errorStatus} Error Status`}
          width="60%"
        >{errorDetail}</Alarm>
      ) : (<></>)
      }
      <Separator />
      <Separator margin={18} />
      {children}
    </Flex>
  );
};

