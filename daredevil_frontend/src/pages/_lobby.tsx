import { Link, Outlet } from "react-router";
import { Grid, GridItem, Container, Flex, Heading, Separator } from '@chakra-ui/react';
import devilUrl from '~/ddevil-pixel.png';
import megaUrl from '~/mega.png';
import designUrl from '~/design.svg';

export default function Lobby() {
  return (
    <Container>
      <Separator borderColor="cyan.700" borderStyle="groove" borderStartStyle="double" />
      <Grid gap={12} mt="2" mb="2" templateColumns="repeat(3, 1fr)">
        <GridItem colSpan={3} gap={12}>
          <Flex direction="column">
            <Flex align="center" justifyContent="center">
              <img
                style={{ position: "absolute", left: 0 }}
                src={designUrl}
                loading="lazy"
                alt="line"
              />
              <Heading size="sm" className="t-font">
                Operational ~ 2025 Woodford's Den ~ <span>Licenses: </span>
                <Link to="/register">Register</Link>
                <span> & </span>
                <Link to="/login">Login again</Link>
              </Heading>
            </Flex>
          </Flex>
        </GridItem>
        <Separator />
        <GridItem colSpan={3} >
          <img
            style={{ position: "absolute", left: 0 }}
            src={megaUrl}
            loading="lazy"
            alt="line"
          />
          <Heading size="xl" mb="5" className="t-font">
            Cloud Console
          </Heading>
        </GridItem>
        <GridItem colSpan={2} bgImg={devilUrl}>
          <Heading size="xl" mb="2" className="t-font">
            KubeCon 2025 November 10-13, 2025 in Atlanta!
          </Heading>
          <img
            style={{ position: "absolute", left: 0 }}
            src={designUrl}
            loading="lazy"
            alt="line"
          />
        </GridItem>
      </Grid>
      <Outlet />
    </Container>
  );
}

