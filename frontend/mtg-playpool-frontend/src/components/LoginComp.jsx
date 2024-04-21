import React, { useState } from 'react';
import {
  VStack,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Box,
  useColorModeValue,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';
import axios from 'axios';
import UseAuth from '../hooks/useAuth';
import { useNavigate, useLocation } from 'react-router-dom';

const LoginComp = () => {
  const { setAuth } = UseAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/";
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errMsg, setErrMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrMsg(''); // Clear any existing errors
    // ...
    // Axios POST request and navigation logic here
    // ...
  };

  // Styling variables
  const bgColor = useColorModeValue('lightParchment', 'stoneGray');
  const headingColor = useColorModeValue('deepBlue', 'gold');
  const inputBgColor = useColorModeValue('manaWhite', 'manaBlack');

  return (
    <Box bg={bgColor} p={8} borderRadius="lg" boxShadow="lg" maxW="md" mx="auto" my={12}>
      <Heading color={headingColor} textAlign="center" mb={6}>
        Login
      </Heading>
      {errMsg && (
        <Alert status="error" mb={6}>
          <AlertIcon />
          {errMsg}
        </Alert>
      )}
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Username</FormLabel>
            <Input
              bg={inputBgColor}
              type="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Password</FormLabel>
            <Input
              bg={inputBgColor}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </FormControl>
          <Button type="submit" colorScheme="red" size="lg" fontSize="md" w="full">
            Login
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default LoginComp;
