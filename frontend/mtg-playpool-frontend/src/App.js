import  AllCards  from "./pages/AllCards";
import Layout from "./components/Layout";
import { Routes, Route } from 'react-router-dom';
import Homepage from "./pages/Homepage";
import Login from "./pages/Login";
import Header from "./components/Header";
import RequireAuth from "./components/RequireAuth";
import Signup from "./pages/Signup";
import DeckCards from "./pages/DeckCards";

function App() {

  return(
      <>
      <Header />
      <Routes>

        <Route path="/" element={<Layout />} >
        <Route path="/" element={<Homepage />} />
        <Route path="login" element={<Login />} />
        <Route path="signup" element={<Signup />} /> 
        </Route>

        <Route element={<RequireAuth />}>
          <Route path="allcards" element={<AllCards />} />
          <Route path="deckcards" element={<DeckCards />} />
          </Route>

      </Routes>
      </>
)}

export default App;