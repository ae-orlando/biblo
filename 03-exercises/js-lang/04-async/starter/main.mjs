export function latestOnly(worker) {
  throw new Error('Not implemented: independent closures, latest request wins');
}
export async function mapLimit(items, limit, worker) {
  throw new Error('Not implemented: bounded workers, ordered results');
}
