
import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Shield, Lock, Zap, Globe, CheckCircle } from 'lucide-react'
import { Link } from 'react-router-dom'
import { SparklesCore } from './ui/sparkles'

export function LandingPage() {
  const [email, setEmail] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission here
    console.log('Submitted email:', email)
    setEmail('')
  }

  return (
    <div className="min-h-screen  from-gray-100 to-white  ">
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <Link to="/">
            <div className="text-2xl font-bold ">SecureWall</div>
          </Link>
          <div className="space-x-4">
            <Button variant="ghost">Features</Button>
            {/* <Button variant="ghost">Pricing</Button> */}
            <Link to={'/login'}>
              <Button variant="ghost">Login</Button>
            </Link>
            <Link to="/dashboard">
              <Button>Get Started</Button>
            </Link>
          </div>
        </nav>
      </header>

      <main>

        {/* Hero Section */}
        <section className="container mx-auto px-4 py-20 text-center ">
          <div className="w-full flex flex-col items-center justify-center overflow-hidden rounded-md">
            <h3 className='text-2xl  text-gray-600 '>Protect Your Network With</h3>
            <h1 className="md:text-7xl text-xl lg:text-9xl font-bold text-center relative z-20">
              SecureWall
            </h1>
            <div className="w-[40rem] h-20 relative">
              {/* Gradients */}
              <div className="absolute inset-x-20 top-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent h-[2px] w-3/4 blur-sm" />
              <div className="absolute inset-x-20 top-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent h-px w-3/4" />
              <div className="absolute inset-x-60 top-0 bg-gradient-to-r from-transparent via-sky-500 to-transparent h-[5px] w-1/4 blur-sm" />
              <div className="absolute inset-x-60 top-0 bg-gradient-to-r from-transparent via-sky-500 to-transparent h-px w-1/4" />

              <div className="absolute inset-0 w-full h-full [mask-image:radial-gradient(350px_200px_at_top,transparent_20%,white)]"></div>
            </div>
            <p className="text-xl mb-8 text-muted-foreground">Advanced firewall solution for businesses of all sizes</p>
            <div className="flex justify-center space-x-4">
              <Link to="/dashboard">
                <Button size="lg">Get Started</Button>
              </Link>
              <Button size="lg" variant="outline">Watch Demo</Button>
            </div>

          </div>


        </section>


        {/* Features Section */}
        <section className="py-20 ">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">Key Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              <Card>
                <CardHeader>
                  <Shield className="w-10 h-10 text-primary mb-2" />
                  <CardTitle>Advanced Threat Protection</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Real-time monitoring and protection against the latest cyber threats.</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <Lock className="w-10 h-10 text-primary mb-2" />
                  <CardTitle>Secure VPN</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Encrypted connections for secure remote access to your network.</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <Zap className="w-10 h-10 text-primary mb-2" />
                  <CardTitle>High Performance</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Optimized for speed with minimal impact on network performance.</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <Globe className="w-10 h-10 text-primary mb-2" />
                  <CardTitle>Cloud Integration</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Seamless integration with popular cloud services and platforms.</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Pricing Section
        <section className="container mx-auto px-4 py-20">
          <h2 className="text-3xl font-bold text-center mb-12">Simple, Transparent Pricing</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <CardTitle>Basic</CardTitle>
                <CardDescription>For small businesses</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold mb-4">$29<span className="text-sm font-normal">/month</span></p>
                <ul className="space-y-2">
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> Basic threat protection</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> 5 VPN connections</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> Email support</li>
                </ul>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Choose Plan</Button>
              </CardFooter>
            </Card>
            <Card className="border-primary">
              <CardHeader>
                <CardTitle>Pro</CardTitle>
                <CardDescription>For growing companies</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold mb-4">$99<span className="text-sm font-normal">/month</span></p>
                <ul className="space-y-2">
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> Advanced threat protection</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> 20 VPN connections</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> 24/7 phone & email support</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> Cloud integration</li>
                </ul>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Choose Plan</Button>
              </CardFooter>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Enterprise</CardTitle>
                <CardDescription>For large organizations</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold mb-4">Custom</p>
                <ul className="space-y-2">
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> Custom security solutions</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> Unlimited VPN connections</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> 24/7 dedicated support</li>
                  <li className="flex items-center"><CheckCircle className="w-5 h-5 text-primary mr-2" /> On-premise deployment option</li>
                </ul>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Contact Sales</Button>
              </CardFooter>
            </Card>
          </div>
        </section> */}

        {/* CTA Section */}

        <section className="bg-primary text-primary-foreground py-20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to secure your network?</h2>
            <p className="text-xl mb-8">Start your free trial today. No credit card required.</p>
            <form onSubmit={handleSubmit} className="flex justify-center max-w-md mx-auto">
              <Input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="rounded-r-none"
                required
              />
              <Button type="submit" className="rounded-l-none">Get Started</Button>
            </form>
          </div>
        </section>
      </main>


      <footer className="py-12 ">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold mb-4">Product</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">Features</a></li>
                {/* <li><a href="#" className="hover:underline">Pricing</a></li> */}
                <li><a href="#" className="hover:underline">Demo</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Company</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">About</a></li>
                <li><a href="#" className="hover:underline">Careers</a></li>
                <li><a href="#" className="hover:underline">Contact</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Resources</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">Blog</a></li>
                <li><a href="#" className="hover:underline">Documentation</a></li>
                <li><a href="#" className="hover:underline">Support</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Legal</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">Privacy Policy</a></li>
                <li><a href="#" className="hover:underline">Terms of Service</a></li>
                <li><a href="#" className="hover:underline">Cookie Policy</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-12 text-center text-sm text-muted-foreground">
            © 2023 SecureWall. All rights reserved.
          </div>
        </div>
      </footer>
    </div >

  )
}