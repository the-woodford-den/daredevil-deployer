import { StrictMode } from 'react';
import { Provider } from '@/components/ui/provider';
import { Header, Footer } from '@/components/nav'
import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from 'react-router';
import { Container, Grid } from '@chakra-ui/react';
import './index.css';

export function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="UTF-8" />
        <meta name="author" content="Adam Kaewell" />
        <meta name="keywords" content="python, fastapi, javascript, react, css, html" />
        <meta name="description" content="Deployment Application using Github API" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="icon" type="image/svg+xml" href="/ruby.svg" />
        <link href="/assets/Bricolage/Grotesque/2025-9-15/bricolage-grotesque.css" rel="preload" as="style" />
        <link href="/assets/Bricolage/Grotesque/2025-9-15/bricolage-grotesque.css" rel="stylesheet" />
        <link href="/assets/Texturina/2025-9-15/texturina.css" rel="preload" as="style" />
        <link href="/assets/Texturina/2025-9-15/texturina.css" rel="stylesheet" />
        <title>Daredevil Deployer</title>
        <Meta />
        <Links />
      </head>
      <body suppressHydrationWarning>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function Root() {
  return (
    <StrictMode>
      <Provider>
        <Container>
          <Header />
          <main>
            <Grid
              templateColumns="repeat(3, 1fr)"
              gap="6"
              pt="2"
              pb="6"
            >
              <Outlet />
            </Grid>
          </main>
          <Container width="75%">
            <Footer />
          </Container>
        </Container>
      </Provider>
    </StrictMode>
  );
}

