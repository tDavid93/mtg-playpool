import React from 'react';
import { Box, Image, Text, useColorModeValue } from '@chakra-ui/react';

function Mtg_Card({card}) {
  const cardBgColor = useColorModeValue('lightParchment', 'stoneGray');
  const cardShadow = useColorModeValue('lg', 'dark-lg');
        
    return (
        <Box
        maxW="sm"
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
        bg={cardBgColor}
        shadow={cardShadow}
        _hover={{ shadow: 'xl' }}
        transition="shadow 0.2s"
        role="group"
      >
        <Image src={card.img_url} alt={card.name} />
        <Box p="6">
          <Box display="flex" alignItems="baseline">
            <Text fontWeight="bold" textTransform="uppercase" fontSize="sm" letterSpacing="wide">
              {card.name}
            </Text>
          </Box>
            </Box>
        </Box>
    );
}

export default Mtg_Card;