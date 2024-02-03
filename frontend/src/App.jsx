import AppsTable from "./AppsTable";
import { Container } from "@mui/material";

function App() {
    return (
        <>
            <Container sx={{ marginBottom: "20px" }}>
                <img
                    style={{ width: "350px" }}
                    src="/shopwizz_logo_full.png"
                ></img>
            </Container>
            <AppsTable />
        </>
    );
}

export default App;
