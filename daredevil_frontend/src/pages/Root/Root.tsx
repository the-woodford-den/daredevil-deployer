import { useRef, useState } from 'react';
import {
  createGitInstallToken,
  searchGitApps,
  searchGitInstalls
} from '@/api/git';
import { Alarm } from '@/components/Alarm';
import { Note } from '@/components/Note';
import { SearchAppsForm } from '@/components/SearchAppsForm';
import { SearchInstallationsForm } from '@/components/SearchInstallationsForm';
import {
  type ApiError,
  type GitApp,
  type EventItem,
  type GitInstall,
  type Token,
  type WebLinks,
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
  const [eventData, setEventData] = useState<EventItem[] | undefined>(undefined);
  const [app, setApp] = useState<GitApp>();
  const [token, setToken] = useState<Token>();
  const [installation, setInstallation] = useState<GitInstall>();
  const [error, setError] = useState<ApiError | null>(null);
  const ref = useRef<HTMLFormElement>(null);


  const handleSearchApps = async (data: FormData) => {
    const slug = data.get("slug") as string;
    const result = await searchGitApps(slug);
    result.match(
      (app) => setApp(app),
      (err) => setError(err)
    );
    console.log(app);
    ref.current?.reset();
  };

  const handleSearchInstallations = async (data: FormData) => {
    const username = data.get("username") as string;
    const result = await searchGitInstalls(username);
    result.match(
      (installObject) => setInstallation(installObject),
      (err) => setError(err)
    );
    let events: EventItem[] = [];
    if (installation) {
      installation.events.map((event) => (events.push({ id: event, event: event })));
      setEventData(events);
    }
    console.log(installation);
    ref.current?.reset();
  };

  const handleCreateInstallationToken = async (event: any) => {
    event.preventDefault();
    if (!installation) {
      throw Error;
    }
    const result = await createGitInstallToken(installation.id);
    result.match(
      (tokenObject) => setToken(tokenObject),
      (err) => setError(err)
    );
    console.log(token);
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
              {installation ? (
                <>
                  <Text textStyle="xl">{`Installation ID: ${installation.id}`}</Text>
                  <Text textStyle="xl">{`Access Tokens Url: ${installation.accessTokensUrl}`}</Text>
                  <Text textStyle="xl">{`App ID: ${installation.appId}`}</Text>
                  <HStack gap="6" wrap="wrap">
                    <For each={eventData}>
                      {(item) => (
                        <VStack key={item.id}>
                          <Text textStyle="xl">{item.event}</Text>
                        </VStack>
                      )}
                    </For>
                  </HStack>
                  <Text textStyle="lg">{`App Slug: ${installation.appSlug}`}</Text>
                  <Text textStyle="xl">{`Install HTML Url ${installation.htmlUrl}`}</Text>
                </>
              ) : (
                <form ref={ref} action={async (formData) => { await handleSearchInstallations(formData) }}>
                  <SearchInstallationsForm />
                </form>
              )
              }
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
              {app ? (
                <div>
                  <Text textStyle="md">{`App Name: ${app.name}`}</Text>
                  <Text textStyle="md">{`App ID: ${app.id}`}</Text>
                  <Text textStyle="md">{`Client ID: ${app.clientId}`}</Text>
                </div>
              ) : (
                <form ref={ref} action={async (formData) => { await handleSearchApps(formData) }}>
                  <SearchAppsForm />
                </form>
              )}
            </Box>
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
              {installation ? (
                <>
                  <VStack key={installation.id}>
                    <IconButton
                      variant="outline"
                      size="lg"
                      disabled={installation ? true : false}
                      asChild={true}
                    >
                      <a href="#" onClick={handleCreateInstallationToken}>
                        {icons['metroid']}
                      </a>
                    </IconButton>
                    <Text textStyle="sm"> grab {installation.appSlug} token</Text>
                  </VStack>
                </>
              ) : (
                <>
                  <Text textStyle="xl">No Installation ID</Text>
                  <Text textStyle="xl">Therefore ...</Text>
                  <Text textStyle="xl">No Access Token</Text>
                </>
              )}
            </Box>
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
              <>
                <Text textStyle="xl">We will ...</Text>
                <Text textStyle="xl">... do something with a token</Text>
              </>
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

