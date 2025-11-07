import { Container } from '@chakra-ui/react';
import { Header, Footer, Main } from '@/components/nav';
import './style.css';

export default function App() {
  return (
    <Container className="layout-container">
      <Header />
      <Main />
      <Footer />
    </Container>
  );
}

