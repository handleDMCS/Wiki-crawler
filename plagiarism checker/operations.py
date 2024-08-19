import redis

class Operations:
    def __init__(self, host='localhost', port=6900, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def get_2grams(self, phrases):
        prev = None
        result = []
        for phrase in phrases:
            if(prev):
                key = f"{prev}:{phrase}"
                result.append(key)
            prev = phrase
        return result

    def insert(self, page_id, phrases):
        keys = self.get_2grams(phrases)
        for key in keys:
            self.client.sadd(key, page_id)

    def remove(self, page_id, phrases):
        keys = self.get_2grams(phrases)
        for key in keys:
            self.client.srem(key, page_id)

    def intersection(self, keys):
        result = self.client.sinter(*keys)
        return [item.decode('utf-8') for item in result]