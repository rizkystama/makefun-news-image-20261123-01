// news-image-20261123 — entrypoint.
//
// The entry is a pre-rendered image held in this repository. This program
// copies it to /output/entry.png after checking it is exactly the approved
// render: PNG magic bytes, exactly 1024x1024, at most 1 MiB, and the pinned
// sha256 below. The copy is read back and hashed again, so the file the
// judge sees is the approved render byte for byte.
//
// Approved render: entry.png, 1024x1024 RGB, 195,685 bytes,
// sha256 90d0c3d1e574ecd48d466d26731966124a3bc993b4e15fc5b95a73ef28f46348.
// Produced by render.py in this repository (deterministic PIL; run twice,
// byte-identical). Concept A broadsheet, 29 verified Monday 23 November
// 2026 stories: COP31 Monday fallout, Merkury sinking + Kyiv toll, Kospi
// -3.31%. ChatGPT concept review 23 Nov ~18:20 WIB: GO WITH CONDITIONS
// (Concept A wins; all 8 conditions applied — see CONCEPT.md). Final
// review 23 Nov ~19:25 WIB: GO AFTER CORRECTIONS — v2 applies all 4:
// Riemann item removed (Nature report dated 20 Nov), KOSPI timeline
// 06:30 UTC, Indonesia card reframed as Monday's continuing search,
// fund corrected to ₩10.76tn (verified vs Korea JoongAng Daily).
// v3 revision (23 Nov ~17:45 WIB, from Rizky's Grok-sourced corrections,
// each verified against sources): Belgium card gains "Charleroi shut"
// (Charleroi cancelled all flights all day — europesays, Travel Tomorrow,
// QNC News, VolClaim, TravelExtra). A DATE CHECK footer clarification was
// tried and reverted: it pushed the amber row onto the sources footer.
// NHS "~700,000", Cikande wording and all map pins were verified already
// correct and left unchanged.
// Fixes after first render (parent visual check): NHS + Gaza captions
// shortened to fit their cards, Lowy chart numbers moved clear of the
// bars, lead-3 body trimmed so the Nasdaq figure appears once (card 15).
// 300px thumbnail checked: masthead, date, 3 leads and newspaper character
// survive at 300px (same standard as the 20261121/20261122 PASS results).
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "entry.png");

const EXPECTED_SHA256 =
  "90d0c3d1e574ecd48d466d26731966124a3bc993b4e15fc5b95a73ef28f46348";

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
