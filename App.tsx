import React from 'react';
import logo from './logo.svg';
import Header from './Components/Header/Header';
import Body from './Components/Body';
// import './App.css';

function App() {
  return (
    <div className="App" 
    style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      alignItems: 'flex-start',
      height: "100vh",
      flex: 1
    }}
    >
      <Header/>
      <Body/>

    </div>
  );
}

export default App;
