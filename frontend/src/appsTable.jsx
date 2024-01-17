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

import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";

const tableHeaderStyle = {
    fontWeight: "bold",
};

export default function AppsTable() {
    const [apps, setApps] = useState([]);
    const [page, setPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);

    function handleSortByRating(event) {
        const sortType = event.target.value;
        let sortedData = [];
        if (sortType === "ASCENDING")
            sortedData = [...apps].sort((a, b) => a.rating - b.rating);
        else sortedData = [...apps].sort((a, b) => b.rating - a.rating);
        setApps(sortedData);
    }

    function handlePagination(event, value) {
        setPage(value);
    }

    function handleSetItemsPerPage(event) {
        setItemsPerPage(event.target.value);
    }

    function getApps() {
        axios
            .get(
                `http://127.0.0.1:8080/api/apps?page=${page}&pageSize=${itemsPerPage}`
            )
            .then((res) => {
                console.log(res.data);
                setApps(res.data);
            })
            .catch((error) => console.log(error));
    }

    useEffect(() => {
        getApps();
    }, [itemsPerPage, page]);

    return (
        <Container>
            <Box sx={{ minWidth: 120, maxWidth: 60, marginBottom: "10px" }}>
                <FormControl fullWidth>
                    <InputLabel>Sort</InputLabel>
                    <Select label="Sort" onChange={handleSortByRating}>
                        <MenuItem value={"ASCENDING"}>Ascending</MenuItem>
                        <MenuItem value={"DESCENDING"}>Descending</MenuItem>
                    </Select>
                </FormControl>
            </Box>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell></TableCell>
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
                        {apps?.map((row, index) => (
                            <TableRow
                                key={row.name}
                                sx={{
                                    "&:last-child td, &:last-child th": {
                                        border: 0,
                                    },
                                }}
                            >
                                <TableCell>{index + 1}</TableCell>
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

            <Stack sx={{ marginTop: "20px", float: "right" }} spacing={2}>
                <Pagination
                    onChange={handlePagination}
                    count={20}
                    page={page}
                    color="primary"
                />
            </Stack>
            <Box
                sx={{
                    minWidth: 120,
                    maxWidth: 60,
                    marginTop: "10px",
                    float: "right",
                }}
            >
                <FormControl fullWidth>
                    <InputLabel>Size</InputLabel>
                    <Select
                        label="Items Per Page"
                        onChange={handleSetItemsPerPage}
                        defaultValue={10}
                    >
                        <MenuItem value={10}>10</MenuItem>
                        <MenuItem value={25}>25</MenuItem>
                        <MenuItem value={50}>50</MenuItem>
                        <MenuItem value={100}>100</MenuItem>
                    </Select>
                </FormControl>
            </Box>
        </Container>
    );
}
