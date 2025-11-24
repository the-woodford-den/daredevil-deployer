import { Link } from "react-router";
import { Container, Flex, Heading } from '@chakra-ui/react';

export default function User() {
  return (
    <Container>
      <Flex direction="column">
        <Flex align="center" justifyContent="center">
          <Heading size="sm" className="t-font">
            Operational ~ 2025 Woodford's Den ~ <span>Licenses: </span>
            <Link to="/cloud/repos">Register</Link>
            <span> & </span>
            <Link to="/cloud/console">Login again</Link>
          </Heading>
        </Flex>
      </Flex>
    </Container>
  );
}



