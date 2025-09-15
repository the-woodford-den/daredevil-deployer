import { createRoot } from 'react-dom/client'
import { StrictMode } from 'react'
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import '@progress/kendo-theme-material/dist/all.css';
import DashboardPage from './modules/dashboard/pages/dashboard-page.tsx';
import Home from './Home.tsx';
import './index.css'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/dashboard/",
    element: <DashboardPage />,
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)

