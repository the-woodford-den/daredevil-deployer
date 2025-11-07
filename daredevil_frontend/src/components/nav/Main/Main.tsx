import { type ReactNode, useRef } from 'react';
import { Flex, Grid, GridItem, Heading, Image, Text } from '@chakra-ui/react';
import { Alarm, LoginForm } from '@/components';
import { errorStore } from '@/state/errorStore';
import { userStore } from '@/state/userStore';
import rubyUrl from '~/ruby.svg';


const ref = useRef<HTMLFormElement>(null);


export function Main({
  children,
}: {
  children: ReactNode;
}) {
  // const loading = userStore(
  //   (state) => state.loading,
  // );
  const username = userStore(
    (state) => state.username,
  );
  const hasError = userStore(
    (state) => state.hasError
  );
  const signIn = userStore(
    (state) => state.handleSignIn,
  );
  // const signOut = userStore(
  //   (state) => state.handleSignOut,
  // );
  const error = errorStore(
    (state) => state
  );

  const handleSignIn = async (
    data: FormData,
  ) => {

    const name = data.get("username") as string;
    const pword = data.get("password") as string;

    const result = await signIn(pword, name);

    console.log(result);
    ref.current?.reset();
  };

  return (
    <main>
      <Flex justify="center" p="3">
        {hasError ? (
          <Alarm
            status="error"
            title={`${error.status} Error Status`}
            width="60%"
          >{error.detail}</Alarm>
        ) : (
          <Heading size="2xl" className="t-font">
            Welcome Welcome Welcome ::: {username ?
              username.toUpperCase() : "Please Sign In"}
          </Heading>
        )}
      </Flex>
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap="6"
      >
        <GridItem colSpan={3} pt="3">
          <Flex direction="column" fontWeight="600">
            <Flex align="center" gap="4" justify="center">
              <Image
                src={rubyUrl}
                alt="Ruby"
                boxSize="6rem"
                fit="contain"
                className="rubyLogo"
              />
              <Text textStyle="lg" className="t-font">Daredevil Deployer</Text>
            </Flex>
            <Flex align="center" gap="2" justify="center">
              <Text textStyle="md" className="t-font">Cloud Engineering</Text>
            </Flex>
          </Flex>
        </GridItem>
      </Grid>
      {username ?
        children : (
          <Flex direction="row">
            <form ref={ref} action={async (formData) => (await handleSignIn(formData))}>
              <LoginForm />
            </form>
          </Flex>
        )
      }
    </main>
  );
};
