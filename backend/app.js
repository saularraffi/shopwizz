const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

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
    categories: Array,
    pricePlans: Object,
    reviews: Object,
});

const ShopifyMarketplaceSchema = mongoose.Schema({
    id: String,
    numberOfApps: Number,
    categories: Array,
});

const ShopifyApp = mongoose.model("app", ShopifyAppSchema);
const ShopifyMarketplace = mongoose.model(
    "marketplacestat",
    ShopifyMarketplaceSchema
);

app.get("/api/apps", async (req, res) => {
    // const page = parseInt(req.query.page);
    // const pageSize = parseInt(req.query.pageSize);
    // const category = req.query.category;
    // const rating = req.query.rating;

    const filter = {};
    filter.problems = { $not: { $size: 0 } };
    // if (category) filter.categories = { $in: [category] };
    // if (rating) filter.rating = { $gte: rating, $lt: Number(rating) + 1 };

    // Calculate the start and end indexes for the requested page
    // const startIndex = (page - 1) * pageSize;
    // const endIndex = page * pageSize;

    const apps = await ShopifyApp.find(filter);
    // const appsSubset = apps.slice(startIndex, endIndex);

    res.send(apps);
});

app.get("/api/marketplace", async (req, res) => {
    const marketplaceInfo = await ShopifyMarketplace.findOne();
    res.send(marketplaceInfo);
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
