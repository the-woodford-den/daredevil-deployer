import { Button, Field, Input, Stack } from '@chakra-ui/react';

export function NetworkForm() {
  return (
    <Stack gap="8" className="network-form">
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          IP Address
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="ipAddress" />
      </Field.Root>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          SSH Key
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="sshKey" />
      </Field.Root>
      <Button type="submit" alignSelf="flex-end">
        Submit
      </Button>
    </Stack>
  );
}
