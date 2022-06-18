import React, {useEffect, useState} from 'react';
import './MainPage.css'
import Graph from "../Chart/Graph";
import axios from "axios";

const MainPage = () => {
    const [data, setData] = useState([])
    const [cost, setCost] = useState([])
    const [date, setDate] = useState([])
    const [sum, setSum] = useState(0)

    const [state, setState] = useState(false)

    const getData = () => {
        axios.get('http://127.0.0.1:8000/api/get-data')
            .then(res => {


                res.data.sort((a, b) => new Date(a['delivery_time']) - new Date(b['delivery_time']))
                res.data.forEach(item => {
                    setCost(oldArray => [...oldArray, item['cost_usd']])
                    setDate(oldArray => [...oldArray, item['delivery_time']])
                    const sumAll = res.data.map(item => item.cost_usd).reduce((prev, curr) => prev + curr, 0);
                    setSum(sumAll)
                })

                setData(res.data.sort((a, b) => a['num'] - b['num']))
                setState(true)
            })
    }

    useEffect(() => {
        getData()
    }, [])

    return (
        <div className='MainPage-body'>
            <div className="Left">
                <Graph cost={cost} date={date} state={state}/>
            </div>
            <div className="Right">
                <div className="Right-top">
                    <div style={{width: '30rem'}}>
                        <div style={{
                            width: '100%',
                            background: 'black',
                            color: 'white',
                            height: '3rem',
                            textAlign: 'center',
                            fontSize: 'x-large'
                        }}>
                            Total
                        </div>
                        <div style={{textAlign: 'center', marginTop: '3rem', fontSize: 'xxx-large'}}>
                            {sum}
                        </div>
                    </div>
                </div>
                <div style={{textAlign: 'center'}} className="Right-bottom">
                    <table style={{width: '40rem'}}>
                        <tr style={{background: 'black', color: 'white', }}>
                            <td>№</td>
                            <td>Заказ №</td>
                            <td>Стоимость, $</td>
                            <td>Срок поставки</td>
                        </tr>
                    </table>
                    <div style={{overflowY: "auto", maxHeight: '19rem'}}>
                        <table style={{width: '40rem'}}>
                            {data.map((item, i) =>
                                <tr key={i}>
                                    <td> {item['num']} </td>
                                    <td> {item['order_num']} </td>
                                    <td> {item['cost_usd']} </td>
                                    <td> {item['delivery_time']} </td>
                                </tr>
                            )}
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MainPage;