import { Link } from "react-router";
import { Container, Flex, Heading } from '@chakra-ui/react';

export default function Profile() {
  return (
    <Container>
      <Flex direction="column">
        <Flex align="center" justifyContent="center">
          <Heading size="sm" className="t-font">
            Operational ~ 2025 Woodford's Den ~ <span>Licenses: </span>
            <Link to="/catch">Catch</Link>
            <span> & </span>
            <Link to="/">Home</Link>
          </Heading>
        </Flex>
      </Flex>
    </Container>
  );
}



