import React, { useContext } from "react";
import { Card, CardHeader, CardBody, CardFooter, Image, Divider, Text, Flex, Button }  from '@chakra-ui/react'
import "../styles.css"
import { axiosPrivate } from "../api/axios";
import { useEffect, useState } from "react";
import ActiveDeckContext from "../context/ActiveDeckContext";

function Mtg_Card({card}) {

    const [currentDeck, setCurrentDeck] = useContext(ActiveDeckContext);
        

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

    const handleAddCard = async () => {
        try {
            console.log(currentDeck)
            let response = await axiosPrivate.post('/deck/add_card', {card_id: card.uuid, deck_id: currentDeck});
            const data = await response.data;
            console.log(data);
        } catch (e) {
            console.log(e);
        } finally {
            console.log('Card added to deck');
        }
    };
    useEffect(() => {
    }, [currentDeck, card]);

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
            <Divider orientation="horizontal" color='grey.600'/>
            <CardFooter className="custom-card-footer">
                <Flex justify='space-between'>
                    <Button colorScheme='teal' size='sm' onClick={handleAddCard}>
                        <Text color='white'>Add to Deck</Text></Button>
                    </Flex>
            </CardFooter>
        </Card>
        )};

export default Mtg_Card;