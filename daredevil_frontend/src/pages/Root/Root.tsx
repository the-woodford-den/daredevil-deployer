import { useRef, useState } from 'react';
import { getAccessTokenGithubApp } from '@/api/github';
import { Alarm } from '@/components/Alarm';
import { Note } from '@/components/Note';
import { GithubAppGetForm } from '@/components/GithubAppGetForm';
import {
  type ApiError,
  type GithubTokenResponse,
  type WebLinks
} from '@/data';
import rubyUrl from '~/ruby.svg';
import { GiMetroid, GiCapybara, GiRam } from 'react-icons/gi';
import {
  Box,
  Container,
  Flex,
  For,
  Grid,
  GridItem,
  Heading,
  HStack,
  IconButton,
  Image,
  Text,
  VStack,
} from '@chakra-ui/react';
import './style.css';


const items: WebLinks[] = [
  {
    id: 'notion',
    text: 'Notion Docs',
    iconClass: 'metroid',
    url: 'https://www.notion.com/'
  },
  {
    id: 'firecracker',
    text: 'Firecracker',
    iconClass: 'capybara',
    url: 'https://firecracker-microvm.github.io/'
  },
  {
    id: 'fastapi',
    text: 'Fast API',
    iconClass: 'ram',
    url: 'https://fastapi.tiangolo.com/'
  },
];

const icons = {
  capybara: <GiCapybara />,
  metroid: <GiMetroid />,
  ram: <GiRam />,
};


export function Root() {
  const [jsonData] = useState<WebLinks[]>(items);
  const [githubToken, setGithubToken] = useState<GithubTokenResponse>();
  const [error, setError] = useState<ApiError | null>(null);
  const ref = useRef<HTMLFormElement>(null);

  const handleGithubAppGet = async (data: FormData) => {
    const client_id = data.get("clientId") as string;
    const result = await getAccessTokenGithubApp(client_id);
    result.match(
      (token) => setGithubToken(token),
      (err) => setError(err)
    );
    console.log(githubToken);
    ref.current?.reset();
  };

  return (
    <Container>
      <Flex justify="center" p="3">
        {error ? (
          <Alarm
            status="error"
            title={error.type}
            width="60%"
          >{error.message}</Alarm>
        ) : (
          <Heading size="5xl" className="t-font">
            Welcome Welcome Welcome
          </Heading>
        )}
      </Flex>
      <Grid
        templateColumns="repeat(4, 1fr)"
        gap="6"
      >
        <GridItem colSpan={3} pt="3">
          <Flex direction="column" fontWeight="600">
            <Flex align="center" gap="4" justify="center">
              <Image
                src={rubyUrl}
                alt="Ruby"
                boxSize="6rem"
                fit="contain"
                className="rubyLogo"
              />
              <Text textStyle="7xl">Daredevil Deployer</Text>
            </Flex>
            <Flex align="center" gap="2" justify="center">
              <Text textStyle="3xl">Deploying Apps</Text>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem pt="3">
          <Flex direction="column">
            <Flex align="flex-end" justify="center">
              <HStack gap="6" wrap="wrap">
                <For each={jsonData}>
                  {(item) => (
                    <VStack key={item.id}>
                      <IconButton
                        aria-label={item.id}
                        variant="outline"
                        size="lg"
                        asChild={true}
                      >
                        <a href={item.url} target="_blank">
                          {icons[item.iconClass as keyof typeof icons]}
                        </a>
                      </IconButton>
                      <Text textStyle="sm">{item.text}</Text>
                    </VStack>
                  )}
                </For>
              </HStack>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem pt="6" pb="8" colSpan={2}>
          <Flex
            w="full"
            justify="right"
          >
            <Box
              background="black"
              p="2rem"
              color="white"
              w="65%"
            >
              {githubToken ? (
                <Note
                  avatar="react"
                  title="Client Id"
                  footer={githubToken.clientId}
                >
                  <Text textStyle="2xl">{githubToken.expires_at}</Text>
                </Note>
              ) : (<Text textStyle="5xl">Nada</Text>)}
            </Box>
          </Flex>
        </GridItem>
        <GridItem pt="6" pb="8" colSpan={2}>
          <Flex
            w="full"
            justify="left"
          >
            <Box
              background="black"
              p="2rem"
              color="white"
              w="65%"
            >
              {githubToken ? (
                <Note
                  avatar="mega"
                  title="Access Token"
                  footer={githubToken.token}
                >
                  <Text textStyle="lg">{githubToken.token}</Text>
                </Note>
              ) : (
                <form ref={ref} action={async (formData) => { await handleGithubAppGet(formData) }}>
                  <GithubAppGetForm />
                </form>
              )}
            </Box>
          </Flex>
        </GridItem>
        <GridItem p="2" colSpan={4}>
          <Flex direction="column">
            <Flex align="end" justify="center">
              <Text className="t-font" textStyle="4xl">Features & Statistics</Text>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem>
          <Note
            avatar="docs"
            title="Documentation"
            footer="This is Amazing, Bye!"
          >
            We are developing this cards from chakra ui into 'Notes'.
          </Note>
        </GridItem>
        <GridItem>
          <Note
            avatar="react"
            title="React.js Application"
            footer="You are Amazing, Bye!"
          >
            Some of my dev tools include nvim, claude, & tmux.
          </Note>
        </GridItem>
        <GridItem>
          <Note
            avatar="mega"
            title="The Design System"
            footer="You are very Special, Bye!"
          >
            Quickly apply harmonious and consistently typed styles.
          </Note>
        </GridItem>
        <GridItem>
          <Note
            avatar="design"
            title="Frameworks"
            footer="We contribute to the World, Bye!"
          >
            Python, FastAPI, Javascript, React.js, Github API
          </Note>
        </GridItem>
      </Grid>
    </Container>
  );
}

