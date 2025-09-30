import { type FC, useState, type ReactNode } from 'react';
import './style.css';
import reactUrl from '~/react.svg';
import rubyUrl from '~/ruby.svg';
import docsUrl from '~/documentation.svg';
import designUrl from '~/design.svg';
import { FaBeer, FaCity, FaDev, FaLemon } from 'react-icons/fa';
import { GiMetroid, GiCapybara, GiRam } from 'react-icons/gi';
import {
  For,
  Grid,
  GridItem,
  IconButton,
  HStack,
  Text,
  VStack,
  Card,
  CardHeader,
  CardTitle,
  CardBody,
  Button,
} from '@chakra-ui/react';



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
    <>
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap="6"
      >
        <GridItem colSpan={2}>
          <section className="section-container">
            <img src={rubyUrl} alt="React Logo" className="ruby-logo" />
            <h3 className="welcome-title">Daredevil Deployer</h3>
            <h4 className="welcome-subtitle">Deploying Apps</h4>
          </section>
        </GridItem>
        <GridItem className="home-welcome-buttons">
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
        </GridItem>
        <GridItem colSpan={3}>
          <section className="section-container get-started">
            <div className="center-section">
              <h5 className="section-title">Welcome Welcome Welcome</h5>
              <div className="k-ml-2">
                <code>using the github api</code>
              </div>
            </div>
          </section>
        </GridItem>
        <GridItem colSpan={3}></GridItem>
      </Grid>
      <Grid templateColumns="repeat(6, 1fr)">
        <GridItem colSpan={6}>
          <h5 className="section-title">Highlights</h5>
        </GridItem>
        <GridItem></GridLayoutItem>
        <GridItem>
          <Card.Root>
            <CardHeader>
              <img src={docsUrl} alt="Documentation Logo" width={64} height={64} />
              <CardTitle>Documentation</CardTitle>
            </CardHeader>
            <CardBody>
              <VStack key="fire">
                <IconButton
                  aria-label={item.id}
                  variant="outline"
                  size="lg"
                >
                  <FaBeer />
                </IconButton>
                <Text textStyle="sm">In development ...</Text>
              </VStack>
            </CardBody>
          </Card.Root>
        </GridItem>
        <GridItem>
          <Card.Root>
            <CardHeader>
              <img src={reactUrl} alt="Virtual Classroom Logo" width={64} height={64} />
              <CardTitle>Using React.js</CardTitle>
            </CardHeader>
            <CardBody>
              <VStack key="nvim">
                <IconButton
                  aria-label="nvimedit"
                  variant="outline"
                  size="lg"
                >
                  <FaCity />
                </IconButton>
                <Text textStyle="sm">Using nvim editor ... Claude Code</Text>
              </VStack>
            </CardBody>
          </Card.Root>
        </GridItem>
        <GridItem>
          <Card.Root>
            <CardHeader>
              <img src={designUrl} alt="Design System Logo" width={64} height={64} />
              <CardTitle>Design System</CardTitle>
            </CardHeader>
            <CardBody>
              <VStack key="components">
                <IconButton
                  aria-label="harmonious"
                  variant="outline"
                  size="lg"
                >
                  <FaDev />
                </IconButton>
                <Text textStyle="sm">
                  Quickly apply harmonious and consistent styles to the components in your app with
                  the Progress Design System.
                </Text>
              </VStack>
            </CardBody>
          </Card.Root>
        </GridItem>
        <GridItem>
          <Card.Root>
            <CardHeader>
              <img src={rubyUrl} alt="ruby" width={64} height={64} />
              <CardTitle>Ruby on Rails</CardTitle>
            </CardHeader>
            <CardBody>
              <VStack key="languages">
                <IconButton
                  aria-label="langs"
                  variant="outline"
                  size="lg"
                >
                  <FaLemon />
                </IconButton>
                <Text textStyle="sm">
                  Ruby, Python, Javascript, Bash
                </Text>
              </VStack>
            </CardBody>
          </Card.Root>
        </GridItem>
      </Grid>
    </>
  );
}
