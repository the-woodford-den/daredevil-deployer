import { Image, Grid, GridItem, Text } from '@chakra-ui/react';
import { createUser } from '@/api';
import { RegisterForm } from '@/components';
import { errorStore, userStore } from '@/state';
import rubyUrl from '~/ruby.svg';
import { Form, redirect } from 'react-router';
import type { User, ErrorState } from '@/tipos';


export default function Register() {

  const createUserState = userStore((state) => state.createUser);

  const setError = errorStore((state) => state.setError);

  const handleCreateUser = async (data: FormData) => {
    const username = data.get("username") as string;
    const email = data.get("email") as string;
    const password = data.get("password") as string;

    const result = await createUser(email, password, username);
    result.match(
      (user: User) => createUserState(user),
      (err: ErrorState) => setError(err)
    );
    console.log(result);
    return redirect('/login');
  };

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
        <Form method="post" action={async (form: FormData) => { await handleCreateUser(form) }}>
          <RegisterForm />
        </Form>
      </GridItem>
    </Grid >
  );
};

