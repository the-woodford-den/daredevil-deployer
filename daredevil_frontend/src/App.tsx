import { Sentry } from "config";
import { createRoot } from 'react-dom/client';
import { StrictMode } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { Provider } from '@/components/ui/provider';
import { Error404 } from '@/pages/error';
import { Layout } from '@/pages/Layout';
import { Root } from '@/pages/Root';
import { Dashboard, Repositories } from '@/pages/user';
import './index.css';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Root /> },
      { path: '/dashboard', element: <Dashboard /> },
      { path: '/repositories', element: <Repositories /> },
      { path: '*', element: <Error404 /> },
    ],
  },
]);

const container = document.getElementById('root')!

const app = createRoot(container, {
  onUncaughtError: Sentry.reactErrorHandler((error, errorInfo) => {
    console.warn('Uncaught error', error, errorInfo.componentStack);
  }),
  onCaughtError: Sentry.reactErrorHandler(),
  onRecoverableError: Sentry.reactErrorHandler(),
})

app.render(
  <StrictMode>
    <Provider>
      <RouterProvider router={router} />
    </Provider>
  </StrictMode>,
);
