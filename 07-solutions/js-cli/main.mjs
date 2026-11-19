import { readFile } from 'node:fs/promises';
const args = process.argv.slice(2);
const usage = 'usage: node main.mjs FILE.json | --help';
if (args.length === 1 && args[0] === '--help') {
  console.log(usage);
} else if (args.length !== 1 || args[0].startsWith('--')) {
  console.error(usage);
  process.exitCode = 2;
} else {
  try {
    const records = JSON.parse(await readFile(args[0], 'utf8'));
    if (!Array.isArray(records)) throw new TypeError('expected an array');
    let total = 0;
    for (const record of records) {
      if (!record || typeof record.label !== 'string' || !record.label.trim() || typeof record.value !== 'number' || !Number.isFinite(record.value)) throw new TypeError('invalid record');
      total += record.value;
      if (!Number.isFinite(total)) throw new RangeError('total overflow');
    }
    console.log(JSON.stringify({ count: records.length, total }));
  } catch (error) {
    console.error(error.code === 'ENOENT' ? 'input file not found (ENOENT)' : error.message);
    process.exitCode = 1;
  }
}
