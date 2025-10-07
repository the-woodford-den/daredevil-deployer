import { Button, Field, Input, Stack } from '@chakra-ui/react';

export function LoginForm() {
  return (
    <Stack gap="8" className="login-form">
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Client ID
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="clientId" />
      </Field.Root>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Email
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="email" type="email" />
      </Field.Root>
      <Button type="submit" alignSelf="flex-end">
        Submit
      </Button>
    </Stack>
  );
}
