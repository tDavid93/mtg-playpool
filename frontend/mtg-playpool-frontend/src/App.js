import './App.css';
import { ChakraProvider } from '@chakra-ui/react'
import Header from './components/Header';
import Card_Grid from './components/Card_Grid';


function App() {
  return (
     <ChakraProvider>
    <div className="1App">
      </div>
      <div>
        <Header />
      </div>
      <div>
        <Card_Grid />        
      </div>
      </ChakraProvider>
  );
}

export default App;
