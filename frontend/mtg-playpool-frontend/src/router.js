import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Homepage } from "./pages/Homepage";
import { AllCards } from "./pages/AllCards";

export const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/allcards" element={<AllCards />} />
      </Routes>
    </BrowserRouter>
  );
}

export default Router;