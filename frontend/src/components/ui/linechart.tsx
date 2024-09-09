import React from 'react';
import ApexCharts from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';

interface LineChartData {
    name: string;
    blocked: number;
    allowed: number;
}

const mockLineChartData: LineChartData[] = [
    { name: 'Jan', blocked: 400, allowed: 2400 },
    { name: 'Feb', blocked: 300, allowed: 1398 },
    { name: 'Mar', blocked: 200, allowed: 9800 },
    { name: 'Apr', blocked: 278, allowed: 3908 },
    { name: 'May', blocked: 189, allowed: 4800 },
    { name: 'Jun', blocked: 239, allowed: 3800 },
];

const LineChart: React.FC = () => {
    const options: ApexOptions = {
        theme: {
            mode: 'dark'
        },
        chart: {
            background:'transparent',
            type: 'line',
            toolbar: {
                // show: true,
            },
        },
        xaxis: {
            categories: mockLineChartData.map(data => data.name),
        },
        yaxis: {
            title: {
                text: 'Value',
            },
        },
        tooltip: {
            x: {
                format: 'dd/MM/yy',
            },
            y: {
                formatter: (value: number) => `${value}`,
            },
        },
        responsive: [
            {
                breakpoint: 600,
                options: {
                    chart: {
                        width: '100%',
                    },
                },
            },
        ],
    };

    const series = [
        {
            name: 'Blocked',
            data: mockLineChartData.map(data => data.blocked),
        },
        {
            name: 'Allowed',
            data: mockLineChartData.map(data => data.allowed),
        },
    ];

    return (
        <ApexCharts
            options={options}
            series={series}
            type="line"
            height={250}
        />
    );
};

export default LineChart;