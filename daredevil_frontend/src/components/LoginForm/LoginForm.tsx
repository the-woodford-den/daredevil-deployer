import { Button, Container, Fieldset, Field, Input, Stack } from '@chakra-ui/react';


export function LoginForm() {

  return (
    <Container centerContent={true} pt="6" pb="6">
      <Fieldset.Root size="lg" maxW="lg" color="aqua">
        <Stack>
          <Fieldset.Legend>Daredevil User</Fieldset.Legend>
          <Fieldset.HelperText>Enter Login Details</Fieldset.HelperText>
        </Stack>

        <Fieldset.Content>
          <Field.Root required>
            <Field.Label>
              username
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="username" type="username" borderColor="aqua" />
          </Field.Root>
          <Field.Root required>
            <Field.Label>
              Password
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="password" type="password" borderColor="aqua" />
          </Field.Root>
        </Fieldset.Content>
        <Button alignSelf="flex-end" type="submit">
          Login
        </Button>
      </Fieldset.Root>
    </Container>
  );
}
