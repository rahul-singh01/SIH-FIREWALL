
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Link } from "react-router-dom"

export const description =
    "A login form with email and password. There's an option to login with Google and a link to sign up if you don't have an account."

export function Login() {
    return (
        <div className="h-screen w-screen ">
            <header className="container mx-auto px-4 py-6">
                <nav className="flex justify-between items-center">
                    <Link to="/">
                        <div className="text-2xl font-bold ">SecureWall</div>
                    </Link>
                    <div className="space-x-4">
                        <Button variant="ghost">Features</Button>
                        {/* <Button variant="ghost">Pricing</Button> */}
                        {/* <Link to={'/login'}>
                            <Button variant="ghost">Login</Button>
                        </Link> */}
                        <Link to="/dashboard">
                            <Button>Get Started</Button>
                        </Link>
                    </div>
                </nav>
            </header>
            <Card className="mx-auto max-w-sm h-fit">
                <CardHeader>
                    <CardTitle className="text-2xl">Login</CardTitle>
                    <CardDescription>
                        Enter your email below to login to your account
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-4">
                        <div className="grid gap-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="m@example.com"
                                required
                            />
                        </div>
                        <div className="grid gap-2">
                            <div className="flex items-center">
                                <Label htmlFor="password">Password</Label>
                                <Link to='#' className="ml-auto inline-block text-sm underline">
                                    Forgot your password?
                                </Link>
                            </div>
                            <Input id="password" type="password" required />
                        </div>
                        <Button type="submit" className="w-full">
                            Login
                        </Button>
                        <Button variant="outline" className="w-full">
                            Login with Google
                        </Button>
                    </div>
                    <div className="mt-4 text-center text-sm">
                        Don&apos;t have an account?{" "}
                        <Link to="/signup" className="underline">
                            Sign up
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}