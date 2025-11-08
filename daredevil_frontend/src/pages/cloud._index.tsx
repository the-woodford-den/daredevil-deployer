import { Fragment, } from 'react';
import { Link, useLoaderData } from "react-router";
import { NetworkForm } from '@/components/NetworkForm';
import { Note } from '@/components/Note';
import {
  Box,
  Flex,
  Grid,
  GridItem,
  Heading,
  Stack,
  Highlight,
  Mark,
  useHighlight
} from '@chakra-ui/react';
import underUrl from '~/underline.svg';

export async function clientLoader() {
  return {
    title: 'Just Keep Showing Up & Life Will Reward You',
  };
}

export default function Cloud() {

  let data = useLoaderData();

  const chunks = useHighlight({
    text: "Authenticating & Authorizing Every Connection :: Securing Data Applications :: Build High Performance AI/ML Pipelines :: Building Cloud Native Agentic Workflows on Kubernetes",
    query: ["Securing Data", "Performance", "Authenticating", "AI/ML Pipelines", "Agentic Workflows on Kubernetes"],
  })


  return (
    <Grid gap={12} mt="2" mb="2" templateColumns="repeat(3, 1fr)">
      <GridItem colSpan={3}>
        <Heading size="xl" mb="5" className="t-font">
          Cloud Console
        </Heading>
      </GridItem>
      <GridItem colSpan={2}>
        <NetworkForm />
      </GridItem>
      <GridItem>
        <Box
          w="100%"
          background="olive"
          color="gold"
        >
          <Heading size="xl" mb="2" className="t-font">
            KubeCon 2025 November 10-13, 2025 in Atlanta!
          </Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={2}></GridItem>
      <GridItem>
        <Note
          avatar="mega"
          title="Monitoring"
        >
          This will be used, maybe, as a monitoring area.
          I'm not sure what else can go here.
          We will see how this plays out...
        </Note>
      </GridItem>
      <GridItem colSpan={3}>
        <Stack>
          <Heading size="2xl" letterSpacing="wider">
            <Highlight query="Life Will Reward" styles={{ color: "teal.600", }}>
              {data.title}
            </Highlight>
          </Heading>
          <Heading size="2xl" maxW="32">
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
          </Heading>
        </Stack>
      </GridItem>
      <GridItem colSpan={3}>
        <Flex direction="column">
          <Flex align="center" justifyContent="center">
            <Heading size="sm" className="t-font">
              Operational ~ 2025 Woodford's Den ~ <span>Licenses: </span>
              <Link to="/cloud/repos">Register</Link>
              <span> & </span>
              <Link to="/cloud/console">Login again</Link>
            </Heading>
          </Flex>
        </Flex>
      </GridItem>
    </Grid>
  );
}

