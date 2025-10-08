import { GithubForm } from '@/components/GithubForm';
import { Note } from '@/components/Note';
import {
  Box,
  Grid,
  GridItem,
  Heading
} from '@chakra-ui/react';

export function Dashboard() {
  return (
    <Grid gap={12} mt="2" mb="2" templateColumns="repeat(3, 1fr)">
      <GridItem colSpan={3}>
        <Heading size="5xl" mb="5" className="t-font">
          User Dashboard
        </Heading>
      </GridItem>
      <GridItem colSpan={2}>
        <GithubForm />
      </GridItem>
      <GridItem>
        <Box
          w="100%"
          background="olive"
          color="gold"
        >
          <Heading size="2xl" mb="2" className="t-font">
            We are thinking
          </Heading>
        </Box>
      </GridItem>
      <GridItem></GridItem>
      <GridItem></GridItem>
      <GridItem>
        <Note
          avatar="mega"
          title="Monitoring"
        >
          This will be used, maybe, as a monitoring area.
          I'm not sure what else can go here.
          We will see how this plays out...
        </Note>
      </GridItem>
    </Grid>
  );
}
