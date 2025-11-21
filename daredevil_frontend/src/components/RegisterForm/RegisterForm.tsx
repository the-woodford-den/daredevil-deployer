import { Button, Container, Field, Fieldset, Input, Stack } from '@chakra-ui/react';

export function RegisterForm() {
  return (
    <Container centerContent={true} pt="6" pb="6">
      <Fieldset.Root size="lg" maxW="lg" color="aqua">
        <Stack>
          <Fieldset.Legend color="aqua">User Details</Fieldset.Legend>
          <Fieldset.HelperText color="aqua">Please Enter Your Info</Fieldset.HelperText>
        </Stack>

        <Fieldset.Content>
          <Field.Root required>
            <Field.Label>
              github username
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="username" borderColor="aqua" />
          </Field.Root>

          <Field.Root required>
            <Field.Label>
              email
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="email" type="email" borderColor="aqua" />
          </Field.Root>

          <Field.Root required>
            <Field.Label>
              daredevil password
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="password" type="password" borderColor="aqua" />
          </Field.Root>
        </Fieldset.Content>
        <Button type="submit" alignSelf="flex-end">
          Register
        </Button>
      </Fieldset.Root>
    </Container>
  );
}

