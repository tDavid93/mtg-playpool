import { useContext, useState } from "react";
import ActiveDeckContext from "../context/ActiveDeckContext";
import useAuth from "../hooks/useAuth";

const ActiveDeckProvider = ({ children }) => {
    const [activeDeck, setActiveDeck] = useState(-1);

    return (
        <ActiveDeckContext.Provider value={[ activeDeck, setActiveDeck ]}>
            {children}
        </ActiveDeckContext.Provider>
    )
}


export default ActiveDeckProvider;



