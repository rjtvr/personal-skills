#!/usr/bin/env node
// Enforces the "keep docs in sync" rule from CLAUDE.md: every plugin listed in the
// marketplace must exist on disk with the expected files, and every plugin must have a
// row in CLAUDE.md's skill index. Run with: node .github/scripts/check-consistency.mjs

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const errors = [];

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (err) {
    errors.push(`${path}: invalid JSON — ${err.message}`);
    return null;
  }
}

const marketplace = readJson(join(root, ".claude-plugin", "marketplace.json"));
const claudeMd = readFileSync(join(root, "CLAUDE.md"), "utf8");

if (marketplace) {
  for (const entry of marketplace.plugins ?? []) {
    const { name, source } = entry;
    if (typeof source !== "string" || !source.startsWith("./")) {
      errors.push(`marketplace.json: plugin "${name}" has a non-local source; skip disk checks for it`);
      continue;
    }
    const pluginDir = join(root, source);

    if (!existsSync(pluginDir)) {
      errors.push(`marketplace.json: plugin "${name}" points at "${source}", which doesn't exist`);
      continue;
    }
    if (!existsSync(join(pluginDir, "SKILL.md"))) {
      errors.push(`${source}: missing SKILL.md`);
    }
    const pluginJsonPath = join(pluginDir, ".claude-plugin", "plugin.json");
    if (!existsSync(pluginJsonPath)) {
      errors.push(`${source}: missing .claude-plugin/plugin.json`);
    } else {
      const pluginJson = readJson(pluginJsonPath);
      if (pluginJson && pluginJson.name !== name) {
        errors.push(
          `${source}: plugin.json name "${pluginJson.name}" doesn't match marketplace entry name "${name}"`
        );
      }
    }

    // Every plugin listed in the marketplace must have a row in the CLAUDE.md skill index.
    const linkedInIndex = new RegExp(`\\]\\(\\./${source.replace("./", "")}/SKILL\\.md\\)`).test(claudeMd);
    if (!linkedInIndex) {
      errors.push(`CLAUDE.md: skill index has no row linking to ${source}/SKILL.md — add one (see the "Adding a new skill" checklist)`);
    }
  }
}

// Catch the opposite drift too: a skill index row pointing at a plugin folder that no
// longer exists or isn't registered in the marketplace.
const indexRowPattern = /\]\(\.\/([^/]+)\/SKILL\.md\)/g;
const marketplaceSources = new Set((marketplace?.plugins ?? []).map((p) => p.source.replace("./", "")));
for (const match of claudeMd.matchAll(indexRowPattern)) {
  const skillDir = match[1];
  if (!existsSync(join(root, skillDir, "SKILL.md"))) {
    errors.push(`CLAUDE.md: skill index links to ${skillDir}/SKILL.md, which doesn't exist`);
  }
  if (!marketplaceSources.has(skillDir)) {
    errors.push(`CLAUDE.md: skill index lists "${skillDir}", which isn't registered in .claude-plugin/marketplace.json`);
  }
}

if (errors.length > 0) {
  console.error(`Found ${errors.length} consistency issue(s):\n`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

console.log("Marketplace, plugin folders, and CLAUDE.md skill index are consistent.");
