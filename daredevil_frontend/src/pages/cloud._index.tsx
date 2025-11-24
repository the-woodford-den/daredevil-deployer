import { Outlet, redirect, useLoaderData } from "react-router";
import {
  Box,
  GridItem,
  Mark,
  Text,
} from '@chakra-ui/react';
import { userStore } from "@/state";
import { CloudTree } from "@/components/CloudTree/CloudTree";
import underUrl from '~/underline.svg';

export async function clientLoader() {
  const user = userStore.getState();
  if (!user.username) {
    console.log(user);
    throw redirect("/login");
  }

  return {
    user: user,
    title: 'Just Keep Showing Up & Life Will Reward You',
  };
}

export default function Cloud() {
  let data = useLoaderData();

  return (
    <GridItem alignItems="start" colSpan={3}>
      <Text mt="3" color="aqua" alignItems="right" mb="5" className="t-font">Cloud Console</Text>
      <CloudTree />
      <Outlet />
      <Box>
        <Mark
          key={`${data.user.username}1`}
          css={{
            fontStyle: 'italic',
            color: "purple.500",
            position: "relative",
          }}
        >
          <span>{data.user.username}</span>
          <img
            style={{ position: "absolute", left: 0 }}
            src={underUrl}
            loading="lazy"
            alt="line"
          />
        </Mark>
      </Box>
    </GridItem>
  );
}

