import {
  GridItem,
  HStack,
  Image,
  StackSeparator,
  Text,
  Stack,
  Flex
} from '@chakra-ui/react';
import { type FormEvent, useRef } from 'react';
import { createUser } from '@/api';
import { RegisterForm } from '@/components';
import { errorStore, userStore } from '@/state';
import rubyUrl from '~/ruby.svg';
import { Form, redirect } from 'react-router';
import type { User, ErrorState } from '@/tipos';


export default function Register() {

  const createUserState = userStore((state) => state.createUser);
  const formRef = useRef<HTMLFormElement>(null);
  const setError = errorStore((state) => state.setError);

  const handleCreateUser = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!formRef.current) {
      return;
    }

    const data = new FormData(formRef.current)
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
    <GridItem colSpan={3} pt="6" pb="6">
      <Stack separator={<StackSeparator />}>
        <Flex gap="8" justify="center">
          <HStack pb="6">
            <Image
              src={rubyUrl}
              alt="Ruby"
              boxSize="5rem"
              fit="contain"
              className="rubyLogo"
            />
            <Text textStyle="4xl" fontWeight="bold" color="aqua">
              Daredevil Deployer Registration
            </Text>
          </HStack>
        </Flex>
        <Form method="post" ref={formRef} action="/login" onSubmit={async (e) => { await handleCreateUser(e) }}>
          <RegisterForm />
        </Form>
      </Stack>
    </GridItem>
  );
};

