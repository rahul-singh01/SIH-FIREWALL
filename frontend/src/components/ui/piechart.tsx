import React from 'react';
import ApexCharts from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';

interface PieChartData {
  name: string;
  value: number;
}

const mockPieChartData: PieChartData[] = [
  { name: 'HTTP', value: 400 },
  { name: 'HTTPS', value: 300 },
  { name: 'FTP', value: 200 },
  { name: 'SMTP', value: 100 },
];

const PieChart: React.FC = () => {
  const options: ApexOptions = {
    chart: {
      type: 'pie',
      background: 'transparent',     
      toolbar: {
        // show: true,
      },
    },
    labels: mockPieChartData.map(data => data.name),
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
        },
      },
    ],
  };

  const series = mockPieChartData.map(data => data.value);

  return (
    <ApexCharts
      options={options}
      series={series}
      type="pie"
      height={250}
    />
  );
};

export default PieChart;