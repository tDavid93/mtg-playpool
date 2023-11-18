import React, { useState, useEffect, useContext } from "react";
import { SimpleGrid, GridItem, Divider, Flex, Container, Box, Button } from "@chakra-ui/react";
import Mtg_Card from "./Mtg_Card";
import InfiniteScroll from 'react-infinite-scroll-component';
import Search_Menu from "./Search_Menu";
import "../styles.css"
import useAxiosPrivate from "../hooks/useAxiosPrivate";
import { useNavigate, useLocation } from "react-router-dom";
import DeckSelector from "./Deck_Selector";
import ActiveDeckContext from "../context/ActiveDeckContext";



function DeckCard_Grid() {
   
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const [error, setError] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const axiosPrivate = useAxiosPrivate();
  const navigate = useNavigate();
  const location = useLocation();
  const [currentDeck, setCurrentDeck] = useContext(ActiveDeckContext);

  const fetchData = async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    setError(false);

    let url = `/deck/get_deck_cards` ;
    
    try {
      let response = await axiosPrivate.get( url, {params:{deck_id: currentDeck, page: page, search: searchQuery}});
      const data = await response.data;
      console.log(data);
        
        setCards(prevItems => [...prevItems, ...data]);
        setPage(prevPage => prevPage + 1);

      if (data.length === 0) {
        setHasMore(false);
      }
    } catch (e) {
      console.log(e);
      setError(e);
      
      navigate('/login', { state: { from: location }, replace: true });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [searchQuery, currentDeck]);

  const handleSearch = query => {
    setSearchQuery(query);
    setPage(0);
    setCards([]);
    setHasMore(true);
  };

  const handleDeckSelect = deck => {
    setCurrentDeck(deck);
    console.log(currentDeck);
  };

  return (
    <>
      <Button onClick={fetchData}>Fetch Data</Button>
      <Box className="search-box" backdropBlur="md" position="center" top="0" zIndex="sticky" left="50%" >
      <Search_Menu onSearch={handleSearch} />
      <Divider height="1" />
      </Box>
      <DeckSelector onDeckSelect={handleDeckSelect}/>
      <InfiniteScroll
        dataLength={cards.length}
        next={fetchData}
        hasMore={hasMore && !loading}
        loader={<h4>Loading...</h4>}
        endMessage={<p>End of cards</p>}
      >
        
        <SimpleGrid className="custom-card-grid" templateColumns="repeat(5, 1fr)" gap={6} overflow="inherit">
          {cards.map((card) => (
            <GridItem key={card.id} overflow="auto">
              <Mtg_Card card={card} currentDeck={currentDeck}/>
            </GridItem>
          ))}
        </SimpleGrid>
       
      </InfiniteScroll>
    </>
  );
}

export default DeckCard_Grid;
