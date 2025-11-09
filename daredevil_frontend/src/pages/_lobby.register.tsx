import { Image, Grid, GridItem, Text } from '@chakra-ui/react';
import { RegisterForm } from '@/components';
import { userStore } from '@/state';
import rubyUrl from '~/ruby.svg';
import { Form, redirect } from 'react-router';
import type { Route } from './+types/_lobby.register';

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const username = formData.get("username") as string;
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  const createUser = userStore.getState().createUser;
  await createUser(password, email, username);

  return redirect('/cloud');
}

export default function Register() {
  return (
    <Grid
      templateColumns="repeat(4,1fr)"
      width="100%"
      gap="10"
      mt="6"
    >
      <GridItem alignItems="end" colSpan={4}>
        <Image
          src={rubyUrl}
          alt="Ruby"
          boxSize="6rem"
          fit="contain"
          className="rubyLogo"
        />
      </GridItem>
      <GridItem
        alignItems="left"
        colSpan={4}
      >
        <Text>
          The Woodford Den: Daredevil Deployer Registration
        </Text>
      </GridItem>
      <GridItem
        alignItems="center"
        colSpan={4}
      >
        <Form method="post">
          <RegisterForm />
        </Form>
      </GridItem>
    </Grid >
  );
};

