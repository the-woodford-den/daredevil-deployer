import { Container, Flex, Grid, GridItem, Text } from '@chakra-ui/react';
import { LoginForm } from '@/components/LoginForm';
import { signIn } from '@/api';
import type { User, ErrorState } from '@/tipos';
import { errorStore, userStore } from '@/state';
import { Form, redirect } from 'react-router';



export default function Login() {
  const storeSignIn = userStore(
    (state) => state.handleSignIn,
  );

  const setError = errorStore((state) => state.setError);

  const handleSignIn = async (formData: FormData) => {
    const username = formData.get("username") as string;
    const password = formData.get("password") as string;
    const result = await signIn(username, password);
    result.match(
      (user: User) => {
        storeSignIn(user);
        const response = redirect('/cloud');
        if (user["cookie"]) {
          response.headers.set('Set-Cookie', user["cookie"]);
        }
        return response;

      },
      (err: ErrorState) => {
        setError(err);
        return redirect('/login');
      }
    );
    console.log(result);
  };


  return (
    <Container>
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap="6"
      >
        <GridItem colSpan={3} pt="3">
          <Text textStyle="4xl" className="t-font">
            Welcome, Welcome, Welcome
          </Text>
        </GridItem>
        <GridItem colSpan={3} textStyle="4xl" pt="3">
          <Flex direction="horizontal">
            <Form method="post" action={async (form: FormData) => { await handleSignIn(form) }}>
              <LoginForm />
            </Form>
          </Flex>
        </GridItem>
      </Grid>
    </Container>
  );
};

