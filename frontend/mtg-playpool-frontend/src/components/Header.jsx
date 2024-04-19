import React from "react";
import { Heading, Flex, Box, Link, useStyleConfig } from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";

const Header = () => {
  // This hook can be used if you have set up custom styles in your theme.js
  // Otherwise, you can use the style props directly in the components
  const styles = useStyleConfig("CustomHeader");

  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      p={4}
      bg="deepBlue"
      color="manaWhite"
      sx={styles} // if you're using a custom style config
    >
      <Flex align="center" mr={5}>
        <Heading as="h1" size="lg" letterSpacing={"tighter"}>
          MTGPlaypool
        </Heading>
      </Flex>

      <Box>
        <Link as={RouterLink} to="/" px={2} py={1} rounded={'md'}>
          Home
        </Link>
        <Link as={RouterLink} to="/allcards" px={2} py={1} rounded={'md'}>
          Cards
        </Link>
        <Link as={RouterLink} to="/login" px={2} py={1} rounded={'md'}>
          Login
        </Link>
      </Box>

      <Box flexGrow={1} height="2px" bg="gold" my={2} />
    </Flex>
  );
};

export default Header;