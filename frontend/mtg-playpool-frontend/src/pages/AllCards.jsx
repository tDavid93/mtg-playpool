import Card_Grid from "../components/Card_Grid";
import ActiveDeckProvider from "../context/ActiveDeckProvider";

const AllCards = () => {

    return(
        <>
        <ActiveDeckProvider>
        <section>
        <Card_Grid />
        </section>)
        </ActiveDeckProvider>
        </>
        )
    };

export default AllCards;