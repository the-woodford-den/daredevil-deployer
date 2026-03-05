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
import { LogoutButton } from '@/components';
import { handleSignOut } from '@/api';
import type { User, ErrorState } from '@/tipos';
import { errorStore, userStore } from '@/state';
import { Form, useNavigate } from 'react-router';
import ddUrl from '@/assets/ddevil-pixel.png';


export default function Logout() {
  const storeSignOut = userStore(
    (state) => state.handleSignOut,
  );
  const formRef = useRef<HTMLFormElement>(null);
  const setError = errorStore((state) => state.setError);
  const navigate = useNavigate();

  const handleSignOut = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formRef.current) {
      return;
    }

    const result = await signOut(username, password);
    result.match(
      (user: User) => {
        storeSignOut(user);
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
                Leaving? Come back soon!
              </Text>
              <Image
                src={ddUrl}
                alt="MM"
                boxSize="6rem"
                fit="contain"
                className="ddLogo"
              />
            </HStack>
          </Flex>
          <Form method="delete" ref={formRef} onSubmit={async (e) => { await handleSignOut(e) }} viewTransition="true">
            <LogoutForm />
          </Form>
        </Stack>
      </Container>
    </GridItem>
  );
};
