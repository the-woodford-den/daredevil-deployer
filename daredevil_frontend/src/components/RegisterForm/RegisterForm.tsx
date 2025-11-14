import { Button, Container, Field, Fieldset, Input, Stack } from '@chakra-ui/react';

export function RegisterForm() {
  return (
    <Container centerContent={true} pt="3" pb="3">
      <Fieldset.Root size="lg" maxW="lg" color="aqua">
        <Stack>
          <Fieldset.Legend>User Details</Fieldset.Legend>
          <Fieldset.HelperText>Please Enter Your Info</Fieldset.HelperText>
        </Stack>

        <Fieldset.Content>
          <Field.Root required>
            <Field.Label>
              github username
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="username" />
          </Field.Root>

          <Field.Root required>
            <Field.Label>
              email
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="email" type="email" />
          </Field.Root>

          <Field.Root required>
            <Field.Label>
              daredevil password
              <Field.RequiredIndicator />
            </Field.Label>
            <Input name="password" type="password" />
          </Field.Root>
        </Fieldset.Content>
        <Button type="submit" alignSelf="flex-end">
          Register
        </Button>
      </Fieldset.Root>
    </Container>
  );
}

