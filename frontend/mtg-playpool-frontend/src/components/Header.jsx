import React from "react";
import { Flex, Heading, Box, Link, useStyleConfig, Image} from "@chakra-ui/react";
import { Link as RouterLink, useLocation } from "react-router-dom";

const Header = () => {
  const location = useLocation();

  // A function to determine if the link is active
  const isActive = (path) => location.pathname === path;


  const headingStyles = useStyleConfig("Heading");


  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      p="1rem"
      bg="deepBlue"
      color="manaWhite"
    >
       <Link as={RouterLink} to="/">
      <Flex align="center" mr={5}>
     
        <Box p={2}>
          
          <Image src="assets/logo.svg" alt="MTGPlaypool" boxSize='50px'/>
          
        </Box>
        <Heading as="h1" size="lg" fontWeight="bold"  sx={headingStyles}>
        MTGPlaypool
        </Heading>
      </Flex>
      </Link>

      <Box display={{ base: 'none', md: 'flex' }} mt={{ base: 4, md: 0 }}>
        <Link as={RouterLink} to="/" px={4} py={2} rounded={'md'}
              fontWeight={isActive('/') ? 'bold' : 'normal'}
              _hover={{ bg: 'manaBlue', color: 'manaWhite' }}>
          Home
        </Link>
        <Link as={RouterLink} to="/allcards" px={4} py={2} rounded={'md'}
              fontWeight={isActive('/allcards') ? 'bold' : 'normal'}
              _hover={{ bg: 'manaBlue', color: 'manaWhite' }}>
          Cards
        </Link>
        <Link as={RouterLink} to="/login" px={4} py={2} rounded={'md'}
              fontWeight={isActive('/login') ? 'bold' : 'normal'}
              _hover={{ bg: 'manaBlue', color: 'manaWhite' }}>
          Login
        </Link>
      </Box>

      {/* This divider might be the bottom border for the active link indicator */}
      <Box flexGrow={1} height="2px" bg="gold" my={2} />
    </Flex>
  );
};

export default Header;
