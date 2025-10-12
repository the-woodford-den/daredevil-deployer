import { useFormStatus } from 'react-dom';
import { Button, Field, Heading, Input, Stack } from '@chakra-ui/react';

export function AppItemForm() {
  const { pending } = useFormStatus();

  return (
    <Stack gap="8" className="app-get-form">
      <Heading size="lg" className="t-font">
        Get Github App Form
      </Heading>
      <Field.Root required orientation="horizontal">
        <Field.Label>
          Slug
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="slug" type="text" disabled={pending} />
      </Field.Root>
      <Button type="submit" disabled={pending}>
        {pending ? "Submitting ..." : "Submit"}
      </Button>
    </Stack>
  );
}

