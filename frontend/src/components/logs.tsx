import { useState, useEffect } from 'react'
import { XIcon } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

const mockLogData = [
    { id: 1, ip: '192.168.1.100', timestamp: '2023-06-15 10:30:15', action: 'Blocked', reason: 'Malicious IP', severity: 'severe' },
    { id: 2, ip: '10.0.0.5', timestamp: '2023-06-15 10:31:22', action: 'Allowed', reason: 'Whitelist', severity: 'normal' },
    { id: 3, ip: '172.16.0.10', timestamp: '2023-06-15 10:32:45', action: 'Blocked', reason: 'Suspicious Activity', severity: 'moderate' },
    { id: 4, ip: '192.168.0.50', timestamp: '2023-06-15 10:33:12', action: 'Blocked', reason: 'Port Scan Attempt', severity: 'severe' },
    { id: 5, ip: '10.1.1.25', timestamp: '2023-06-15 10:34:30', action: 'Allowed', reason: 'Normal Traffic', severity: 'normal' },
]

const mockActiveIPs = [
    '192.168.1.100',
    '10.0.0.5',
    '172.16.0.10',
    '192.168.0.50',
    '10.1.1.25',
]

export default function Logs() {
    const [selectedIPs, setSelectedIPs] = useState<string[]>([])
    const [sortBy, setSortBy] = useState('timestamp')
    const [sortOrder, setSortOrder] = useState('desc')
    const [filteredLogs, setFilteredLogs] = useState(mockLogData)

    useEffect(() => {
        if (selectedIPs.length > 0) {
            setFilteredLogs(mockLogData.filter(log => selectedIPs.includes(log.ip)))
        } else {
            setFilteredLogs(mockLogData)
        }
    }, [selectedIPs])

    const sortedLogs = [...filteredLogs].sort((a, b) => {
        if (sortOrder === 'asc') {
            return a[sortBy] > b[sortBy] ? 1 : -1
        } else {
            return a[sortBy] < b[sortBy] ? 1 : -1
        }
    })

    const toggleIPFilter = (ip: string) => {
        setSelectedIPs(prev =>
            prev.includes(ip) ? prev.filter(selectedIP => selectedIP !== ip) : [...prev, ip]
        )
    }

    const removeIPFilter = (ip: string) => {
        setSelectedIPs(prev => prev.filter(selectedIP => selectedIP !== ip))
    }

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'severe':
                return 'text-red-500 dark:text-red-900'
            case 'moderate':
                return 'text-yellow-500 dark:text-yellow-300'
            case 'normal':
                return 'text-green-500 dark:text-green-900'
            default:
                return ''
        }
    }

    return <main className="flex-1 overflow-x-hidden overflow-y-auto  bg-card p-6">
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h3 className="text-3xl font-semibold text-gray-1000 ">Firewall Logs</h3>
                <div className="flex gap-4">
                    <Select value={sortBy} onValueChange={setSortBy}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Sort by" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="timestamp">Timestamp</SelectItem>
                            <SelectItem value="ip">IP Address</SelectItem>
                            <SelectItem value="action">Action</SelectItem>
                        </SelectContent>
                    </Select>
                    <Select value={sortOrder} onValueChange={setSortOrder}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Sort order" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="asc">Ascending</SelectItem>
                            <SelectItem value="desc">Descending</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Log Entries</CardTitle>
                        {selectedIPs.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-2">
                                {selectedIPs.map(ip => (
                                    <Badge key={ip} variant="secondary" className="text-xs">
                                        {ip}
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            className="ml-1 h-4 w-4 p-0"
                                            onClick={() => removeIPFilter(ip)}
                                        >
                                            <XIcon className="h-3 w-3" />
                                        </Button>
                                    </Badge>
                                ))}
                            </div>
                        )}
                    </CardHeader>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Timestamp</TableHead>
                                    <TableHead>IP Address</TableHead>
                                    <TableHead>Action</TableHead>
                                    <TableHead>Reason</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {sortedLogs.map((log) => (
                                    <TableRow key={log.id} className={`${getSeverityColor(log.severity)}`}>
                                        <TableCell>{log.timestamp}</TableCell>
                                        <TableCell>{log.ip}</TableCell>
                                        <TableCell>{log.action}</TableCell>
                                        <TableCell>{log.reason}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>Active Firewall IPs</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            {mockActiveIPs.map(ip => (
                                <Button
                                    key={ip}
                                    variant={selectedIPs.includes(ip) ? "secondary" : "outline"}
                                    className="w-full justify-start"
                                    onClick={() => toggleIPFilter(ip)}
                                >
                                    {ip}
                                </Button>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </main>
}