typedef struct {
    void *key;
    void *value;
    WeakKeyDictionary ioloop_for_asyncio;
} WeakKeyDictionary;