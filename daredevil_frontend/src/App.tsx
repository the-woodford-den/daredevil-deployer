import { createRoot } from 'react-dom/client';
import { StrictMode } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { Root } from '@pages/Root';
import { Repositories } from '@pages/Repositories';
import { Home } from '@pages/Home';
import { NotHere } from '@pages/NotHere';
import './index.scss';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    children: [
      { index: true, element: <Home /> },
      { path: '/repositories', element: <Repositories /> },
      { path: '*', element: <NotHere /> },
    ],
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
