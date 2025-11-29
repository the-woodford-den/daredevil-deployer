import { useRef, type FormEvent } from 'react';
import {
  Container,
  Flex,
  GridItem,
  HStack,
  Image,
  Stack,
  StackSeparator,
  Text
} from '@chakra-ui/react';
import { LoginForm } from '@/components';
import { signIn } from '@/api';
import type { User, ErrorState } from '@/tipos';
import { errorStore, userStore } from '@/state';
import { Form, useNavigate } from 'react-router';
import mmUrl from '~/mm1.svg';



export default function Login() {
  const storeSignIn = userStore(
    (state) => state.handleSignIn,
  );
  const formRef = useRef<HTMLFormElement>(null);
  const setError = errorStore((state) => state.setError);
  const navigate = useNavigate();

  const handleSignIn = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formRef.current) {
      return;
    }

    const data = new FormData(formRef.current);
    const username = data.get("username") as string;
    const password = data.get("password") as string;
    const result = await signIn(username, password);
    result.match(
      (user: User) => {
        storeSignIn(user);
        console.log(result);
        navigate("/cloud");
      },
      (err: ErrorState) => {
        setError(err);
      }
    );
  };


  return (
    <GridItem colSpan={3} >
      <Container width="85%">
        <Stack separator={<StackSeparator borderColor="seagreen" height=".50rem" />} >
          <Flex gap="8" justify="center">
            <HStack pb="6">
              <Text textStyle="4xl" fontWeight="bold" color="aqua">
                DareDevil Deployer Login
              </Text>
              <Image
                src={mmUrl}
                alt="MM"
                boxSize="6rem"
                fit="contain"
                className="mmLogo"
              />
            </HStack>
          </Flex>
          <Form method="post" ref={formRef} onSubmit={async (e) => { await handleSignIn(e) }}>
            <LoginForm />
          </Form>
        </Stack>
      </Container>
    </GridItem>
  );
};

