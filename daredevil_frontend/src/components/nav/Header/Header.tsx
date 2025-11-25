import { userStore } from '@/state/userStore';
import { Link } from 'react-router';
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
    <Flex direction="column" pt="2" pl="2" pr="2">
      <Flex align="center" justify="space-between" className="header-container">
        <Text fontWeight="bold" color="aqua">DareDevil Deployer</Text>
        <Breadcrumb.Root marginEnd="1">
          <Breadcrumb.List>
            <Breadcrumb.Item>
              <Breadcrumb.Link asChild>
                <Link to="/" viewTransition>Home</Link>
              </Breadcrumb.Link>
            </Breadcrumb.Item>
            <Breadcrumb.Separator />
            {username ? (
              <>
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/cloud" viewTransition>Cloud</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
                <Breadcrumb.Separator />
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/cloud/console" viewTransition>Console</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
                <Breadcrumb.Separator />
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/cloud/repos" viewTransition>Repos</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
                <Breadcrumb.Separator />
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/logout" viewTransition>Logout</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
              </>
            ) : (
              <>
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/login" viewTransition>Login</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
                <Breadcrumb.Separator />
                <Breadcrumb.Item>
                  <Breadcrumb.Link asChild>
                    <Link to="/register" viewTransition>Register</Link>
                  </Breadcrumb.Link>
                </Breadcrumb.Item>
              </>
            )
            }
            <Breadcrumb.Separator />
            <Breadcrumb.Item>
              <Breadcrumb.Link asChild>
                <Link to="/about" viewTransition>About</Link>
              </Breadcrumb.Link>
            </Breadcrumb.Item>
          </Breadcrumb.List>
        </Breadcrumb.Root>
      </Flex>
    </Flex>
  );
}

