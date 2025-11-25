import { Outlet, redirect, useLoaderData } from "react-router";
import {
  Box,
  GridItem,
  Heading,
  Mark,
  HStack,
  Center,
} from '@chakra-ui/react';
import { userStore } from "@/state";
import underUrl from '~/underline.svg';

export async function clientLoader() {
  const user = userStore.getState();
  if (!user.username) {
    console.log(user);
    throw redirect("/login");
  }

  const username = user.username;
  const title = `${username!.at(0).toUpperCase()}` +
    `${username!.slice(1)}'s Cloud Console`;

  return {
    title: title,
    footer: 'Just Keep Showing Up & Life Will Reward You',
  };
}

export default function Cloud() {
  let data = useLoaderData();

  return (
    <GridItem alignItems="start" colSpan={3}>
      <Center mb="6" pb="6">
        <HStack>
          <Box>
            <Mark
              key={`${data.name}1`}
              css={{
                fontStyle: 'italic',
                color: "purple.500",
                position: "relative",
              }}
            >
              <Heading textStyle="2xl" className="t-font">{data.title}</Heading>
              <img
                style={{ position: "absolute", left: 0 }}
                src={underUrl}
                loading="lazy"
                alt="line"
              />
            </Mark>
          </Box>
        </HStack>
      </Center>
      <Outlet />
      <Center mt="6" pt="6">
        <Heading textStyle="2xl" className="t-font">{data.footer}</Heading>
      </Center>
    </GridItem>
  );
}

