import { useState, useEffect } from "react";
import axios from "axios";

export default function AppsTable() {
    const [apps, setApps] = useState({});

    function getApps() {
        axios
            .get("http://127.0.0.1:8000/")
            .then((res) => console.log(res))
            .catch((error) => console.log(error));
    }

    useEffect(() => {
        getApps();
    }, []);

    return <h1>Apps Table</h1>;
}
