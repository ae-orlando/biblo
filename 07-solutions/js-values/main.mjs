export function parseCount(input) {
  if (typeof input !== 'string') throw new TypeError('count must be text');
  const text = input.trim();
  if (!/^\d+$/.test(text)) throw new RangeError('count must contain only decimal digits');
  const value = Number(text);
  if (!Number.isSafeInteger(value)) throw new RangeError('count exceeds the safe integer range');
  return value;
}
