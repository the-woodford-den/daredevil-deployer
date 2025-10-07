import { useState, type ReactNode } from 'react';
import { Note } from '@/components/Note';
import { LoginForm } from '@/components/LoginForm';
import { NetworkForm } from '@/components/NetworkForm';
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
  Stack,
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
        <GridItem colSpan={4} pt="3">
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
        <GridItem pb="2" colSpan={4} >
          <Flex direction="column">
            <Flex align="end" justify="center">
              <Text className="t-font" textStyle="2xl">Github App Login</Text>
            </Flex>
          </Flex>
        </GridItem>
        <GridItem pb="8" colSpan={2}>
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
              <LoginForm />
            </Box>
          </Flex>
        </GridItem>
        <GridItem pb="8" colSpan={2}>
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
              <NetworkForm />
            </Box>
          </Flex>
        </GridItem>
        <GridItem p="2" colSpan={4}>
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

