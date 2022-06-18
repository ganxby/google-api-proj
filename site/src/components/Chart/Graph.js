import React from "react";
import {Line} from "react-chartjs-2";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

const Graph = (props) => {

    const lineChartData = {
        labels: props.date,
        datasets: [
            {
                data: props.cost,
                label: 'Стоимость',
                borderColor: "#3333ff",
                fill: true,
                lineTension: 0.5
            }
        ]
    };

    if (!props.state) {
        return <p></p>
    } else {
        return (
            <div>
                <Line
                    type="line"
                    width={160}
                    height={105}
                    data={lineChartData}
                />
            </div>
        )
    }
};

export default Graph;