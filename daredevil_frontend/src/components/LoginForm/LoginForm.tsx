import { Button, GridItem, Field, Heading, Input } from '@chakra-ui/react';
import { userStore } from '@/state/userStore';
import type { FormEvent } from 'react';


export function LoginForm() {

  return (
    <GridItem colSpan={3} textStyle="5xl" className="t-font">
      <Heading textStyle="4xl" className="t-font">
        Daredevil Login
      </Heading>
      <Field.Root orientation="horizontal" required>
        <Field.Label textStyle="2xl" textEmphasisStyle="sesame" className="t-font">
          username
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="username" type="username" />
      </Field.Root>
      <Field.Root orientation="horizontal" required>
        <Field.Label textStyle="2xl" textEmphasisStyle="sesame" className="t-font">
          Password
          <Field.RequiredIndicator />
        </Field.Label>
        <Input name="password" type="password" />
      </Field.Root>
      <Button alignSelf="stretch" type="submit">
        <Heading textStyle="4xl" className="t-font">Submit</Heading>
      </Button>
    </GridItem >
  );
}
