import React from "react";
import { Heading, Flex, Divider, HStack, Box } from "@chakra-ui/react";
import "../styles.css";
import { Link } from "react-router-dom";


const Header = () => {
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="0.5rem"
      className="custom-header"
    >
      <Flex align="center" mr={5}>
       <HStack>
        <Heading as="h1" size="sm">MTGPlaypool</Heading>
          <Box>
          <Link to="/">Home</Link>
          </Box >
          <Divider orientation="vertical"  />
          <Box>
          <Link to="/allcards">Cards</Link>
          </Box>
          <Box>
          <Link to="/login">Login</Link>
          </Box>

          <Divider orientation="vertical" />
        </HStack>
        <Divider />
      </Flex>
    </Flex>
  );
};

export default Header;