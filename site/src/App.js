import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import MainPage from "./components/MainPage/MainPage";

function App() {
    return (
        <div className="App">
            <div className="Header">
                <div style={{ marginTop: '2.5rem', marginLeft: '2rem' }}>
                    <h2> Каналсервис</h2>
                </div>
            </div>
            <div className="MainPage">
                <MainPage/>
            </div>
        </div>
    );
}

export default App;
