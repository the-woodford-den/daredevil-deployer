import { userStore } from '@/state/userStore';
import { Link } from 'react-router-dom';
import { Breadcrumb, Flex, Text } from '@chakra-ui/react';
import './style.css';

export function Header() {

  const username = userStore(
    (state) => state.username,
  );
  const signIn = userStore(
    (state) => state.handleSignIn,
  );
  const signOut = userStore(
    (state) => state.handleSignOut,
  );

  const handleSignOut = async (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();
    const result = signOut();

    console.log(result);
  };

  return (
    <Flex direction="column">
      <Flex align="center" justify="space-between" className="t-font header-container">
        <Text marginStart="">Daredevil 🩸 Deployer</Text>
        <Breadcrumb.Root marginEnd="1">
          <Breadcrumb.List>
            {username ? (
              <Breadcrumb.Item>
                <Breadcrumb.Link asChild>
                  <Link to="/">Logout</Link>
                </Breadcrumb.Link>
              </Breadcrumb.Item>
            ) : (
              <Breadcrumb.Item>
                <Breadcrumb.Link asChild>
                  <Link to="/">Homepage</Link>
                </Breadcrumb.Link>
              </Breadcrumb.Item>
            )
            }
            <Breadcrumb.Separator />
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

