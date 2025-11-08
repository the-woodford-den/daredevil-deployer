import { useRef } from 'react';
import { useNavigate } from 'react-router';
import { Container, Flex, Grid, GridItem, Image, Text } from '@chakra-ui/react';
import { LoginForm } from '@/components';
import { userStore } from '@/state';
import rubyUrl from '~/ruby.svg';

export function Login() {
  const ref = useRef<HTMLFormElement>(null);

  const username = userStore(
    (state) => state.username,
  );

  const signIn = userStore(
    (state) => state.handleSignIn,
  );

  const handleSignIn = async (
    data: FormData,
  ) => {

    const navigate = useNavigate()
    const name = data.get("username") as string;

    const pword = data.get("password") as string;
    const result = await signIn(pword, name);

    ref.current?.reset();
    navigate('/cloud');
  };

  return (
    <Container>
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap="6"
      >
        <GridItem colSpan={3} pt="3">
          <Text textStyle="lg" className="t-font">
            Welcome, Welcome, Welcome
          </Text>
        </GridItem>
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
              <Text textStyle="xl" className="t-font">Daredevil Deployer</Text>
            </Flex>
            <Flex align="center" gap="2" justify="center">
              <Text textStyle="md" className="t-font">Cloud Engineering</Text>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem colSpan={3} pt="3">
          <Flex direction="row">
            <form ref={ref} action={async (formData) => (await handleSignIn(formData))}>
              <LoginForm />
            </form>
          </Flex>
        </GridItem>
      </Grid>
    </Container>
  );
};

