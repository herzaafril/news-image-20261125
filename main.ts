// news-image-20261125 entry (Node 22, standard library only).
//
// The entry image ships in this repository as entry.png. This program
// validates it against the gate's limits (whole PNG, at most 1 MiB, at most
// 1024 by 1024 pixels) and copies it byte for byte to the output directory.
// It reads no clock, no network and no randomness, so both grader runs write
// identical bytes.
//
// Locations: the repository is mounted read-only at /bot and the output
// directory is /output in the grader. MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// override them for a local run:
//   MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024; // 1 MiB gate limit
const MAX_DIM = 1024; // 1024 by 1024 gate limit

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = join(botDir, 'entry.png');
const dest = join(outDir, 'entry.png');

if (!existsSync(src)) {
  throw new Error(`entry.png not found at ${src}`);
}

const size = statSync(src).size;
if (size === 0) {
  throw new Error('entry.png is empty');
}
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate limit`);
}

const bytes = readFileSync(src);

// PNG magic: the first eight bytes are fixed for every PNG file.
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < PNG_MAGIC.length; i++) {
  if (bytes[i] !== PNG_MAGIC[i]) {
    throw new Error('entry.png does not start with the PNG magic bytes');
  }
}

// The IHDR chunk follows the magic: 4-byte length, "IHDR", then width and
// height as big-endian uint32 at offsets 16 and 20.
if (bytes.length < 24 || bytes.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk where a PNG must carry one');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > MAX_DIM || height > MAX_DIM) {
  throw new Error(`entry.png is ${width}x${height}, outside the 1024x1024 gate limit`);
}

copyFileSync(src, dest);

// Confirm the copy landed whole before reporting success.
const written = statSync(dest).size;
if (written !== size) {
  throw new Error(`copied entry.png is ${written} bytes, expected ${size}`);
}
console.log(`entry.png validated (${width}x${height}, ${size} bytes) and copied to ${dest}`);
