import React, { useContext, useRef, useEffect, useState } from 'react';
import {
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  Button,
  Radio,
  RadioGroup,
  Stack,
  Input,
  Box,
  Text,
  Spacer
} from '@chakra-ui/react';
import ActiveDeckContext from '../context/ActiveDeckContext';
import { axiosPrivate } from '../api/axios';

function DeckSelector() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const deckSelectButtonRef = useRef();
  const [Decks, setDecks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newDeckName, setNewDeckName] = useState('');
  const [newDeckDescription, setNewDeckDescription] = useState('');
  const [newDeckFormat, setNewDeckFormat] = useState('');
  const [currentDeck, setCurrentDeck] = useContext(ActiveDeckContext);
    console.log(currentDeck);
  const handleNewDeckNameChange = (e) => {
    setNewDeckName(e.target.value);
  };

  const handleNewDeckDescriptionChange = (e) => {
    setNewDeckDescription(e.target.value);
  };

  const handleNewDeckFormatChange = (e) => {
    setNewDeckFormat(e.target.value);
  };

  const handleDeckSelect = (e) => {
    setCurrentDeck(e);
  };

  const fetchDecks = async () => {
    
    if (loading) return;
    setLoading(true);
    try {
      const response = await axiosPrivate.get('/deck/get_decks');
      const data = response.data;
        console.log(data);
      setDecks(data);
    } catch (error) {
      console.error('Error fetching decks:', error);
    } finally {
      setLoading(false);
    }
  };

  const addDeck = async () => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await axiosPrivate.post('/deck/create', {
        name: newDeckName,
        description: newDeckDescription,
        format: newDeckFormat
      });
      const data = response.data;
      console.log(data);
      fetchDecks();
    } catch (error) {
      console.error('Error adding deck:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDecks();
  }, [Decks, currentDeck]);

  return (
    <>
      <Button ref={deckSelectButtonRef} colorScheme="teal" onClick={onOpen}>
        Open
      </Button>
      <Drawer
        isOpen={isOpen}
        placement="left"
        size="md"
        onClose={onClose}
        finalFocusRef={deckSelectButtonRef}
        isFullHeight={true}
        variant="primary"
        bg="#ffffff"
      >
        <DrawerOverlay />
        <DrawerContent bg="#ffffff">
          <DrawerCloseButton />
          <DrawerHeader>Select your active deck</DrawerHeader>
          <DrawerBody>
             <Button colorScheme="teal" size="sm" onClick={fetchDecks} position="right">
              Refresh
              </Button>
             <RadioGroup onChange={handleDeckSelect} value={currentDeck ? currentDeck.id : '0'}>
              <Stack spacing={4}>
                { Decks.map((deck) => (
                  <Radio key={deck.id} value={deck.id}>
                    <Text>{deck.name}</Text>
                  </Radio>
                ))}
              </Stack>
            </RadioGroup>
             <Spacer height="1.5" />
            <Box scale="50%">
              <Text>Add New Deck:</Text>
              <Stack direction="column" spacing={4} align="right">
                <Spacer />
                <Text>Deck Name:</Text>
                <Input placeholder="Deck Name" value={newDeckName} onChange={handleNewDeckNameChange} />
                <Spacer />
                <Text>Deck Description:</Text>
                <Input placeholder="Deck Description" value={newDeckDescription} onChange={handleNewDeckDescriptionChange} />
                <Spacer />
                <Text>Deck Format:</Text>
                <Input placeholder="Deck Format" value={newDeckFormat} onChange={handleNewDeckFormatChange} />
                <Spacer />
                <Button colorScheme="teal" size="sm" onClick={addDeck} position="right">
                  Add
                </Button>
              </Stack>
            </Box>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </>
  );
}

export default DeckSelector;
