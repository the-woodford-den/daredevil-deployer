import { Outlet } from 'react-router-dom';
import bricolageLicense from '~/Bricolage/Grotesque/2025-9-15/license.md?url';
import texturinaLicense from '~/Texturina/2025-9-15/license.md?url';
import { Breadcrumb, Container, Heading } from '@chakra-ui/react';
import './style.css';

export function Root() {
  return (
    <div className="root-container">
      <Container centerContent={true} className="header-container">
        <Heading size="sm">Daredevil 🩸 Deployer</Heading>
        <Breadcrumb.Root>
          <Breadcrumb.List>
            <Breadcrumb.Item>
              <Breadcrumb.Link href="/" />
            </Breadcrumb.Item>
            <Breadcrumb.Separator />
            <Breadcrumb.Item>
              <Breadcrumb.Link href="/repositories" />
            </Breadcrumb.Item>
          </Breadcrumb.List>
        </Breadcrumb.Root>
      </Container>
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
    </div>
  );
}
