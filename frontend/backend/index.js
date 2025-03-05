const functions = require("firebase-functions");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Sample API endpoint
app.get("/api/hello", (req, res) => {
    res.json({ message: "Backend is working!" });
});

exports.app = functions.https.onRequest(app);
