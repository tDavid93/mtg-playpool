import React from "react";
import { Card, CardHeader, CardBody, CardFooter, Image, Divider }  from '@chakra-ui/react'

function Mtg_Card({card}) {
    

    return (
        <Card maxW="sm" borderWidth="1px" borderRadius="lg" overflow="hidden" size='lg' >
            
            <CardHeader bg="gray.200">{card.name}</CardHeader>
            <Divider orientation="horizontal" color='grey.600'/>
            <CardBody>
            <Image src={card.img_url} alt={card.name} />
            </CardBody>
        </Card>
        )};

export default Mtg_Card;