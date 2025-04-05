from functools import lru_cache

class GlobalCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._storage = {}  # 实际存储数据的字典
        return cls._instance

    @lru_cache(maxsize=1024)  # 扩大缓存大小
    def __getitem__(self, key):
        print(f"[Cache] 读取键 {key}...")
        return self._storage[key]

    def __setitem__(self, key, value):
        self._storage[key] = value
        self.__getitem__.cache_clear()  # 设置新值时清空缓存（确保一致性）

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

