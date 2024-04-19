import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  colors: {
    deepBlue: "#003366",
    manaWhite: "#F4F4F4",
    manaBlue: "#0077CC",
    manaBlack: "#282828",
    manaRed: "#CC0000",
    manaGreen: "#009933",
    stoneGray: "#8A8A8A",
    lightParchment: "#FFF8E7",
    gold: "#B59A6A",
    crimson: "#850101",
  },
  components: {
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