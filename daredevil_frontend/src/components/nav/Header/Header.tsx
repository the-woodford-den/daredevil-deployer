import { Link } from 'react-router-dom';
import { Breadcrumb, Flex, Text } from '@chakra-ui/react';
import './style.css';

export function Header() {
  return (
    <Flex direction="column">
      <Flex align="center" justify="space-between" className="t-font header-container">
        <Text marginStart="">Daredevil 🩸 Deployer</Text>
        <Breadcrumb.Root marginEnd="1">
          <Breadcrumb.List>
            <Breadcrumb.Item>
              <Breadcrumb.Link asChild>
                <Link to="/">Homepage</Link>
              </Breadcrumb.Link>
            </Breadcrumb.Item>
            <Breadcrumb.Separator />
            <Breadcrumb.Item>
              <Breadcrumb.Link asChild>
                <Link to="/dashboard">Dashboard</Link>
              </Breadcrumb.Link>
            </Breadcrumb.Item>
          </Breadcrumb.List>
        </Breadcrumb.Root>
      </Flex>
    </Flex>
  );
}

