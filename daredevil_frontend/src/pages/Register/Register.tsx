import { Container, Grid, GridItem, Text } from '@chakra-ui/react';
import { RegisterForm } from '@/components/RegisterForm';

export function Register() {

  return (
    <Container>
      <Grid>
        <GridItem>
          <Text>
            Create Daredevil User
          </Text>
        </GridItem>
        <GridItem>
          <RegisterForm />
        </GridItem>
      </Grid>
    </Container>
  );
};

