import React, { useState, useEffect, useRef } from "react";
import { SimpleGrid, GridItem, Divider } from "@chakra-ui/react";
import Mtg_Card from "./Mtg_Card";
import InfiniteScroll from 'react-infinite-scroll-component';


function Card_Grid() {
  const [cards, setCards] = useState([]);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const observerTarget = useRef(null);


  const fetchData = async () => {
    setLoading(true);
    setError(false);  
    
    try {
        let response = await fetch('/api/cardslist?page='+page, { mode: 'cors' });
        const data = await response.json();
        setCards(prevItems => [...prevItems, ...data]);
        setPage(page+1); // Update the state once the data is fetched and parsed
      } catch (e) {
        console.log(e);
        setError(e);
      }finally {
        setLoading(false);
      }

    };



  useEffect(() => {
    fetchData();
  }, []);

  return (<>
  <Divider height="5"></Divider>
    <InfiniteScroll
    dataLength={cards.length}
    next={fetchData}
    hasMore={true}
    loader={<h4>Loading...</h4>}
    endMessage={<p>End of cards</p>}>
    <SimpleGrid templateColumns="repeat(5, 1fr)" gap={6}>
      {cards.map((card) => (
        <GridItem key={card.id} >
          <Mtg_Card card={card} />
          
        </GridItem>
      ))}
    </SimpleGrid>
    </InfiniteScroll>
    </>
  );
}
  
  export default Card_Grid;