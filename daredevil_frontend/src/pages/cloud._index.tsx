import { Outlet, redirect, useLoaderData } from "react-router";
import {
  Box,
  Container,
  Grid,
  GridItem,
  Mark,
  Text,
} from '@chakra-ui/react';
import { findApp } from "@/api";
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


  // const cookieHeader = request.headers.get("Cookie");
  const app = await findApp();
  console.log(app);

  return {
    title: 'Just Keep Showing Up & Life Will Reward You',
  };
}


export default function Cloud() {

  let data = useLoaderData();
  const userState = userStore(
    (state) => state.cookie,
  );
  const user = userStore((state) => state);

  if (!userState) {
    throw redirect("/login");
  }

  return (
    <Container>
      <Header />
      <Text mt="3" color="aqua" alignItems="right" mb="5" className="t-font">Cloud Console</Text>
      <Grid gap={12} mt="2" mb="2" templateColumns="repeat(3, 1fr)">
        <GridItem alignItems="start" colSpan={3}>
          <CloudTree />
        </GridItem>
        <GridItem colSpan={3}>
          <Outlet />
        </GridItem>
        <GridItem alignItems="end">
          <Box>
            <Mark
              key={user.gitId}
              css={{
                fontStyle: 'italic',
                color: "purple.500",
                position: "relative",
              }}
            >
              <span>{user.username}</span><span>{data.title}</span>
              <img
                style={{ position: "absolute", left: 0 }}
                src={underUrl}
                loading="lazy"
                alt="line"
              />
            </Mark>
          </Box>
        </GridItem>
      </Grid>
      <Footer />
    </Container>
  );
}

