import { Fragment } from 'react';
import { useLoaderData } from "react-router";
import {
  Container,
  Flex,
  GridItem,
  Heading,
  Highlight,
  HStack,
  Mark,
  useHighlight,
  StackSeparator,
  VStack,
} from '@chakra-ui/react';
import underUrl from '~/underline.svg';

export async function clientLoader() {
  return {
    title: 'DareDevil Deployer',
    welcome: "Welcome Welcome Welcome"
  };
}

export default function Lobby() {
  let data = useLoaderData();

  const chunks = useHighlight({
    text: ":: Authenticating Connections ::",
    query: ["Authenticating", "Connections"],
  })

  return (
    <GridItem colSpan={3} pb="3">
      <Container width="85%">
        <Flex justify="center">
          <VStack gap="8" separator={<StackSeparator borderColor="aqua" height=".25rem" />}>
            <Heading size="6xl" color="aqua">
              {data.title}
            </Heading>
            <Heading size="4xl" color="aqua" letterSpacing="wider">
              <Highlight query=" Welcome " styles={{ color: "purple.500", }}>
                {data.welcome}
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

