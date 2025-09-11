import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import App from './App.tsx'
import { Calendar } from '@progress/kendo-react-dateinputs'
import '@progress/kendo-theme-default/dist/all.css'

createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <App />
    <Calendar />
  </BrowserRouter>,
)
