import { useFormStatus } from 'react-dom';
import { Button, Field, Heading, Input, Stack } from '@chakra-ui/react';

export function FindInstallForm() {
  const { pending } = useFormStatus();

  return (
    <Stack gap="8" className="app-get-form">
      <Heading size="lg" className="t-font">
        Find Installation Record
      </Heading>
      <Field.Root required orientation="horizontal">
        <Field.Label>
          Username
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="username" type="text" disabled={pending} />
      </Field.Root>
      <Button type="submit" disabled={pending}>
        {pending ? "Submitting ..." : "Submit"}
      </Button>
    </Stack>
  );
}

