import { Container, Flex, Separator, Stack, Text } from '@chakra-ui/react';
import { useLoaderData } from "react-router";

export async function clientLoader() {
  return {
    title: 'Console',
  };
}

export default function Console() {
  let data = useLoaderData();

  return (
    <Container width="75%">
      <Text pb="3" textStyle="4xl">{data.title}</Text>
      <Flex pt="3" align="center" justify="space-between" className="t-font">
        <Stack>
          <Text textStyle="2xl">First</Text>
          <Separator />
          <Text textStyle="2xl">Second</Text>
          <Separator />
          <Text textStyle="2xl">Third</Text>
        </Stack>
      </Flex>
    </Container>
  );
}


