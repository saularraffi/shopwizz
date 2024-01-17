const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();

app.use(cors());

const ShopifyAppSchema = mongoose.Schema({
    id: String,
    url: String,
    title: String,
    imageUrl: String,
    rating: Number,
    reviewCount: Number,
    developerName: String,
    developerLink: String,
    dateLaunched: String,
    categories: String,
    pricePlans: Object,
    reviews: Object,
});

const ShopifyApp = mongoose.model("App", ShopifyAppSchema);

app.get("/api/apps", async (req, res) => {
    const page = parseInt(req.query.page);
    const pageSize = parseInt(req.query.pageSize);

    // Calculate the start and end indexes for the requested page
    const startIndex = (page - 1) * pageSize;
    const endIndex = page * pageSize;

    const apps = await ShopifyApp.find({});
    const appsSubset = apps.slice(startIndex, endIndex);

    res.send(appsSubset);
});

const host = "0.0.0.0";
const port = parseInt(process.env.DEV_APP_PORT) || 8080;
dbConnectionString = "mongodb://localhost:27017/shopifyAppMarketplace";
dbOptions = {
    useNewUrlParser: true,
    useUnifiedTopology: true,
};

mongoose
    .connect(dbConnectionString, dbOptions)
    .then(() => {
        console.log("\n[+] MongoDB connection successfull");

        app.listen(port, host, () => {
            console.log(`\n[+] Server running at http://${host}:${port}/`);
        });
    })
    .catch((err) => {
        console.log("\n[-] MongoDB connection failed\n");
    });
