export function summarizeOrders(orders) {
  if (!Array.isArray(orders)) throw new TypeError('orders must be an array');
  const seen = new Set();
  const users = new Map();
  for (const order of orders) {
    if (!order || typeof order !== 'object' || Array.isArray(order) ||
        typeof order.id !== 'string' || !order.id.trim() ||
        typeof order.user !== 'string' || !order.user.trim() ||
        !Number.isSafeInteger(order.cents) || order.cents < 0 ||
        !['paid', 'cancelled'].includes(order.status)) throw new TypeError('invalid order');
    if (seen.has(order.id)) throw new Error('duplicate order ID');
    seen.add(order.id);
    if (order.status === 'cancelled') continue;
    const previous = users.get(order.user) ?? { user: order.user, count: 0, cents: 0 };
    const cents = previous.cents + order.cents;
    if (!Number.isSafeInteger(cents)) throw new RangeError('total overflow');
    users.set(order.user, { user: order.user, count: previous.count + 1, cents });
  }
  return [...users.values()].sort((a, b) => a.user < b.user ? -1 : a.user > b.user ? 1 : 0);
}
