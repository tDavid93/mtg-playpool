import React, { useState } from "react";
import { Input, Button, Flex } from "@chakra-ui/react";

function Search_Menu({ onSearch }) {
  const [searchInput, setSearchInput] = useState("");

  const handleSearch = () => {
    onSearch(searchInput); // This will use the latest state value
  };

  return (
    <Flex align="center" justify="center" mb={6}>
      <Input
        type="text"
        placeholder="Search for cards..."
        value={searchInput}
        onChange={(e) => setSearchInput(e.target.value)} // Update state here
        onKeyPress={(e) => e.key === "Enter" && handleSearch()} // Handle search on Enter key
        mr={2}
      />
      <Button colorScheme="blue" onClick={handleSearch}>
        Search
      </Button>
    </Flex>
  );
}

export default Search_Menu;