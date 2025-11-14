import { Header } from '@/components/nav'
import { Footer } from '@/components/nav'
import { Outlet } from "react-router";
import { Container, Grid, Separator } from '@chakra-ui/react';

export default function Lobby() {
  return (
    <Container>
      <Header />
      <Separator />
      <main>
        <Grid
          templateColumns="repeat(3, 1fr)"
          gap="6"
        >
          <Outlet />
        </Grid>
      </main>
      <Container width="75%">
        <Separator />
        <Footer />
      </Container>
    </Container>
  );
}

