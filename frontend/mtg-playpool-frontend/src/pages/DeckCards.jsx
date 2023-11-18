import DeckCard_Grid from "../components/DeckCard_Grid";
import ActiveDeckProvider from "../context/ActiveDeckProvider";

const DeckCards = () => {

    return(
        <>
        <ActiveDeckProvider>
        <section>
        <DeckCard_Grid />
        </section>)
        </ActiveDeckProvider>
        </>
        )
    };

export default DeckCards;