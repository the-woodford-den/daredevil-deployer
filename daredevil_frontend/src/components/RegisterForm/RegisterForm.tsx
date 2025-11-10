import { Button, Container, Field, HStack, Input, VStack } from '@chakra-ui/react';

export function RegisterForm() {
  return (
    <Container color="black" fontStyle="italic" fontFamily="cursive" bgColor="skyblue" alignItems="flexGrow: '100'">
      <HStack maxWidth="100%">
        <VStack maxHeight="100%">
          <Field.Root orientation="horizontal" required>
            <Field.Label>
              github username
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="username" />
          </Field.Root>
          <Field.Root orientation="horizontal" required>
            <Field.Label>
              email
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="email" type="email" />
          </Field.Root>
          <Field.Root orientation="horizontal" required>
            <Field.Label>
              daredevil password
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="password" type="password" />
          </Field.Root>
          <Button type="submit" alignSelf="flex-end">
            Register
          </Button>
        </VStack>
      </HStack>
    </Container>
  );
}

