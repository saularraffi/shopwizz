import { useState, useEffect } from "react";
import axios from "axios";

export default function AppsTable() {
    const [apps, setApps] = useState({});

    function getApps() {
        axios
            .get("http://localhost:3000/_default")
            .then((res) => setApps(res.data))
            .catch((error) => console.log(error));
    }

    useEffect(() => {
        getApps();
    }, []);

    return <h1>Apps Table</h1>;
}
