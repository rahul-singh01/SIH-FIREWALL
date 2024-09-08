import { Card, CardHeader, CardTitle, CardContent } from "./ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"
import { Button } from "./ui/button"



export default function Rules() {
    return <>
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-card-100 p-6">
            <h3 className="text-3xl font-semibold text-gray-800 dark:text-gray-200 mb-5">Firewall Rules</h3>

            <Card>
                <CardHeader>
                    <CardTitle className="text-lg">Description</CardTitle>
                </CardHeader>
                <CardContent>
                    <form className="space-y-6">
                        <div className="space-y-4">
                            <div>
                                <Label htmlFor="rule-type">Rule Type</Label>
                                <Select>
                                    <SelectTrigger id="rule-type">
                                        <SelectValue placeholder="Select rule type" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="block-ip">Block IP</SelectItem>
                                        <SelectItem value="block-domain">Block Domain</SelectItem>
                                        <SelectItem value="block-port">Block Port</SelectItem>
                                        <SelectItem value="allow-ip">Allow IP</SelectItem>
                                        <SelectItem value="allow-domain">Allow Domain</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div>
                                <Label htmlFor="ip-address">IP Address / Domain</Label>
                                <Input id="ip-address" placeholder="Enter IP address or domain" />
                            </div>
                            <div>
                                <Label htmlFor="port">Port (optional)</Label>
                                <Input id="port" placeholder="Enter port number" type="number" />
                            </div>
                            <div>
                                <Label htmlFor="protocol">Protocol</Label>
                                <Select>
                                    <SelectTrigger id="protocol">
                                        <SelectValue placeholder="Select protocol" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="any">Any</SelectItem>
                                        <SelectItem value="tcp">TCP</SelectItem>
                                        <SelectItem value="udp">UDP</SelectItem>
                                        <SelectItem value="icmp">ICMP</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div>
                                <Label htmlFor="action">Action</Label>
                                <Select>
                                    <SelectTrigger id="action">
                                        <SelectValue placeholder="Select action" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="allow">Allow</SelectItem>
                                        <SelectItem value="deny">Deny</SelectItem>
                                        <SelectItem value="log">Log</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>
                        <Button type="submit">Add Rule</Button>
                    </form>
                </CardContent>
            </Card>
        </main>
    </>
}