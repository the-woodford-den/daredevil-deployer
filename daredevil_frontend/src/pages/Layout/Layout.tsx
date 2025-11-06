import { Outlet } from 'react-router-dom';
import { Container } from '@chakra-ui/react';
import { Header, Footer } from '@/components/nav';
import './style.css';

export function Layout() {
  return (
    <Container className="layout-container">
      <Header />
      <main>
        <Outlet />
      </main>
      <Footer />
    </Container>
  );
}
