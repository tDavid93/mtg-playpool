import React from "react";
import { Card, CardHeader, CardBody, CardFooter, Image, Divider, Text, Flex }  from '@chakra-ui/react'

function Mtg_Card({card}) {
    

    return (
        <Card maxW="sm" borderWidth="1px" borderRadius="lg" overflow="auto" size='lg' > 
            <CardHeader bg="gray.200" height={50}>
                <Text overflow={"hidden"}>{card.name}</Text>
                </CardHeader>
            <Divider orientation="horizontal" color='grey.600'/>
            <CardBody>
            <Image src={card.img_url} alt={card.name} />
            </CardBody>
        </Card>
        )};

export default Mtg_Card;