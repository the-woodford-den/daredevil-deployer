import { createRoot } from 'react-dom/client'
import { StrictMode } from 'react'
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import '@progress/kendo-theme-material/dist/all.css';
import Root from './routes/Root/Root.tsx'
import Repositories from './routes/Repositories/Repositories.tsx';
import Home from './routes/Home/Home.tsx';
import NotHere from './routes/NotHere/NotHere.tsx';
import './index.scss'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      { index: true, element: <Home /> },
      { path: "/repositories", element: <Repositories /> },
      { path: "*", element: <NotHere /> }
    ],
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)

