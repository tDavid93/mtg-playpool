import { Flex, Box, Text, Button, Image, useColorModeValue, useStyleConfig } from "@chakra-ui/react";

const Homepage = () => {
  const bgNav = useColorModeValue("deepBlue", "deepBlue");
  const bgFooter = useColorModeValue("stoneGray", "stoneGray");
  const textHero = useColorModeValue("manaWhite", "manaWhite");
  const heroBg = useColorModeValue("rgba(0, 0, 0, 0.5)", "rgba(255, 255, 255, 0.5)");
  const headingStyles = useStyleConfig("Heading");

  return (
    <Flex direction="column" align="center" justify="center">
      {/* Navigation Bar */}
      <Box bg={bgNav} w="full" p={4} color="white">
        {/* Navigation Links */}
      </Box>

      {/* Hero Section */}
      <Flex direction="column" align="center" justify="center" position="relative" h="100vh" w="full">
        {/* <Image src="assets/hero-image.webp" /> */}
        <Box position="absolute" p={9} bg={heroBg} align="center">
        <Box p={2}>
          
          <Image src="assets/logo.svg" alt="MTGPlaypool" boxSize='150px'/>
          
        </Box>
          <Text color={textHero} fontSize="2xl">Welcome to</Text>
          <Text color={textHero} fontSize="3xl" fontWeight="bold" sx={headingStyles}>MTGPlaypool</Text>
          <Text color={textHero}>Your ultimate resource for exploring Magic: The Gathering cards.</Text>
          
          <Box h={4} />
          <Button colorScheme="blue" size="lg" align="center">Search Cards</Button>
          <Box h={4} />
        </Box>

      </Flex>

    </Flex>
  );
};

export default Homepage;
