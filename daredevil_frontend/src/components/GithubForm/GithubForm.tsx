import { Button, Field, Heading, Input, Stack } from '@chakra-ui/react';

type Params = {
  isDisabled: boolean;
}

export function GithubForm({
  isDisabled
}: Params) {
  return (
    <Stack gap="8" className="login-form">
      <Heading size="lg" className="t-font">
        Github Login
      </Heading>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Client ID
          <Field.RequiredIndicator />
        </Field.Label>
        <Input disabled={isDisabled} name="clientId" />
      </Field.Root>
      <Field.Root orientation="horizontal" required>
        <Field.Label>
          Email
          <Field.RequiredIndicator />
        </Field.Label>
        <Input disabled={isDisabled} name="email" type="email" />
      </Field.Root>
      <Button disabled={isDisabled} type="submit" alignSelf="flex-end">
        Submit
      </Button>
    </Stack>
  );
}
