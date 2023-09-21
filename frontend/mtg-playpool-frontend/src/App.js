import  AllCards  from "./pages/AllCards";
import Layout from "./components/Layout";
import { Routes, Route } from 'react-router-dom';
import Homepage from "./pages/Homepage";
import Login from "./pages/Login";
import Header from "./components/Header";
import RequireAuth from "./components/RequireAuth";

function App() {

  return(
      <>
      <Routes>

        <Route path="/" element={<Layout />} >
        <Route path="/" element={<Homepage />} />
        <Route path="login" element={<Login />} />
        
        </Route>

        <Route element={<RequireAuth />}>
          <Route path="allcards" element={<AllCards />} />
          </Route>

      </Routes>
      </>
)}

export default App;