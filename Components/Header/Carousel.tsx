import React, { useState } from 'react'
import Icon from './Icon'


export interface icon {
    name: string,
    iconUrl: string,
}


export default function Carousel() {

    const [iconList, setIconlist] = useState<icon[]>([])

    const [isLoading, setLoading] = useState(true)



    if (isLoading) {
        setLoading(false)
        let iconListTemp: icon[] = []

        for (let i = 0; i < 30; i++) {
            let newIcon: icon = {
                iconUrl: "asdfasdfsadf",
                name: `Icon ${i}`
            }
            iconListTemp.push(newIcon)
    
        }

        setIconlist(iconListTemp)

        console.log(iconListTemp)
    }



    return (
    <div
    style={{
        width: "100%",
        height: "50px",
        backgroundColor: "red",
        display: "flex",
        
        flexDirection: "row",
        
        // overflowX:"scroll",
        
    }}
    >
        {iconList.length > 0 &&
        <div
        style={{
            width: "100%",
            height: "80px",
            backgroundColor: "red",
            display: "flex",
            
            flexDirection: "row",
            overflowX:"scroll",
            // overflowY: "hidden"
            
        }}
        >
            {iconList.map((icon: icon) => {
                return (
                    <Icon inputIcon= {icon}/>
                )
            })}
        </div>}
        
    
    </div>
  )
}
