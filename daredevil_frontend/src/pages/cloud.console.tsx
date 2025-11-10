import { Container, Flex, Separator, Stack, Text } from '@chakra-ui/react';

export default function Console() {


  return (
    <Container direction="column">
      <Flex align="center" justify="space-between" className="t-font">
        <Stack>
          <Text>First</Text>
          <Separator />
          <Text>Second</Text>
          <Separator />
          <Text>Third</Text>
        </Stack>
      </Flex>
    </Container>
  );
}


