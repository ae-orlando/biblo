# Dependencies — progressive hints

1. Store state belongs to the selected app, not a mutable module/default shared by all factories.
2. A request dependency can obtain that app-owned store; export the same callable object used by Depends.
3. Keep domain failures independent of HTTP where useful and translate them at the route boundary. The reference demonstrates one small feature package, not mandatory folder names.
