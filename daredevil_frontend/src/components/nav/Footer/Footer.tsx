import bricolageLicense from '~/Bricolage/Grotesque/2025-9-15/license.md?url';
import texturinaLicense from '~/Texturina/2025-9-15/license.md?url';
import { Flex, Heading } from '@chakra-ui/react';
import './style.css';

export function Footer() {
  return (
    <footer className="footer-container">
      <Flex direction="column" pt="6">
        <Flex color="aqua" align="center" justifyContent="center">
          <Heading size="sm" className="t-font">
            Operational ~ 2025 Woodford's Den ~ <span>Licenses: </span>
            <a href={bricolageLicense} target="_blank" rel="noopener noreferrer">
              Bricolage Grotesque
            </a>
            <span> & </span>
            <a href={texturinaLicense} target="_blank" rel="noopener noreferrer">
              Texturina
            </a>
          </Heading>
        </Flex>
      </Flex>
    </footer>
  );
}
