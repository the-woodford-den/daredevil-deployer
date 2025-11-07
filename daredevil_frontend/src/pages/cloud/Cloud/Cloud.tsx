import { NetworkForm, Note } from '@/components';
import {
  Box,
  Grid,
  GridItem,
  Heading
} from '@chakra-ui/react';

export function Console() {
  return (
    <Grid gap={12} mt="2" mb="2" templateColumns="repeat(3, 1fr)">
      <GridItem colSpan={3}>
        <Heading size="xl" mb="5" className="t-font">
          Cloud Console
        </Heading>
      </GridItem>
      <GridItem colSpan={2}>
        <NetworkForm />
      </GridItem>
      <GridItem>
        <Box
          w="100%"
          background="olive"
          color="gold"
        >
          <Heading size="xl" mb="2" className="t-font">
            KubeCon 2025 November 10-13, 2025 in Atlanta!
          </Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={2}></GridItem>
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
