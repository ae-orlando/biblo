# Reference: small API, explicit limits

`server.mjs` keeps state per server instance, assigns UUIDs, validates route/method/media type/body shape and bounds retained input bytes. The body reader discards excess chunks without destroying the socket before a `413` can be sent. Unknown internal errors are not exposed to the client.

The factory is tested on an ephemeral loopback port. Direct execution listens only on `127.0.0.1:3000`. There is no authentication, durable storage, production rate limiting or distributed consistency. Do not deploy it as an auth system. Mutation to catch: checking JavaScript string length instead of byte length or using timestamp IDs.

Verification: `python3 90-tools/practice.py check js-http --reference`.
