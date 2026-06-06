#!/usr/bin/env node
/**
 * Auto-generates sitemap.xml after every Astro build.
 * Reads all HTML files from dist/ and builds a proper sitemap.
 * Triggered via postbuild script in package.json.
 */
import { readdir, writeFile, stat } from "fs/promises";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DIST_DIR  = join(__dirname, "../dist");
const SITE      = "https://blog.smarttv.one";
const TODAY     = new Date().toISOString().split("T")[0];

// Priority map by path pattern
function getPriority(url) {
  if (url === `${SITE}/`) return "1.0";
  if (url.match(/bester-iptv-anbieter|iptv-anbieter-vergleich|iptv-kaufen/)) return "0.95";
  if (url.match(/\/blog\//)) return "0.85";
  return "0.7";
}

function getChangefreq(url) {
  if (url.match(/wm-2026|bundesliga|favoriten/)) return "daily";
  if (url.match(/\/blog\//)) return "weekly";
  return "monthly";
}

async function collectUrls(dir, base = "") {
  const urls = [];
  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      const sub = await collectUrls(fullPath, `${base}/${entry.name}`);
      urls.push(...sub);
    } else if (entry.name === "index.html") {
      const urlPath = base === "" ? "/" : `${base}/`;
      urls.push(`${SITE}${urlPath}`);
    }
  }
  return urls;
}

async function main() {
  const urls = await collectUrls(DIST_DIR);
  urls.sort();

  const entries = urls.map(url => `  <url>
    <loc>${url}</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>${getChangefreq(url)}</changefreq>
    <priority>${getPriority(url)}</priority>
  </url>`).join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
    http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
${entries}
</urlset>`;

  await writeFile(join(DIST_DIR, "sitemap.xml"), xml, "utf-8");
  console.log(`✅ Sitemap: ${urls.length} URLs → dist/sitemap.xml`);
}

main().catch(err => {
  console.error("❌ Sitemap error:", err.message);
  process.exit(1);
});
