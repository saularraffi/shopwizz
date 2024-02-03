import { TableCell } from "@mui/material";
import { Typography } from "@mui/material";
import { Box } from "@mui/material";

const styles = {
    title: {
        fontWeight: "bold",
    },
    box: {
        display: "flex",
    },
};

export default function AppDetails({ app }) {
    return (
        <TableCell colSpan="5">
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
                <Box sx={styles.box}>
                    {app.pricePlans?.map((plan) => (
                        <Typography component="p">{plan},</Typography>
                    ))}
                </Box>
            </Box>
            <Box>
                <Typography sx={styles.title} component="p">
                    Problems Analysis:
                </Typography>
                {app.problems.map((problem) => (
                    <Typography component="p">{problem.overview}</Typography>
                ))}
            </Box>
        </TableCell>
    );
}
