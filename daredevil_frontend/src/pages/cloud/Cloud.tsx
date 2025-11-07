import { Outlet } from 'react-router-dom';
import {
  Container,
} from '@chakra-ui/react';
import './style.css';


export function Cloud() {

  return (
    <Container>
      <Outlet />
    </Container>
  );
}

