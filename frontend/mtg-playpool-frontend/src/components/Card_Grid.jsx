import React, { useState, useEffect, useCallback } from "react";
import { SimpleGrid, Box, useColorModeValue, Center, Spinner, Text, Switch, FormLabel } from "@chakra-ui/react";
import Mtg_Card from "./Mtg_Card";
import InfiniteScroll from 'react-infinite-scroll-component';
import Search_Menu from "./Search_Menu";
import useFetchCards from "../hooks/useFetchCards"; // Custom hook for fetching data

function Card_Grid() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isAltEndpoint, setIsAltEndpoint] = useState(false);
  const { cards, hasMore, loading, error, fetchNextPage } = useFetchCards(searchQuery, isAltEndpoint);

  const handleSearch = query => {
    setSearchQuery(query);
  };

  const toggleEndpoint = () => {
    setIsAltEndpoint(prev => !prev);
    setSearchQuery(""); // Optionally reset search query on endpoint toggle
  };

  const gridBgColor = useColorModeValue('lightParchment', 'stoneGray');
  const gridItemBgColor = useColorModeValue('manaWhite', 'manaBlack');
  const loaderColor = useColorModeValue('manaBlue', 'manaGreen');
  const endMessageColor = useColorModeValue('manaGreen', 'gold');

  return (
    <>
      <Box className="search-box">
        <FormLabel htmlFor="endpoint-toggle">Use Alternative Endpoint</FormLabel>
        <Switch id="endpoint-toggle" isChecked={isAltEndpoint} onChange={toggleEndpoint} />
        <Search_Menu onSearch={handleSearch} />
      </Box>
      <InfiniteScroll
        dataLength={cards.length}
        next={fetchNextPage}
        hasMore={hasMore && !loading}
        loader={<Center my={8}><Spinner size="xl" color={loaderColor} /></Center>}
        endMessage={
          <Center py={8}>
            <Text color={endMessageColor} fontSize="lg">
              You've reached the end of the cards
            </Text>
          </Center>
        }
      >
        <SimpleGrid columns={[2, null, 3, 5]} spacing={6} p={6}>
          {cards.map(card => <Mtg_Card key={card.id} card={card} />)}
        </SimpleGrid>
      </InfiniteScroll>
      {error && <Center color="red.500">Failed to load data, please try again.</Center>}
    </>
  );
}

export default Card_Grid;
