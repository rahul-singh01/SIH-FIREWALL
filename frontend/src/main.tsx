import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Layout } from './components/layout.tsx'
import Dashboard from './components/dashboard.tsx'
import Rules from './components/rules.tsx'
import Logs from './components/logs.tsx'
import { ThemeProvider } from './components/theme-provider.tsx'

const router = createBrowserRouter([{
  path: "/",
  element: <Layout><Dashboard /></Layout>,
}, {
  path: '/logs',
  element: <Layout><Logs /></Layout>
}, {
  path: "/rules",
  element: <Layout><Rules /></Layout>
}
])


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <RouterProvider router={router} />
    </ThemeProvider>
  </StrictMode>,
)
