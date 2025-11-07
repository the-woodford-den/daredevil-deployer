import { type ReactNode, useRef } from 'react';
import { Flex, Grid, GridItem, Heading, Image, Text } from '@chakra-ui/react';
import { Alarm, LoginForm } from '@/components';
import { errorStore } from '@/state/errorStore';
import { userStore } from '@/state/userStore';


const ref = useRef<HTMLFormElement>(null);


export function Main() {
  // const loading = userStore(
  //   (state) => state.loading,
  // );
  // const username = userStore(
  //   (state) => state.username,
  // );
  const hasError = userStore(
    (state) => state.hasError
  );
  // const signIn = userStore(
  //   (state) => state.handleSignIn,
  // );
  // const signOut = userStore(
  //   (state) => state.handleSignOut,
  // );
  const error = errorStore(
    (state) => state
  );


  return (
    <Flex justify="center" p="3">
      {hasError ? (
        <Alarm
          status="error"
          title={`${error.status} Error Status`}
          width="60%"
        >{error.detail}</Alarm>
      ) : (
        <></>
      )}
    </Flex>
  );
};

