import React from 'react'
import { icon } from './Carousel'
import './Icon.css'
export default function Icon(props: any) {
  
    console.log(props)

    let currentIcon: icon = props.inputIcon

    return (
    <div 
    className='icon'
    style = {{
        width: "50px",
        height:"50px",
        // overflow: 'hidden',
        // border: 1,
        borderColor: "black",
        borderWidth: "2px",
        borderStyle: "dashed",

    }}
    
    >
        <b>{currentIcon.name}</b>
        <img src={"https://picsum.photos/200/200/?blur"}/>
    </div>
  )
}
