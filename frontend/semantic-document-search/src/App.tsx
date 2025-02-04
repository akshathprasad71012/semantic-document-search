import { useState } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [count, setCount] = useState(5)
  const [querry, setQuerry] = useState("")
  const [results, setResults] = useState([])
   
  function handleQuerryChange(e){
    setQuerry(e.target.value);
  }

  function handleCountChange(e){
    setCount(e.target.value);
  }

  function handleButton(){
     const getResults = async ()=> {
        const r = await axios.get(`http://127.0.0.1:8000/${querry}/${count}`);
        setResults(r['data']['results'])
    }
    getResults();
  }

  return (
    <>
      <div className='input-area'>
        <input id='search-box' type='text' placeholder='Describe the document you are looking for...' onChange={handleQuerryChange}/>      
        <input id='count-box' type='number' placeholder='5' min={1} defaultValue={5} onChange={handleCountChange}/>
        <input id='search-button' type='button' value={"Search"} onClick={handleButton} />
      </div>
        {
            (results?.length >= 1) && (
                
      <div className='result-box'>
        <ul>
        {results.map(result => (<li><div className='result-element'><h5>{result}</h5></div></li>))}
        </ul>
      </div>
            )
        }
        
    </>
  )
}

export default App
