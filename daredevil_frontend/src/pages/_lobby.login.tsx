import { Container, Flex, Grid, GridItem, Text } from '@chakra-ui/react';
import { LoginForm } from '@/components/LoginForm';
import { userStore } from '@/state';
import { Form, redirect } from 'react-router';
import type { Route } from './+types/_lobby.login';

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const username = formData.get("username") as string;
  const password = formData.get("password") as string;

  const signIn = userStore.getState().handleSignIn;
  const result = await signIn(password, username);

  // Check if sign-in was successful and forward the cookie
  const redirectResponse = await result.match(
    (data) => {
      // Create a redirect response with the Set-Cookie header from backend
      const response = redirect('/cloud');
      if (data.setCookieHeader) {
        response.headers.set('Set-Cookie', data.setCookieHeader);
      }
      return response;
    },
    () => null
  );

  if (redirectResponse) {
    return redirectResponse;
  }

  // If sign-in failed, stay on login page
  // TODO: Show error message to user
  return null;
}

export default function Login() {
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
            <Form method="post">
              <LoginForm />
            </Form>
          </Flex>
        </GridItem>
      </Grid>
    </Container>
  );
};

