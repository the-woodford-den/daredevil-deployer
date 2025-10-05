import { useState, type ReactNode } from 'react';
import { Note } from '@/components/Note';
import rubyUrl from '~/ruby.svg';
import { GiMetroid, GiCapybara, GiRam } from 'react-icons/gi';
import {
  Box,
  Code,
  Container,
  Flex,
  For,
  Grid,
  GridItem,
  HStack,
  IconButton,
  Image,
  Text,
  VStack,
} from '@chakra-ui/react';
import './style.css';


interface DataModel {
  id: string;
  text?: string;
  icon?: ReactNode;
  iconClass?: string;
}

const items: DataModel[] = [
  {
    id: 'notion',
    text: 'Notion Docs',
    iconClass: 'metroid',
  },
  {
    id: 'firecracker',
    text: 'Firecracker',
    iconClass: 'capybara',
  },
  {
    id: 'fastapi',
    text: 'Fast API',
    iconClass: 'ram',
  },
];

const icons = {
  capybara: <GiCapybara />,
  metroid: <GiMetroid />,
  ram: <GiRam />,
};


export function Home() {
  const [data] = useState<DataModel[]>(items);
  return (
    <Container>
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap="6"
      >
        <GridItem colSpan={2} pt="3">
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
                <For each={data}>
                  {(item) => (
                    <VStack key={item.id}>
                      <IconButton
                        aria-label={item.id}
                        variant="outline"
                        size="lg"
                      >
                        {item.iconClass && icons[item.iconClass as keyof typeof icons]}
                      </IconButton>
                      <Text textStyle="sm">{item.text}</Text>
                    </VStack>
                  )}
                </For>
              </HStack>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem colSpan={3} pt="3">
          <Flex direction="column">
            <Box
              p="4"
              w="100%"
              _hover={{ bg: "var(--chakra-colors-fg-muted)", color: "black" }}
            >
              <Flex align="center" justify="center" gap="16">
                <Text textStyle="xl">Welcome Welcome Welcome</Text>
                <Code>FastAPI, React.js, Github API</Code>
              </Flex>
            </Box>
          </Flex>
        </GridItem>
        <GridItem pb="2" colSpan={3} >
          <Flex direction="column">
            <Flex align="end" justify="center">
              <Text className="t-font" textStyle="2xl">Github App Login</Text>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem pb="8" colSpan={3} >
          <Flex direction="column">
            <Flex align="center" gap="8" justify="center">
              <Note
                avatar="mega"
                title="Gain Access"
                button="metroid"
                footer="This needs to be an input form"
              >
                Input Field For: Client_ID,
                Possible Field For: userEmail,
                Possible Field For: userName
              </Note>
              <Note
                avatar="ruby"
                title="Network Access"
                button="raspPi"
                footer="This needs to be an input form"
              >
                Input Field For: SSH KEY?,
                Possible Field For: network address,
                Possible Field For: userName
              </Note>
            </Flex>
          </Flex>
        </GridItem>
      </Grid>
      <Grid templateColumns="repeat(4, 1fr)" gap="8">
        <GridItem p="2" colSpan={4} >
          <Flex direction="column">
            <Flex align="end" justify="center">
              <Text className="t-font" textStyle="2xl">Features & Statistics</Text>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem>
          <Note
            avatar="docs"
            title="Documentation"
            button="beer"
            footer="This is Amazing, Bye!"
          >
            We are developing this cards from chakra ui into 'Notes'.
          </Note>
        </GridItem>
        <GridItem>
          <Note
            avatar="react"
            title="React.js Application"
            button="metroid"
            footer="You are Amazing, Bye!"
          >
            Some of my dev tools include nvim, claude, & tmux.
          </Note>
        </GridItem>
        <GridItem>
          <Note
            avatar="mega"
            title="The Design System"
            button="raspPi"
            footer="You are very Special, Bye!"
          >
            Quickly apply harmonious and consistently typed styles.
          </Note>
        </GridItem>
        <GridItem>
          <Note
            avatar="design"
            title="Frameworks"
            button="lemon"
            footer="We contribute to the World, Bye!"
          >
            Python, FastAPI, Javascript, React.js, Github API
          </Note>
        </GridItem>
      </Grid>
    </Container>
  );
}

