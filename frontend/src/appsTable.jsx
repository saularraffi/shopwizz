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

import StarIcon from "@mui/icons-material/Star";

const tableHeaderStyle = {
    fontWeight: "bold",
};

export default function AppsTable() {
    const [apps, setApps] = useState([]);
    const [marketplaceData, setMarketplaceData] = useState({});
    const [page, setPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [sortType, setSortType] = useState("");
    const [selectedCategory, setSelectedCategory] = useState("");
    const [selectedRating, setSelectedRating] = useState(-1);

    const numberOfApps = marketplaceData?.numberOfApps || 0;
    const categories = marketplaceData?.categories;
    const numberOfPages = Math.ceil(numberOfApps / itemsPerPage);

    function getSortedApps(data, ascending) {
        if (ascending) return [...data].sort((a, b) => a.rating - b.rating);
        else return [...data].sort((a, b) => b.rating - a.rating);
    }

    function handleSortByRating(event) {
        const ascending = event.target.value === "ASCENDING";
        setSortType(event.target.value);
        const sortedApps = getSortedApps(apps, ascending);
        setApps(sortedApps);
    }

    function handleCategorySelection(event) {
        setSelectedCategory(event.target.value);
    }

    function handleRatingSelection(event) {
        setSelectedRating(event.target.value);
    }

    function handlePagination(event, value) {
        setPage(value);
    }

    function handleSetItemsPerPage(event) {
        setItemsPerPage(event.target.value);
    }

    function getApps() {
        const categoryQuery =
            selectedCategory !== "" && selectedCategory != "None"
                ? `&category=${selectedCategory}`
                : "";

        const ratingQuery =
            selectedRating !== -1 ? `&rating=${selectedRating}` : "";

        axios
            .get(
                `http://127.0.0.1:8080/api/apps?page=${page}&pageSize=${itemsPerPage}${categoryQuery}${ratingQuery}`
            )
            .then((res) => {
                const apps =
                    sortType === ""
                        ? res.data
                        : getSortedApps(res.data, sortType === "ASCENDING");
                setApps(apps);
            })
            .catch((error) => console.log(error));
    }

    function getMarketplaceInfo() {
        axios
            .get("http://127.0.0.1:8080/api/marketplace")
            .then((res) => setMarketplaceData(res.data))
            .catch((error) => console.log(error));
    }

    useEffect(() => {
        getApps();
    }, [itemsPerPage, page, sortType, selectedCategory, selectedRating]);

    useEffect(() => {
        getMarketplaceInfo();
    }, []);

    return (
        <Container sx={{ marginBottom: "100px" }}>
            <Box
                sx={{
                    minWidth: 120,
                    maxWidth: 60,
                    marginRight: "10px",
                    marginBottom: "10px",
                    float: "left",
                }}
            >
                <FormControl fullWidth>
                    <InputLabel>Sort</InputLabel>
                    <Select label="Sort" onChange={handleSortByRating}>
                        <MenuItem value={"ASCENDING"}>Ascending</MenuItem>
                        <MenuItem value={"DESCENDING"}>Descending</MenuItem>
                    </Select>
                </FormControl>
            </Box>

            <Box
                sx={{
                    minWidth: 300,
                    marginRight: "10px",
                    marginBottom: "10px",
                    float: "left",
                }}
            >
                <FormControl fullWidth>
                    <InputLabel>Categories</InputLabel>
                    <Select
                        label="Categories"
                        onChange={handleCategorySelection}
                    >
                        <MenuItem value="None">None</MenuItem>
                        {categories?.map((category) => (
                            <MenuItem value={category}>{category}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>

            <Box
                sx={{
                    minWidth: 120,
                    maxWidth: 60,
                    marginRight: "10px",
                    marginBottom: "10px",
                    float: "left",
                }}
            >
                <FormControl fullWidth>
                    <InputLabel>Rating</InputLabel>
                    <Select label="Rating" onChange={handleRatingSelection}>
                        <MenuItem value={-1}>None</MenuItem>
                        <MenuItem value={1}>
                            1.0 <StarIcon sx={{ color: "#EAD419" }} />
                        </MenuItem>
                        <MenuItem value={2}>
                            2.0
                            {Array.from(Array(2), (e, i) => (
                                <StarIcon sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
                        <MenuItem value={3}>
                            3.0
                            {Array.from(Array(3), (e, i) => (
                                <StarIcon sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
                        <MenuItem value={4}>
                            4.0
                            {Array.from(Array(4), (e, i) => (
                                <StarIcon sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
                        <MenuItem value={5}>
                            5.0
                            {Array.from(Array(5), (e, i) => (
                                <StarIcon sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
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

            <Box sx={{ marginTop: "20px", float: "right" }}>
                <Stack sx={{ float: "right" }} spacing={2}>
                    <Pagination
                        onChange={handlePagination}
                        count={numberOfPages}
                        page={page}
                        color="primary"
                    />
                </Stack>
                <Box
                    sx={{
                        minWidth: 120,
                        maxWidth: 60,
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
            </Box>
        </Container>
    );
}
