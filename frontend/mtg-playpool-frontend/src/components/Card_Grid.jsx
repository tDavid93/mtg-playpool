import React, { useState, useEffect } from "react";
import { SimpleGrid, GridItem, Divider, Flex, Container } from "@chakra-ui/react";
import Mtg_Card from "./Mtg_Card";
import InfiniteScroll from 'react-infinite-scroll-component';
import Search_Menu from "./Search_Menu";

function Card_Grid() {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const [error, setError] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const fetchData = async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    setError(false);

    let url = searchQuery ? `/api/search?page=${page}&search=${searchQuery}` : `/api/cardslist?page=${page}`;
    
    try {
      let response = await fetch(url, { mode: 'cors' });
      const data = await response.json();
      
      if (searchQuery) {
        setCards(data);
        console.log(data);
      } else {
        setCards(prevItems => [...prevItems, ...data]);
        setPage(prevPage => prevPage + 1);
      }

      if (data.length === 0) {
        setHasMore(false);
      }
    } catch (e) {
      console.log(e);
      setError(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [page, searchQuery]);

  const handleSearch = query => {
    setSearchQuery(query);
    setPage(0);
    setCards([]);
    setHasMore(true);
  };

  return (
    <>
      <Divider height="5" />
      <Search_Menu onSearch={handleSearch} />
      <InfiniteScroll
        dataLength={cards.length}
        next={fetchData}
        hasMore={hasMore && !loading}
        loader={<h4>Loading...</h4>}
        endMessage={<p>End of cards</p>}
      >
        <SimpleGrid templateColumns="repeat(5, 1fr)" gap={6} overflow="auto">
          {cards.map((card) => (
            <GridItem key={card.id} overflow="auto">
              <Mtg_Card card={card} />
            </GridItem>
          ))}
        </SimpleGrid>
      </InfiniteScroll>
    </>
  );
}

export default Card_Grid;
