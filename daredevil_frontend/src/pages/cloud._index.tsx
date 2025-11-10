import { Outlet, redirect } from "react-router";
import { userContext } from "src/context";
import {
  Container,
  Grid,
  GridItem,
  Text,
} from '@chakra-ui/react';
import { findInstallation } from "@/api";
import type { Route } from "./+types/cloud._index";
import { authMiddleware, timingMiddleware } from "@/lib/middleware";
import { Footer, Header } from "@/components";
import { CloudTree } from "@/components/CloudTree/CloudTree";

export const middleware: Route.MiddlewareFunction[] = [
  authMiddleware,
];

export const clientMiddleware: Route.ClientMiddlewareFunction[] = [timingMiddleware];

export async function loader({
  context,
}: Route.LoaderArgs) {

  const user = context.get(userContext);
  if (!user) {
    throw redirect("/login");
  }
  const installation = await findInstallation();
  return {
    title: 'Just Keep Showing Up & Life Will Reward You',
    user: user,
    userInstall: installation,
  };
}


export default function Cloud() {

  // let data = useLoaderData();

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
      </Grid>
      <Footer />
    </Container>
  );
}

