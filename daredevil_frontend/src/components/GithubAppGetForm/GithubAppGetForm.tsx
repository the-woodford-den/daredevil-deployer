import { useFormStatus } from 'react-dom';
import { Button, Field, Heading, Input, Stack } from '@chakra-ui/react';

export function GithubAppGetForm() {
  const { pending } = useFormStatus();

  return (
    <Stack gap="8" className="github-app-form">
      <Heading size="lg" className="t-font">
        Github App Installation
      </Heading>
      <Field.Root orientation="horizontal">
        <Field.Label>
          App Slug
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="appSlug" type="text" disabled={pending} />
      </Field.Root>
      <Button type="submit" disabled={pending}>
        {pending ? "Submitting ..." : "Submit"}
      </Button>
    </Stack>
  );
}
