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
    const [visibleApps, setVisibleApps] = useState([]);
    const [marketplaceData, setMarketplaceData] = useState({});
    const [page, setPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [selectedSortType, setSelectedSortType] = useState(null);
    const [selectedRating, setSelectedRating] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState(null);

    const numberOfApps = marketplaceData?.numberOfApps || 0;
    const categories = marketplaceData?.categories;
    const numberOfPages = Math.ceil(numberOfApps / itemsPerPage);

    function getSortedApps(appsList) {
        switch (selectedSortType) {
            case "RFI-DESCENDING":
                return [...appsList].sort((a, b) => b.rfiScore - a.rfiScore);
            case "RFI-ASCENDING":
                return [...appsList].sort((a, b) => a.rfiScore - b.rfiScore);
            case "RATING-DESCENDING":
                return [...appsList].sort((a, b) => b.rating - a.rating);
            case "RATING-ASCENDING":
                return [...appsList].sort((a, b) => a.rating - b.rating);
        }
        return appsList;
    }

    function filterByCategory(appsList) {
        let filtered = [];

        if (selectedCategory === "None" || !selectedCategory) {
            filtered = appsList.filter(() => true);
        } else {
            filtered = appsList.filter((app) =>
                app.categories.includes(selectedCategory)
            );
        }
        return filtered;
    }

    function filterByRating(appsList) {
        let filtered = [];

        if (selectedRating == 0 || !selectedRating) {
            filtered = appsList.filter(() => true);
        } else {
            filtered = appsList.filter(
                (app) =>
                    app.rating < selectedRating + 1 &&
                    app.rating >= selectedRating
            );
        }
        return filtered;
    }

    function handleRatingSelection(event) {
        const rating = event.target.value;
        setSelectedRating(rating);
    }

    function handleCategorySelection(event) {
        const category = event.target.value;
        setSelectedCategory(category);
    }

    function handleSortTypeSelection(event) {
        const sortType = event.target.value;
        setSelectedSortType(sortType);
    }

    function handlePagination(_, value) {
        setPage(value);
    }

    function handleSetItemsPerPage(event) {
        setItemsPerPage(event.target.value);
    }

    function handleSetVisibleApps(appsList) {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = page * itemsPerPage;
        const appsSubset = appsList.slice(startIndex, endIndex);

        setVisibleApps(appsSubset);
    }

    function filterApps() {
        const filter1 = filterByRating(apps);
        const filter2 = filterByCategory(filter1);
        const filter3 = getSortedApps(filter2);

        return filter3;
    }

    function getApps() {
        axios
            .get("http://127.0.0.1:8080/api/apps?")
            .then((res) => {
                const sortedByRfi = res.data.sort(
                    (a, b) => b.rfiScore - a.rfiScore
                );

                setApps(sortedByRfi);
                handleSetVisibleApps(sortedByRfi);
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
        getMarketplaceInfo();
    }, []);

    useEffect(() => {
        const filtered = filterApps();
        handleSetVisibleApps(filtered);
    }, [
        selectedRating,
        selectedCategory,
        selectedSortType,
        page,
        itemsPerPage,
    ]);

    return (
        <Container sx={{ marginBottom: "100px" }}>
            <Box
                sx={{
                    minWidth: 150,
                    marginRight: "10px",
                    marginBottom: "10px",
                    float: "left",
                }}
            >
                <FormControl fullWidth>
                    <InputLabel>Sort By</InputLabel>
                    <Select
                        label="Sort By"
                        onChange={handleSortTypeSelection}
                        value={selectedSortType}
                    >
                        <MenuItem value={"RFI-DESCENDING"}>
                            RFI Score - High to Low
                        </MenuItem>
                        <MenuItem value={"RFI-ASCENDING"}>
                            RFI Score - Low to High
                        </MenuItem>
                        <MenuItem value={"RATING-DESCENDING"}>
                            Rating - High to Low
                        </MenuItem>
                        <MenuItem value={"RATING-ASCENDING"}>
                            Rating - Low to High
                        </MenuItem>
                    </Select>
                </FormControl>
            </Box>

            <Box
                sx={{
                    minWidth: 175,
                    maxWidth: 60,
                    marginRight: "10px",
                    marginBottom: "10px",
                    float: "left",
                }}
            >
                <FormControl fullWidth>
                    <InputLabel>Rating Filter</InputLabel>
                    <Select
                        label="Rating Filter"
                        onChange={handleRatingSelection}
                        value={selectedRating}
                    >
                        <MenuItem value={0}>None</MenuItem>
                        <MenuItem value={1}>
                            1.0 <StarIcon sx={{ color: "#EAD419" }} />
                        </MenuItem>
                        <MenuItem value={2}>
                            2.0
                            {Array.from(Array(2), (e, i) => (
                                <StarIcon key={i} sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
                        <MenuItem value={3}>
                            3.0
                            {Array.from(Array(3), (e, i) => (
                                <StarIcon key={i} sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
                        <MenuItem value={4}>
                            4.0
                            {Array.from(Array(4), (e, i) => (
                                <StarIcon key={i} sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
                        <MenuItem value={5}>
                            5.0
                            {Array.from(Array(5), (e, i) => (
                                <StarIcon key={i} sx={{ color: "#EAD419" }} />
                            ))}
                        </MenuItem>
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
                    <InputLabel>Category Filter</InputLabel>
                    <Select
                        label="Category Filter"
                        onChange={handleCategorySelection}
                        value={selectedCategory}
                    >
                        <MenuItem value="None">None</MenuItem>
                        {categories?.map((category) => (
                            <MenuItem value={category}>{category}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell style={tableHeaderStyle}>
                                RFI Score
                            </TableCell>
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
                        {visibleApps?.map((row) => (
                            <TableRow
                                key={row.name}
                                sx={{
                                    "&:last-child td, &:last-child th": {
                                        border: 0,
                                    },
                                }}
                            >
                                <TableCell>{row.rfiScore}</TableCell>
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
