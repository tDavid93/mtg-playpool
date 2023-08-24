import React from "react";
import { Heading, Flex, Divider } from "@chakra-ui/react";
import "../styles.css";

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
        <Heading as="h1" size="sm">MTGPlaypool</Heading>
        <Divider />
      </Flex>
    </Flex>
  );
};

export default Header;