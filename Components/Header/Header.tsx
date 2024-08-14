import React from 'react'
import Carousel from './Carousel'

export default function Header() {
  return (
    <div style={{
      display: 'flex',
      width: '100%',
      backgroundColor:'grey',
      height: '50%',
      flexDirection: 'column',
    }}>
    
      <b
      style={{
        textAlign: 'center',
        width: "100%"
      }}
      >Hello world</b>
      <Carousel/>

      </div>
  )
}
