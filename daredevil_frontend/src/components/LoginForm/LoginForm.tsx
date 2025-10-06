import { Field, Input, Stack } from '@chakra-ui/react';

export function LoginForm() {
  return (
    <Stack gap="8" maxW="md" css={{ "--field-label-width": "6rem" }}>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Client_ID
          <Field.RequiredIndicator />
        </Field.Label>
        <Input flex="1" />
        <Field.HelperText>Github App Client ID</Field.HelperText>
      </Field.Root>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Email
          <Field.RequiredIndicator />
        </Field.Label>
        <Input flex="1" />
        <Field.HelperText>Github User Email</Field.HelperText>
      </Field.Root>
    </Stack>
  );
}
