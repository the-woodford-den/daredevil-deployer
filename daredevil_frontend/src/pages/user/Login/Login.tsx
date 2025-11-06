import { Container, Grid, GridItem, Text } from '@chakra-ui/react';
import { LoginForm } from '@/components';

export function Login() {

  return (
    <Container>
      <Grid>
        <GridItem>
          <Text>
            Welcome, Welcome, Welcome
          </Text>
        </GridItem>
        <GridItem>
          <LoginForm />
        </GridItem>
      </Grid>
    </Container>
  );
};

