import underUrl from '~/underline.svg';
import { useLoaderData } from "react-router";
import {
  Container,
  Mark,
  Separator,
  Text,
} from '@chakra-ui/react';

export async function clientLoader() {
  return {
    title: 'Your Repositories',
  };
}

export function Repos() {
  let data = useLoaderData();

  return (
    <Container direction="column">
      <Text pb="3" textStyle="4xl">{data.title}</Text>
      <Separator pb="3" />
      <Mark
        key={"index"}
        css={{
          fontStyle: "italic",
          color: "red.500",
          position: "relative",
        }}
      >
        <span>Repositories</span>
        <img
          style={{ position: "absolute", left: 0 }}
          src={underUrl}
          loading="lazy"
          alt=""
        />
      </Mark>
      <Separator />
    </Container >
  );
}



