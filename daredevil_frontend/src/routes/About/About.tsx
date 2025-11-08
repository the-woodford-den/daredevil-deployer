import { Fragment } from 'react';
import { useLoaderData } from "react-router";
import { Stack, Highlight, Heading, Mark, useHighlight } from '@chakra-ui/react';
import underUrl from '~/underline.svg';

export async function clientLoader() {
  return {
    title: 'Just Keep Showing Up & Life Will Reward You',
  };
}

export default function About() {
  let data = useLoaderData();

  const chunks = useHighlight({
    text: "Authenticating & Authorizing Every Connection :: Securing Data Applications :: Build High Performance AI/ML Pipelines :: Building Cloud Native Agentic Workflows on Kubernetes",
    query: ["Securing Data", "Performance", "Authenticating", "AI/ML Pipelines", "Agentic Workflows on Kubernetes"],
  })


  return (
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
  )
}


