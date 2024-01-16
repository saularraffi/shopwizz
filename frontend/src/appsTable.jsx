import { useState, useEffect } from "react";
import axios from "axios";

import Container from "@mui/material/Container";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const tableHeaderStyle = {
    fontWeight: "bold",
};

export default function AppsTable() {
    const [apps, setApps] = useState([]);

    function handleSortByRating(descending = false) {
        let sortedData = [];
        if (descending)
            sortedData = [...apps].sort((a, b) => b.rating - a.rating);
        else sortedData = [...apps].sort((a, b) => a.rating - b.rating);
        setApps(sortedData);
    }

    function getApps() {
        axios
            .get("http://127.0.0.1:8000/test")
            .then((res) => {
                console.log(res.data);
                setApps(res.data);
            })
            .catch((error) => console.log(error));
    }

    useEffect(() => {
        getApps();
    }, []);

    return (
        <Container>
            <button onClick={() => handleSortByRating(false)}>Sort</button>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell style={tableHeaderStyle}>
                                Image
                            </TableCell>
                            <TableCell style={tableHeaderStyle} align="right">
                                Title
                            </TableCell>
                            <TableCell style={tableHeaderStyle} align="right">
                                Rating
                            </TableCell>
                            <TableCell style={tableHeaderStyle} align="right">
                                Review Count
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {apps?.map((row) => (
                            <TableRow
                                key={row.name}
                                sx={{
                                    "&:last-child td, &:last-child th": {
                                        border: 0,
                                    },
                                }}
                            >
                                <TableCell component="th" scope="row">
                                    <img
                                        style={{ width: "60px" }}
                                        src={row.imageUrl}
                                        alt="Italian Trulli"
                                    />
                                </TableCell>
                                <TableCell align="right">
                                    <a
                                        href={row.url}
                                        target="_blank"
                                        rel="noreferrer"
                                    >
                                        {row.title}
                                    </a>
                                </TableCell>
                                <TableCell align="right">
                                    {row.rating}
                                </TableCell>
                                <TableCell align="right">
                                    {row.reviewCount}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
}
