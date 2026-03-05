import { Button, Container, Fieldset, Stack } from '@chakra-ui/react';


export function LogoutForm() {

  return (
    <Container centerContent={true} pt="6" pb="6">
      <Fieldset.Root size="lg" maxW="lg" color="aqua">
        <Stack>
          <Fieldset.Legend>DareDevil</Fieldset.Legend>
          <Fieldset.HelperText>ByeBye</Fieldset.HelperText>
        </Stack>
        <Button alignSelf="flex-end" type="submit">
          Logout
        </Button>
      </Fieldset.Root>
    </Container>
  );
}

