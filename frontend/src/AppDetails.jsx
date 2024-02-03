import { TableCell } from "@mui/material";
import { Typography } from "@mui/material";
import { Box } from "@mui/material";

const styles = {
    title: {
        fontWeight: "bold",
        marginRight: "10px",
    },
    box: {
        display: "flex",
        flex: 1,
    },
    inLineList: {
        marginRight: "10px",
    },
};

export default function AppDetails({ app }) {
    return (
        <TableCell colSpan="5">
            <Box sx={{ ...styles.box, width: "100%" }}>
                <Box sx={styles.box}>
                    <Typography sx={styles.title} component="p">
                        Developer Name:
                    </Typography>
                    <Typography component="p">{app.developerName}</Typography>
                </Box>
                <Box sx={styles.box}>
                    <Typography sx={styles.title} component="p">
                        Launch Date:
                    </Typography>
                    <Typography component="p">{app.dateLaunched}</Typography>
                </Box>
                <Box sx={styles.box}>
                    <Typography sx={styles.title} component="p">
                        Price Plans:
                    </Typography>
                    <Box>
                        {app.pricePlans?.map((plan, idx) => (
                            <Typography sx={styles.inLineList} component="p">
                                {plan}
                            </Typography>
                        ))}
                    </Box>
                </Box>
            </Box>
            <Box sx={{ marginTop: "10px" }}>
                <Typography sx={styles.title} component="p">
                    Problems Analysis:
                </Typography>
                {app.problems.map((problem) => (
                    <>
                        <Box style={styles.box}>
                            <Box style={styles.box}>
                                <Typography sx={styles.title} component="p">
                                    Overview:
                                </Typography>
                                <Typography component="p">
                                    {problem.overview}
                                </Typography>
                            </Box>
                            <Box style={styles.box}>
                                <Box style={styles.box}>
                                    <Typography sx={styles.title} component="p">
                                        Severity:
                                    </Typography>
                                    <Typography component="p">
                                        {problem.severity}
                                    </Typography>
                                </Box>
                                <Box style={styles.box}>
                                    <Typography sx={styles.title} component="p">
                                        Frequency:
                                    </Typography>
                                    <Typography component="p">
                                        {Math.round(problem.frequency * 100)}%
                                    </Typography>
                                </Box>
                            </Box>
                        </Box>
                        <Box style={styles.box}>
                            <ul>
                                {problem.details.map((detail) => (
                                    <li>{detail}</li>
                                ))}
                            </ul>
                        </Box>
                    </>
                ))}
            </Box>
        </TableCell>
    );
}
