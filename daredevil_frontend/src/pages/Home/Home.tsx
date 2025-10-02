import { useState, type ReactNode } from 'react';
import { Note } from '@components/Note';
import reactUrl from '~/react.svg';
import rubyUrl from '~/ruby.svg';
import docsUrl from '~/documentation.svg';
import designUrl from '~/design.svg';
import megaUrl from '~/mega.png';
import { FaBeer, FaCity, FaDev, FaLemon } from 'react-icons/fa';
import { GiMetroid, GiCapybara, GiRam } from 'react-icons/gi';
import {
  Avatar,
  Box,
  Card,
  Code,
  Container,
  Flex,
  For,
  Grid,
  GridItem,
  HStack,
  IconButton,
  Image,
  Strong,
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
        <GridItem colSpan={3}></GridItem>
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
          <Card.Root>
            <Card.Body gap="4">
              <HStack mb="6" gap="6">
                <Avatar.Root size="lg" shape="full">
                  <Avatar.Image src={reactUrl} />
                  <Avatar.Fallback name="React Logo" />
                </Avatar.Root>
                <Card.Title>
                  <Text fontWeight="semibold" textStyle="lg">
                    Using React.js
                  </Text>
                </Card.Title>
              </HStack>
              <HStack mb="6" gap="6">
                <IconButton
                  aria-label="nvimedit"
                  variant="outline"
                  size="lg"
                >
                  <FaCity />
                </IconButton>
                <Card.Description>
                  <Strong>Using nvim editor & Claude</Strong>
                </Card.Description>
              </HStack>
              <Card.Footer unstyled={true}>
                <Flex align="center" justify="center">
                  <Strong textStyle="sm">See ya next time!</Strong>
                </Flex>
              </Card.Footer>
            </Card.Body>
          </Card.Root>
        </GridItem>
        <GridItem>
          <Card.Root>
            <Card.Body gap="4">
              <HStack mb="6" gap="6">
                <Avatar.Root size="lg" shape="full">
                  <Avatar.Image src={designUrl} />
                  <Avatar.Fallback name="Design System Logo" />
                </Avatar.Root>
                <Card.Title>
                  <Text fontWeight="semibold" textStyle="lg">
                    Design System
                  </Text>
                </Card.Title>
              </HStack>
              <HStack mb="6" gap="6">
                <IconButton
                  aria-label="harmonious"
                  variant="outline"
                  size="lg"
                >
                  <FaDev />
                </IconButton>
                <Card.Description>
                  <Strong>Quickly apply harmonious and consistent styles</Strong>
                </Card.Description>
              </HStack>
              <Card.Footer unstyled={true}>
                <Flex align="center" justify="center">
                  <Strong textStyle="sm">Direct Connection</Strong>
                </Flex>
              </Card.Footer>
            </Card.Body>
          </Card.Root>
        </GridItem>
        <GridItem>
          <Card.Root>
            <Card.Body gap="4">
              <HStack mb="6" gap="6">
                <Avatar.Root size="lg" shape="full">
                  <Avatar.Image src={megaUrl} />
                  <Avatar.Fallback name="MegaMan" />
                </Avatar.Root>
                <Card.Title>
                  <Text fontWeight="semibold" textStyle="lg">
                    Frameworks & Langs
                  </Text>
                </Card.Title>
              </HStack>
              <HStack mb="6" gap="6">
                <IconButton
                  aria-label="lemon"
                  variant="outline"
                  size="lg"
                >
                  <FaLemon />
                </IconButton>
                <Card.Description>
                  <Strong>Python, Javascript, Bash</Strong>
                </Card.Description>
              </HStack>
              <Card.Footer unstyled={true}>
                <Flex align="center" justify="center">
                  <Strong textStyle="sm">Fast Quick Speed</Strong>
                </Flex>
              </Card.Footer>
            </Card.Body>
          </Card.Root>
        </GridItem>
      </Grid>
    </Container>
  );
}
