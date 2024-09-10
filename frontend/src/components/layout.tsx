import { useEffect, useState } from 'react'
import { Bell, ChevronDown, LayoutDashboard, Shield, LogOut, Menu, X, List } from 'lucide-react'
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Link, useLocation } from 'react-router-dom'
import { ModeToggle } from './mode-toggle'

export function Layout({ children }: { children: React.ReactNode }) {
  const [activePage, setActivePage] = useState<String | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    const saved = localStorage.getItem('sidebarOpen');
    return saved !== null ? JSON.parse(saved) : false;
  });

  const route = useLocation();
  useEffect(() => {
    localStorage.setItem('sidebarOpen', JSON.stringify(sidebarOpen));
  }, [sidebarOpen]);

  useEffect(() => {
    setActivePage(route.pathname.split('/')[1])
  }, [route])


  return (
    <div className="flex h-screen bg-card">
      {/* Sidebar */}
      <aside className={`bg-card shadow-md transition-all duration-300 ease-in-out ${sidebarOpen ? 'w-64' : 'w-16'}
      `}
      >
        <div className="p-4 flex items-center justify-between">
          <Link to="/">
            <h1 className={`text-2xl font-bold text-gray-800 dark:text-gray-200 ${sidebarOpen ? 'block' : 'hidden'}`}>SecureWall</h1>
          </Link>
          <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(!sidebarOpen)}
          // className="lg:hidden"
          >
            {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </Button>
        </div>
        <nav className="mt-6 p-2 flex flex-col gap-2">
          <Link to="/dashboard">
            <Button
              variant={activePage === 'dashboard' ? 'default' : 'ghost'}
              className="w-full justify-start"
            >
              <LayoutDashboard className="h-4 w-4" />
              <span className={`ml-2 ${sidebarOpen ? 'inline-block' : 'hidden'} `}>Dashboard</span>
            </Button>
          </Link>
          <Link to="/rules">
            <Button
              variant={activePage === 'rules' ? 'default' : 'ghost'}
              className="w-full justify-start"
            >
              <Shield className="h-4 w-4" />
              <span className={`ml-2 ${sidebarOpen ? 'inline-block' : 'hidden'}`}>Firewall Rules</span>
            </Button>
          </Link>
          <Link to='/logs'>
            <Button
              variant={activePage === 'logs' ? 'default' : 'ghost'}
              className="w-full justify-start"
            >
              <List className="h-4 w-4" />
              <span className={`ml-2 ${sidebarOpen ? 'inline-block' : 'hidden'} `}>Logs</span>
            </Button>
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Navbar */}
        <header className="bg-card shadow-sm border-border">
          <div className="flex items-center justify-between p-4">
            <div className="flex items-center">
              {/* <h1 className="text-3xl font-semibold text-gray-800 dark:text-gray-200">
                {activePage === '' ? 'Dashboard' : activePage === 'rules' ? 'Firewall Rules' : 'Logs'}
              </h1> */}
            </div>
            <div className="flex items-center space-x-4">
              <ModeToggle />
              <Button variant="ghost" size="icon">
                <Bell className="h-5 w-5" />
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="ml-2">
                    <img
                      src="/placeholder.svg?height=32&width=32"
                      alt="User avatar"
                      className="w-8 h-8 rounded-full mr-2"
                    />
                    <span className="hidden md:inline">Admin User</span>
                    <ChevronDown className="ml-2 h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>My Account</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>Profile</DropdownMenuItem>
                  <DropdownMenuItem>Settings</DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </header>

        {/* Page Content */}
        {children}
      </div>
    </div>)
}