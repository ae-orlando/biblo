export function latestOnly(worker) {
  let latest = 0;
  return async (...args) => {
    const mine = ++latest;
    try {
      const value = await worker(...args);
      return mine === latest ? { applied: true, value } : { applied: false };
    } catch (error) {
      if (mine !== latest) return { applied: false };
      throw error;
    }
  };
}

export async function mapLimit(items, limit, worker) {
  if (!Array.isArray(items) || !Number.isInteger(limit) || limit < 1 || typeof worker !== 'function') throw new TypeError('invalid mapLimit arguments');
  const results = new Array(items.length);
  let next = 0, failed = false;
  async function consume() {
    while (!failed && next < items.length) {
      const index = next++;
      try { results[index] = await worker(items[index], index); }
      catch (error) { failed = true; throw error; }
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, consume));
  return results;
}
