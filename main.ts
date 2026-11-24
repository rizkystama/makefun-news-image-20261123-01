// news-image-20261123 — entrypoint (v4 revision).
//
// The entry is a pre-rendered image held in this repository. This program
// copies it to /output/entry.png after checking it is exactly the approved
// render: PNG magic bytes, exactly 1024x1024, at most 1 MiB, and the pinned
// sha256 below. The copy is read back and hashed again, so the file the
// judge sees is the approved render byte for byte.
//
// Approved render: entry.png, 1024x1024 RGB (v4).
// Produced by render.py in this repository (deterministic PIL; run twice,
// byte-identical). v4 revision (25 Nov ~00:00 WIB, built on Rizky's
// "Bangun v4 news-image malam ini" after R3 landed at 57.49% / rank
// 3,458): FOUR leads across — COP31 Monday fallout, Merkury sinking +
// Kyiv toll, the US Monday rebound (NEW lead: S&P +4.73% to 7,237.17,
// Nasdaq +6.51%, best day since April 2025), Kospi -3.31%. 30 verified
// Monday 23 November 2026 stories: 4 leads + 12 cards + 14 ALSO.
// v4 carries the day's resolved evening news v3 missed: the US close
// (21:00 UTC), Nvidia's board reinstating Jensen Huang as CEO (+31.48%,
// ~$950B added — new card 16), the Rubio–Qatar 8th Strategic Dialogue
// readout (card 12, upgraded from preview to outcome), the confirmed
// Kyiv toll of 15 incl. the Dymer boy rescued after 22 hours. New
// masthead nameplate ("THE MONDAY GLOBE"); DATE CHECK loses its
// "not yet decided" row (all decided now) and the world map grows
// (576x146) with reworked pin labels. Sources read through ~21:30 UTC.
// v3 (commit f8d9363, sub 01a207ff): R1 56.96% / R2 71.46% / R3 57.49%.
// 300px thumbnail checked before submit (same standard as the
// 20261121/20261122 PASS results).
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "entry.png");

const EXPECTED_SHA256 = "c31171719e878929e16407756362987389d25e564dbdb8c2cd640e8dd42859a4";

// PNG magic bytes (89 50 4E 47 0D 0A 1A 0A). The judge tells the format from
// the first bytes, so a non-PNG here would fail intake outright.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const bytes = readFileSync(SRC);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG (bad magic bytes)");
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
// IHDR width/height are big-endian uint32 at bytes 16..24. The entry must be
// exactly 1024x1024, not merely no larger than that.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, must be exactly 1024x1024`);
}
const sha256 = createHash("sha256").update(bytes).digest("hex");
if (sha256 !== EXPECTED_SHA256) {
  throw new Error(
    `entry.png sha256 ${sha256} does not match the approved render`,
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(SRC, join(outDir, "entry.png"));
const copied = statSync(join(outDir, "entry.png"));
if (copied.size !== bytes.length) {
  throw new Error("copied entry.png differs in size from the source");
}
// Read the copy back and hash it: the file the judge sees must be the
// approved render byte for byte, not just the same size.
const copiedSha = createHash("sha256")
  .update(readFileSync(join(outDir, "entry.png")))
  .digest("hex");
if (copiedSha !== EXPECTED_SHA256) {
  throw new Error(
    `copied entry.png sha256 ${copiedSha} does not match the approved render`,
  );
}
console.log(
  `entry.png ${width}x${height} ${bytes.length} bytes sha256=${sha256}`,
);
