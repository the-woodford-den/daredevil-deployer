import { Outlet } from 'react-router-dom';
import { Container } from '@chakra-ui/react';
import { Header, Footer } from '@/components/nav';
import { UserProvider } from '@/state/UserProvider';
import './style.css';

export function Layout() {
  return (
    <Container className="layout-container">
      <UserProvider>
        <Header />
        <main>
          <Outlet />
        </main>
      </UserProvider>
      <Footer />
    </Container>
  );
}
