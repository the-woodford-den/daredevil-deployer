import { StrictMode } from 'react';
import { Provider } from '@/components/ui/provider';
import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from 'react-router';
import './index.css';

export function App({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="UTF-8" />
        <link rel="icon" type="image/svg+xml" href="/ruby.svg" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
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
        <Outlet />
      </Provider>
    </StrictMode>
  );
}

