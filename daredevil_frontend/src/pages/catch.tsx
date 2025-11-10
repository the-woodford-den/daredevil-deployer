import { Grid, GridItem, Heading } from '@chakra-ui/react';

export default function Catch() {
  return (
    <Grid
      templateColumns="repeat(3, 1fr)"
      gap="6"
      mt="4"
    >
      <GridItem alignSelf="auto" justifySelf="center" colSpan={3}>
        <Heading size="2xl">Route Not Found!</Heading>
      </GridItem>
      <GridItem colSpan={3}></GridItem>
      <GridItem alignSelf="auto" justifySelf="center" colSpan={3}>
        <Heading size="md">Try Again!</Heading>
      </GridItem>
    </Grid>
  );
}

