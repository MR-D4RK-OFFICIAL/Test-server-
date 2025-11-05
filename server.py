import express from "express";
import fetch from "node-fetch";
import archiver from "archiver";
import fs from "fs";
import path from "path";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

app.get("/clone", async (req, res) => {
  try {
    const url = req.query.url;
    if (!url) return res.status(400).json({ error: "No URL provided" });

    // HTML ক্লোন করা
    const response = await fetch(url);
    const html = await response.text();

    // temp folder তৈরি
    const folder = "./temp";
    if (!fs.existsSync(folder)) fs.mkdirSync(folder);

    const filePath = path.join(folder, "index.html");
    fs.writeFileSync(filePath, html);

    // ZIP বানানো
    const zipPath = path.join(folder, "clone.zip");
    const output = fs.createWriteStream(zipPath);
    const archive = archiver("zip");
    archive.pipe(output);
    archive.file(filePath, { name: "index.html" });
    await archive.finalize();

    output.on("close", () => {
      res.download(zipPath, "website.zip");
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server Error" });
  }
});

app.get("/", (req, res) => {
  res.send("✅ Clone server is working!");
});

export default app;
