import React from "react";
import { Box, Image, Text } from '@chakra-ui/react'

function Mtg_Card({card}) {
        
    return (
        <Box
          maxW="sm"
          borderWidth="1px"
          borderRadius="lg"
          overflow="hidden"
          boxShadow="0 4px 8px rgba(0, 0, 0, 0.1)"
          _hover={{
            boxShadow: "0 6px 12px rgba(0, 0, 0, 0.2)"
          }}
          m={4} // Equivalent to margin: 1rem
          transition="box-shadow 0.3s ease-in-out"
          bg="white"
        > 
            <Box
              p={2} // Equivalent to padding: 0.5rem
              bg="blue.500"
              color="black"
              fontSize="lg"
              fontWeight="bold"
              height="50px"
              lineHeight="50px"
              overflow="hidden"
              whiteSpace="nowrap"
              textOverflow="ellipsis"
              textAlign="center"
            >
                {card.name}
            </Box>
            <Image
              src={card.img_url}
              alt={card.name}
              fit="cover"
              align="center"
              w="100%"
            />
            <Box p={4}>
              <Text fontSize="sm">{card.text}</Text>
            </Box>
        </Box>
    );
}

export default Mtg_Card;