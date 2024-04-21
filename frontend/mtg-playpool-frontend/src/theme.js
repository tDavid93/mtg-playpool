import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  styles: {
    global: {
      "@font-face": {
        fontFamily: "'YourFontName'",
        src: `url('/fonts/Fantasy Narratives Demo.otf') format('woff'),
              url('/fonts/Fantasy Narratives Demo.ttf') format('truetype')`,
        fontWeight: "normal",
        fontStyle: "normal",
      },
      'html, body': {
        bg: 'rgba(0, 0, 0, 0.4)', // Adjust the RGB values to the color you want
        bgImage: "url('/assets/background2.webp')", // Replace with your image path
        bgSize: 'cover',
        bgAttachment: 'fixed',
        bgBlendMode: 'overlay', // This blends the background color with the image
      },
      '.search-box': { // Custom class for the search box
        bg: "rgba(249, 241, 228, 0.9)", // Using lightParchment color with 40% opacity
        padding: '4', // Example padding
        borderRadius: 'lg',
        boxShadow: 'lg',
        position: 'sticky',
        top: '0',
        zIndex: 'sticky',
      }
    },
   
  
  },
  colors: {
    deepBlue: "#003366",
    manaWhite: "#F4F4F4",
    manaBlue: "#0077CC",
    manaBlack: "#282828",
    manaRed: "#CC0000",
    manaGreen: "#009933",
    stoneGray: "#8A8A8A",
    lightParchment: "#FFF8E7" ,
    gold: "#B59A6A",
    crimson: "#850101",
  },
  components: {
    Heading: {
      // Customizing the Heading component globally
      baseStyle: (props) => ({
        fontFamily: "YourFontName, sans-serif",
        // Other base styles
      }),
    },
    CustomHeader: {
      // This is just a sample. You can define your own styles here.
      baseStyle: {
        bg: "deepBlue",
        color: "manaWhite",
        borderBottom: "2px solid",
        borderBottomColor: "gold",
        
      },
    },
    // ... other component overrides
  },
  // You can also extend other theme keys here
});

export default theme;