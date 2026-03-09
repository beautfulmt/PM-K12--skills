#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { pathToFileURL } from "node:url";

function usage() {
  return [
    "Usage:",
    '  node scripts/export-html-to-png.mjs <input.html[#hash]> <output.png> [--width 320] [--height 568] [--delay 2500] [--timeout 20000] [--full-page]',
    "",
    "Examples:",
    '  node scripts/export-html-to-png.mjs "原型/AI名师讲题-prototype.html#home" "导出PNG/home.png" --width 320 --height 568',
    '  node scripts/export-html-to-png.mjs "流程图/AI名师讲题-flow.html" "导出PNG/flow.png" --width 1400 --height 2400 --delay 4000 --full-page',
    "",
    "Notes:",
    "  --full-page is kept for CLI compatibility. In the Chrome exporter it means: set a large enough --height for the page you want to capture.",
    "  You can override the browser path with CHROME_BIN=/path/to/chrome",
  ].join("\n");
}

function expandHome(inputPath) {
  if (!inputPath.startsWith("~")) {
    return inputPath;
  }
  return path.join(os.homedir(), inputPath.slice(1));
}

function splitInput(rawInput) {
  const hashIndex = rawInput.indexOf("#");
  if (hashIndex === -1) {
    return { inputPath: rawInput, fragment: "" };
  }
  return {
    inputPath: rawInput.slice(0, hashIndex),
    fragment: rawInput.slice(hashIndex + 1),
  };
}

function parseArgs(argv) {
  if (argv.length < 2 || argv.includes("--help") || argv.includes("-h")) {
    console.error(usage());
    process.exit(argv.includes("--help") || argv.includes("-h") ? 0 : 1);
  }

  const options = {
    input: argv[0],
    output: argv[1],
    width: 320,
    height: 568,
    delayMs: 2500,
    timeoutMs: 20000,
  };

  let index = 2;
  while (index < argv.length) {
    const flag = argv[index];
    switch (flag) {
      case "--width":
        index += 1;
        options.width = Number.parseInt(argv[index], 10);
        break;
      case "--height":
        index += 1;
        options.height = Number.parseInt(argv[index], 10);
        break;
      case "--delay":
        index += 1;
        options.delayMs = Number.parseInt(argv[index], 10);
        break;
      case "--timeout":
        index += 1;
        options.timeoutMs = Number.parseInt(argv[index], 10);
        break;
      case "--full-page":
        break;
      default:
        console.error(`Unknown argument: ${flag}\n\n${usage()}`);
        process.exit(1);
    }
    index += 1;
  }

  if (!Number.isInteger(options.width) || options.width <= 0) {
    throw new Error("Invalid value for --width");
  }
  if (!Number.isInteger(options.height) || options.height <= 0) {
    throw new Error("Invalid value for --height");
  }
  if (!Number.isInteger(options.delayMs) || options.delayMs < 0) {
    throw new Error("Invalid value for --delay");
  }
  if (!Number.isInteger(options.timeoutMs) || options.timeoutMs <= 0) {
    throw new Error("Invalid value for --timeout");
  }

  return options;
}

function resolveChromeBinary() {
  const candidates = [
    process.env.CHROME_BIN,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Arc.app/Contents/MacOS/Arc",
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }

  throw new Error(
    "No supported browser binary was found. Install Chrome/Chromium or set CHROME_BIN."
  );
}

function buildFileUrl(rawInput) {
  const { inputPath, fragment } = splitInput(rawInput);
  const absolutePath = path.resolve(process.cwd(), expandHome(inputPath));
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`Input file not found: ${inputPath}`);
  }

  const fileUrl = pathToFileURL(absolutePath);
  if (fragment) {
    fileUrl.hash = fragment;
  }
  return fileUrl.toString();
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForScreenshot(outputPath, timeoutMs, childState) {
  const startedAt = Date.now();
  let lastSize = -1;
  let stableCount = 0;

  while (Date.now() - startedAt < timeoutMs) {
    if (fs.existsSync(outputPath)) {
      const { size } = fs.statSync(outputPath);
      if (size > 0) {
        if (size === lastSize) {
          stableCount += 1;
        } else {
          stableCount = 0;
          lastSize = size;
        }
        if (stableCount >= 2) {
          return;
        }
      }
    }

    if (childState.exited && !fs.existsSync(outputPath)) {
      throw new Error(`Chrome exited before writing screenshot (code: ${childState.code ?? "unknown"})`);
    }

    await sleep(200);
  }

  throw new Error("Timed out while waiting for the screenshot file");
}

function killProcessTree(pid) {
  if (!pid) {
    return;
  }

  try {
    process.kill(-pid, "SIGKILL");
  } catch {}

  try {
    process.kill(pid, "SIGKILL");
  } catch {}
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const chromeBinary = resolveChromeBinary();
  const fileUrl = buildFileUrl(options.input);
  const outputPath = path.resolve(process.cwd(), expandHome(options.output));
  const profileDir = fs.mkdtempSync(path.join(os.tmpdir(), "codex-chrome-profile-"));

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.rmSync(outputPath, { force: true });

  const chromeArgs = [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--disable-background-networking",
    "--disable-component-update",
    "--disable-default-apps",
    "--disable-sync",
    "--disable-breakpad",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${profileDir}`,
    `--window-size=${options.width},${options.height}`,
    `--virtual-time-budget=${options.delayMs}`,
    `--screenshot=${outputPath}`,
    fileUrl,
  ];

  const child = spawn(chromeBinary, chromeArgs, {
    detached: true,
    stdio: "ignore",
  });

  const childState = { exited: false, code: null };
  child.on("exit", (code) => {
    childState.exited = true;
    childState.code = code;
  });

  try {
    await waitForScreenshot(outputPath, options.timeoutMs, childState);
    console.log(`Saved PNG to ${outputPath}`);
  } finally {
    killProcessTree(child.pid);
    fs.rmSync(profileDir, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
