import { Button, Field, Input, Stack } from '@chakra-ui/react';

export function RegisterForm() {
  return (
    <Stack gap="8">
      <Field.Root orientation="vertical" required>
        <Field.Label>
          github username
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="username" />
        <Field.HelperText />
        <Field.ErrorText />
      </Field.Root>
      <Field.Root orientation="vertical" required>
        <Field.Label>
          daredevil password
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="password" />
        <Field.HelperText />
        <Field.ErrorText />
      </Field.Root>
      <Button type="submit" alignSelf="flex-end">
        Register
      </Button>
    </Stack>
  );
};

