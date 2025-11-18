import { Fragment } from 'react';
import { useLoaderData } from "react-router";
import {
  Container,
  HStack,
  Flex,
  GridItem,
  VStack,
  Highlight,
  Heading,
  Mark,
  useHighlight,
  StackSeparator
} from '@chakra-ui/react';
import underUrl from '~/underline.svg';

export async function clientLoader() {
  return {
    title: 'Welcome Welcome Welcome!',
  };
}

export default function Lobby() {
  let data = useLoaderData();

  const chunks = useHighlight({
    text: ":: Authenticating Connections ::",
    query: ["Authenticating", "Connections"],
  })


  return (
    <GridItem colSpan={3}>
      <Container width="85%">
        <Flex justify="center">
          <VStack gap="8" separator={<StackSeparator borderColor="seagreen" height=".25rem" />}>
            <Heading size="5xl">
              DareDevil Deployer
            </Heading>
            <Heading size="2xl" letterSpacing="wider">
              <Highlight query="Welcome!" styles={{ color: "teal.600", }}>
                {data.title}
              </Highlight>
            </Heading>
            <Heading size="2xl" maxW="32">
              <HStack justify="center">

                {chunks.map((chunk, index) => {
                  return chunk.match ? (
                    <Mark
                      key={index}
                      css={{
                        fontStyle: 'italic',
                        color: "purple.500",
                        position: "relative",
                      }}
                    >
                      {chunk.text}
                      <img
                        style={{ position: "absolute", left: 0 }}
                        src={underUrl}
                        loading="lazy"
                        alt="line"
                      />
                    </Mark>
                  ) : (
                    <Fragment key={index}>{chunk.text}</Fragment>
                  )
                })}
              </HStack>
            </Heading>
          </VStack>
        </Flex>
      </Container>
    </GridItem>
  )
}
