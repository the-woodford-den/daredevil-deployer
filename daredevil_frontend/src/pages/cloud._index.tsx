import { Outlet, redirect, useLoaderData } from "react-router";
import {
  Box,
  Container,
  Grid,
  GridItem,
  Mark,
  Text,
} from '@chakra-ui/react';
// import { findApp } from "@/api";
import { userStore } from "@/state";
// import type { Route } from "./+types/cloud._index";
// import { authMiddleware, timingMiddleware } from "@/lib/middleware";
import { Footer, Header } from "@/components";
import { CloudTree } from "@/components/CloudTree/CloudTree";
import underUrl from '~/underline.svg';

// export const middleware: Route.MiddlewareFunction[] = [
//   authMiddleware,
// ];
//
// export const clientMiddleware: Route.ClientMiddlewareFunction[] = [timingMiddleware];

export async function clientLoader() {
  // const formRef = useRef<HTMLFormElement>(null);

  const user = userStore.getState();
  if (!user.username) {
    console.log(user);
    throw redirect("/login");
  }

  // const cookieHeader = request.headers.get("Cookie");
  // const app = await findApp();
  // console.log(app);


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

