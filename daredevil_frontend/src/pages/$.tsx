import { GridItem, Text, VStack } from '@chakra-ui/react';

export async function loader() {
  return ({}, 404);
}

export default function Catch() {

  return (
    <GridItem alignSelf="auto" justifySelf="center" colSpan={3}>
      <VStack>
        <Text textStyle="4xl">Route Not Found!</Text>
        <Text textStyle="2xl">Try Again!</Text>
      </VStack>
    </GridItem>
  );
}

