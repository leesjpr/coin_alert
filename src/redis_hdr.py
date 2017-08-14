import redis
from single_instance import SingleInstance

class RedisHandler(object):
    def __init__(self, addr, port, password=None, timeout=10):
        self.addr = addr
        self.port = port
        self.password = password
        self.timeout = timeout
        self._running = False
        self.log = SingleInstance.get('log')
        self.redis = self.connection()


    def running(self):
        return self._running


    def connection(self):
        try:
            conn = redis.StrictRedis(host=self.addr, port=self.port, password=self.password, socket_timeout=self.timeout)
            self._running = True
            #self.log.info("Connection Redis host: %s port: %s" % (self.addr, self.port))
        except Exception, err:
            print str(err)
            #self.log.error("Fail Redis connection!! --> [%s]" % str(err))

        return conn


    def close(self):
        if self._running == Ture:
            self.redis.quit()
            #self.log.info("Redis Bye~")


if __name__ == "__main__":
    redis_hdr = RedisHandler("127.0.0.1", "6379", "job_searcher")
    redis_hdr.redis.set('foo', 'bar')
    redis_hdr.redis.get("foo")

