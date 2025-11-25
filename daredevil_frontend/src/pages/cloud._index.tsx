import { useLoaderData } from "react-router";
import {
  Container,
  Text,
  VStack
} from '@chakra-ui/react';
import { CloudTree } from "@/components/CloudTree/CloudTree";

export async function clientLoader() {
  return {
    title: 'Just Keep Showing Up & Life Will Reward You',
  };
}

export default function Cloud() {
  let data = useLoaderData();

  return (
    <Container width="50%">
      <VStack>
        <CloudTree />
        <Text>{data.title}</Text>
      </VStack>
    </Container>
  );
}

