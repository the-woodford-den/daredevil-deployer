import { Fragment } from 'react';
import { useLoaderData } from "react-router";
import {
  Center,
  Grid,
  GridItem,
  Highlight,
  Heading,
  Mark,
  useHighlight
} from '@chakra-ui/react';
import underUrl from '~/underline.svg';

export async function clientLoader() {
  return {
    title: 'Just Keep Showing Up & Life Will Reward You',
  };
}

export default function About() {
  let data = useLoaderData();

  const chunks = useHighlight({
    text: " Secure Responsive Environments :: High Performance CI/CD ::" +
      " Persistent Data Intense Applications :: AI/ML Pipelines ::" +
      " Cloud Native Cloud Formation :: Kubernetes & Podman ::",
    query: [
      " Secure Responsive Environments ::",
      " High Performance CI/CD ::",
      " Persistent Data Intense Applications ::",
      " AI/ML Pipelines ::",
      " Cloud Native Cloud Formation ::",
      " Kubernetes & Podman ::"
    ],
  })


  return (
    <GridItem colSpan={3}>
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap="12"
        pt="2"
        pb="6"
      >
        <GridItem colSpan={3}>
          <Center>
            <Heading color="aqua" size="4xl" letterSpacing="wider" className="t-font">
              <Highlight query="& Life Will Reward You" styles={{ color: "purple.600", }}>
                {data.title}
              </Highlight>
            </Heading>
          </Center>
        </GridItem>
        {chunks.map((chunk, index) => {
          return chunk.match ? (
            <GridItem alignSelf="end">
              <Heading size="xl" maxW="32" className="t-font">
                <Mark
                  key={index}
                  css={{
                    fontStyle: 'italic',
                    color: "purple.600",
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
              </Heading>
            </GridItem>
          ) : (
            <GridItem>
              <Heading size="2xl" maxW="32">
                {chunk.text}
              </Heading></GridItem>
          )
        })}
      </Grid>
    </GridItem>
  )
}
