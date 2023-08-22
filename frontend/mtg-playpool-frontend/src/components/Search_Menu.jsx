import React, { useState } from "react";
import { Input, Button, Flex } from "@chakra-ui/react";

function Search_Menu({ onSearch }) {
  const [searchInput, setSearchInput] = useState("");

  const handleSearch = () => {
    onSearch(searchInput);
  };

  return (
    <Flex align="center" justify="center" mb={6}>
      <Input
        type="text"
        placeholder="Search for cards..."
        value={searchInput}
        onChange={(e) => setSearchInput(e.target.value)}
        mr={2}
        onInput={handleSearch}
      />
      <Button colorScheme="blue" onClick={handleSearch}>
        Search
      </Button>
    </Flex>
  );
}

export default Search_Menu;
