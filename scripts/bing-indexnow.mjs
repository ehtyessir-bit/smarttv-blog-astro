#!/usr/bin/env node
/**
 * Soumet automatiquement tous les articles à Bing IndexNow après chaque build.
 * Déclenché via le script postbuild dans package.json.
 */
import { readdir } from "fs/promises";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const INDEXNOW_KEY = "bf1b23cb7a984e8e9fb3bb240748db92";
const HOST         = "blog.smarttv.one";
const KEY_LOCATION = `https://${HOST}/${INDEXNOW_KEY}.txt`;
const API_URL      = "https://api.indexnow.org/indexnow";

async function getArticleUrls() {
  const blogDir = join(__dirname, "../src/content/blog");
  const files   = await readdir(blogDir);
  return files
    .filter(f => f.endsWith(".md") || f.endsWith(".mdx"))
    .map(f => `https://${HOST}/blog/${f.replace(/\.(md|mdx)$/, "/")}`);
}

async function submitToBing(urls) {
  const payload = JSON.stringify({
    host:        HOST,
    key:         INDEXNOW_KEY,
    keyLocation: KEY_LOCATION,
    urlList:     urls,
  });

  const res = await fetch(API_URL, {
    method:  "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body:    payload,
  });

  return res.status;
}

async function main() {
  const urls   = await getArticleUrls();
  const status = await submitToBing(urls);

  if (status === 200 || status === 202) {
    console.log(`✅ Bing IndexNow: ${urls.length} URLs soumises (HTTP ${status})`);
  } else {
    // Ne pas faire échouer le build — la clé sera disponible au prochain deploy
    console.warn(`⚠️  Bing IndexNow: HTTP ${status} (le fichier clé sera actif après ce deploy)`);
  }
}

main().catch(err => {
  console.warn("⚠️  Bing IndexNow:", err.message);
});
