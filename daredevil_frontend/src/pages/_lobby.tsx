import { Header } from '@/components/nav'
import { Footer } from '@/components/nav'
import { Outlet } from "react-router";
import { Container, } from '@chakra-ui/react';

export default function Lobby() {
  return (
    <Container>
      <Header />
      <main>
        <Outlet />
      </main>
      <Footer />
    </Container>
  );
}

