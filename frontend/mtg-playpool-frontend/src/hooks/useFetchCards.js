import { useState, useEffect, useCallback } from 'react';
import useAxiosPrivate from './useAxiosPrivate';

const useFetchCards = (query, isAltEndpoint) => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);

  const axiosPrivate = useAxiosPrivate();

  const fetchCards = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    setError(null);

    const endpoint = isAltEndpoint ? '/search' : '/transformer_search';
    try {
      const response = await axiosPrivate.get(endpoint, { params: { page, query } });
      const newData = response.data;

      setCards(prevCards => (page === 0 ? newData : [...prevCards, ...newData]));
      setPage(prevPage => prevPage + 1);
      setHasMore(newData.length !== 0);
    } catch (error) {
      setError(error);
      setHasMore(false);
    } finally {
      setLoading(false);
    }
  }, [axiosPrivate, query, page, isAltEndpoint, loading, hasMore]);

  useEffect(() => {
    fetchCards();
  }, [fetchCards]);

  useEffect(() => {
    setCards([]);
    setPage(0);
    setHasMore(true);
    fetchCards();
  }, [query, isAltEndpoint]);

  return { cards, loading, error, hasMore, fetchNextPage: fetchCards };
};

export default useFetchCards;
