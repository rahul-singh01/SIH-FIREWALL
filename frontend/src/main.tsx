import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Layout } from './components/layout'
import Dashboard from './components/dashboard'
import Rules from './components/rules'
import Logs from './components/logs'
import { ThemeProvider } from './components/theme-provider'
import { Login } from './components/login'
import { LandingPage } from './components/landing-page'
import { Signup } from './components/signup'

const router = createBrowserRouter([
  {
    path: '/',
    element: <LandingPage />
  },
  {
    path: '/signup',
    element: <Signup />
  },
  {
    path: '/login',
    element: <Login />
  }, {
    path: "/dashboard",
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
