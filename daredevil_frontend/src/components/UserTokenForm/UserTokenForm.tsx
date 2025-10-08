import { useFormStatus } from 'react-dom';
import { Button, Field, Heading, Input, Stack } from '@chakra-ui/react';

export function UserTokenForm() {
  const { pending } = useFormStatus();

  return (
    <Stack gap="8" className="login-form">
      <Heading size="lg" className="t-font">
        Github Login
      </Heading>
      <Field.Root orientation="horizontal">
        <Field.Label>
          Client ID
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="clientId" type="text" disabled={pending} />
      </Field.Root>
      <Button type="submit" disabled={pending}>
        {pending ? "Submitting ..." : "Submit"}
      </Button>
    </Stack>
  );
}
