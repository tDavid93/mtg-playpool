import React from "react";
import { Card, CardHeader, CardBody, CardFooter, Image, Divider, Text, Flex }  from '@chakra-ui/react'
import "../styles.css"


function Mtg_Card({card}) {
        

    const headerHeight = 50; // Adjust as needed

    // Calculate the scaling factor based on text length and header width
    const calculateScalingFactor = () => {
        const headerElement = document.getElementById("card-header");
        if (!headerElement) return 1;

        const textElement = headerElement.querySelector(".text-element");
        if (!textElement) return 1;

        const textWidth = textElement.offsetWidth;
        const headerWidth = headerElement.offsetWidth;

        return Math.min(1, headerWidth / textWidth);
    };


    return (
        <Card maxW="sm" borderWidth="1px" borderRadius="lg" overflow="auto" size='lg' > 
            <CardHeader className="custom-card-header" height={headerHeight} id="card-header">
                <Text
                    textOverflow={"ellipsis"}
                    whiteSpace="nowrap"
                    overflow="hidden"
                    className="text-element"
                    style={{ transform: `scale(${calculateScalingFactor()})` }}
                >
                    {card.name}
                </Text>
            </CardHeader>
            <Divider orientation="horizontal" color='grey.600'/>
            <CardBody className="custom-card-body">
            <Image src={card.img_url} alt={card.name} />
            </CardBody>
        </Card>
        )};

export default Mtg_Card;