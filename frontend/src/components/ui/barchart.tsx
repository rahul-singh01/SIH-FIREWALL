import React from 'react';
import ApexCharts from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';

interface BarChartData {
    name: string;
    value: number;
}

const mockBarChartData: BarChartData[] = [
    { name: 'example.com', value: 400 },
    { name: 'test.com', value: 300 },
    { name: 'sample.org', value: 200 },
    { name: 'demo.net', value: 150 },
    { name: 'blocked.site', value: 100 },
];

const BarChart: React.FC = () => {
    const options: ApexOptions = {
        theme: {
            mode: 'dark'
        },
        chart: {
            background: 'transparent',
            type: 'bar',
            toolbar: {
                // show: true,
            },
        },
        xaxis: {
            categories: mockBarChartData.map(data => data.name),
        },
        yaxis: {
            title: {
                text: 'Value',
            },
        },
        tooltip: {
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
                    plotOptions: {
                        bar: {
                            horizontal: false,
                        },
                    },
                },
            },
        ],
    };

    const series = [
        {
            name: 'Values',
            data: mockBarChartData.map(data => data.value),
        },
    ];

    return (
        <ApexCharts
            options={options}
            series={series}
            type="bar"
            height={280}
        />
    );
};

export default BarChart;