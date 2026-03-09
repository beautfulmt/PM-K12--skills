#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

function usage() {
  return [
    "Usage:",
    '  node scripts/export-prototype-pngs.mjs <prototype.html> [output-dir] [--delay 2500]',
    "",
    "Examples:",
    '  node scripts/export-prototype-pngs.mjs "原型/AI名师讲题-prototype.html"',
    '  node scripts/export-prototype-pngs.mjs "原型/AI名师讲题-prototype.html" "导出PNG/AI名师讲题" --delay 3000',
  ].join("\n");
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
  console.log(usage());
  process.exit(args.length === 0 ? 1 : 0);
}

const prototypePath = path.resolve(process.cwd(), args[0]);
const secondArg = args[1];
const hasCustomOutput = secondArg && !secondArg.startsWith("--");
const outputDir = path.resolve(
  process.cwd(),
  hasCustomOutput
    ? secondArg
    : path.join(
        "导出PNG",
        path.basename(prototypePath, path.extname(prototypePath)).replace(/-prototype$/, "")
      )
);
const forwardArgs = args.slice(hasCustomOutput ? 2 : 1);

if (!fs.existsSync(prototypePath)) {
  console.error(`Prototype file not found: ${args[0]}`);
  process.exit(1);
}

const html = fs.readFileSync(prototypePath, "utf8");
const deviceTagPattern = /<div\b([^>]*\bclass="[^"]*\bdevice\b[^"]*"[^>]*)>/g;
const ids = [];

for (const match of html.matchAll(deviceTagPattern)) {
  const attrs = match[1];
  const idMatch = attrs.match(/\bid="([^"]+)"/);
  if (idMatch) {
    ids.push(idMatch[1]);
  }
}

const uniqueIds = [...new Set(ids)];
if (uniqueIds.length === 0) {
  console.error("No .device views with id attributes were found in the prototype file.");
  process.exit(1);
}

fs.mkdirSync(outputDir, { recursive: true });

const scriptPath = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "export-html-to-png.sh"
);

for (const viewId of uniqueIds) {
  const outputPath = path.join(outputDir, `${viewId}.png`);
  const result = spawnSync(
    "zsh",
    [
      scriptPath,
      `${prototypePath}#${viewId}`,
      outputPath,
      "--width",
      "320",
      "--height",
      "568",
      ...forwardArgs,
    ],
    { stdio: "inherit" }
  );

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

console.log(`Exported ${uniqueIds.length} prototype PNG files to ${outputDir}`);
