import { Sentry } from "config";
import { createRoot } from 'react-dom/client';
import { StrictMode } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { Provider } from '@/components/ui/provider';
import { Error404 } from '@/pages/error';
import { Lobby } from '@/pages/git';
import { Dashboard, Login, Register, Repositories } from '@/pages/user';
import App from './App';
import './index.css';


const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/user', children: [
          { index: true, path: '/login', element: <Login /> },
          { path: '/create', element: <Register /> },
          { path: '/dashboard', element: <Dashboard /> },
          { path: '/repositories', element: <Repositories /> },
        ],
      },
      { path: '/lobby', element: <Lobby /> },
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

