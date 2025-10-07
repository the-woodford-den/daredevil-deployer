import { Field, Input, Stack } from '@chakra-ui/react';

export function NetworkForm() {
  return (
    <Stack gap="8" maxW="xl" css={{ "--field-label-width": "8rem" }}>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          IP Address
          <Field.RequiredIndicator />
        </Field.Label>
        <Input flex="1" />
        <Field.HelperText orientation="vertical">Home Network IP</Field.HelperText>
      </Field.Root>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          SSH Key
          <Field.RequiredIndicator />
        </Field.Label>
        <Input flex="1" />
        <Field.HelperText orientation="vertical">Name & Location</Field.HelperText>
      </Field.Root>
    </Stack>
  );
}
