import { Link } from 'react-router-dom';
import { Outlet } from 'react-router-dom';
import bricolageLicense from '~/Bricolage/Grotesque/2025-9-15/license.md?url';
import texturinaLicense from '~/Texturina/2025-9-15/license.md?url';
import { Box, Text, Breadcrumb, Container, Flex, Heading, Spacer } from '@chakra-ui/react';
import { LuZap } from 'react-icons/lu';
import './style.css';

export function Root() {
  return (
    <Container className="root-container">
      <Flex direction="column">
        <Flex align="center" className="header-container">
          <Box className="b-g-font">Daredevil 🩸 Deployer</Box>
          <Spacer />
          <Box>
            <Breadcrumb.Root marginEnd="auto">
              <Breadcrumb.List>
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/">Home</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
                <Breadcrumb.Separator />
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/repositories">Repositories</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
              </Breadcrumb.List>
            </Breadcrumb.Root>
          </Box>
        </Flex>
      </Flex>
      <main>
        <Outlet />
      </main>
      <footer className="footer-container">
        <Heading size="sm">
          Operational ~ 2025 Woodford's Den ~ <span>Licenses: </span>
          <a href={bricolageLicense} target="_blank" rel="noopener noreferrer">
            Bricolage Grotesque
          </a>
          <span> & </span>
          <a href={texturinaLicense} target="_blank" rel="noopener noreferrer">
            Texturina
          </a>
        </Heading>
      </footer>
    </Container>
  );
}
