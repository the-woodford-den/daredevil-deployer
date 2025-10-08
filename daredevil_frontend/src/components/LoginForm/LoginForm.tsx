import { Button, Field, Heading, Input, Stack } from '@chakra-ui/react';
import { useFormStatus } from 'react-dom';


export function LoginForm() {
  const { pending } = useFormStatus();

  return (
    <Stack gap="8" className="login-form">
      <Heading size="lg" className="t-font">
        User Login
      </Heading>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Email
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="email" type="email" />
      </Field.Root>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Password
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="password" type="password" />
      </Field.Root>
      <Button disabled={pending} type="button" alignSelf="flex-end">
        {pending ? "Submitting ..." : "Submit"}
      </Button>
    </Stack>
  );
}
