import { Container, Grid, GridItem, Text } from '@chakra-ui/react';
import { RegisterForm } from '@/components';

export function Register() {

  return (
    <Container>
      <Grid>
        <GridItem>
          <Text>
            The Woodford Den: Daredevil Deployer Registration
          </Text>
        </GridItem>
        <GridItem>
          <RegisterForm />
        </GridItem>
      </Grid>
    </Container>
  );
};

