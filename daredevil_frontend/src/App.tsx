import { Container } from '@chakra-ui/react';
import { Header, Footer, Main } from '@/components/nav';
import { Cloud } from '@/pages/cloud';
import './style.css';

export default function App() {
  return (
    <Container className="layout-container">
      <Header />
      <Main>
        <Cloud />
      </Main>
      <Footer />
    </Container>
  );
}

