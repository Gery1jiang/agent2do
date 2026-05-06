class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # 存储键值对
        self.order = []  # 存储访问顺序，最近访问的在末尾
    
    def get(self, key):
        if key in self.cache:
            # 将访问的键移到末尾（表示最近使用）
            self.order.remove(key)
            self.order.append(key)
            print(f"Get {key}: {self.cache[key]} (缓存命中)")
            return self.cache[key]
        else:
            print(f"Get {key}: -1 (缓存未命中)")
            return -1
    
    def put(self, key, value):
        if key in self.cache:
            # 更新已存在的键
            self.cache[key] = value
            # 更新访问顺序
            self.order.remove(key)
            self.order.append(key)
            print(f"Put {key}={value} (更新已存在键)")
        else:
            # 插入新键
            if len(self.cache) >= self.capacity:
                # 缓存已满，移除最久未使用的键
                lru_key = self.order.pop(0)  # 移除最前面的键
                del self.cache[lru_key]
                print(f"Put {key}={value} (缓存已满，移除 {lru_key})")
            else:
                print(f"Put {key}={value} (插入新键)")
            
            self.cache[key] = value
            self.order.append(key)
    
    def display(self):
        print(f"当前缓存状态: {dict(self.cache)}")
        print(f"访问顺序: {self.order}")
        print("-" * 40)


# 演示 LRU 缓存操作
def demo_lru_cache():
    print("=== LRU 缓存演示 (容量=3) ===")
    cache = LRUCache(3)
    
    print("1. 插入键值对 (1, 1)")
    cache.put(1, 1)
    cache.display()
    
    print("2. 插入键值对 (2, 2)")
    cache.put(2, 2)
    cache.display()
    
    print("3. 插入键值对 (3, 3)")
    cache.put(3, 3)
    cache.display()
    
    print("4. 获取键 1 的值")
    result = cache.get(1)
    cache.display()
    
    print("5. 插入键值对 (4, 4) - 缓存已满，需要淘汰")
    cache.put(4, 4)
    cache.display()
    
    print("6. 获取键 2 的值 (应该未命中)")
    result = cache.get(2)
    cache.display()
    
    print("7. 获取键 3 的值")
    result = cache.get(3)
    cache.display()
    
    print("8. 插入键值对 (5, 5) - 缓存已满，需要淘汰")
    cache.put(5, 5)
    cache.display()
    
    print("9. 获取键 1 的值 (应该未命中)")
    result = cache.get(1)
    cache.display()
    
    print("10. 更新键 4 的值")
    cache.put(4, 40)
    cache.display()


if __name__ == "__main__":
    demo_lru_cache()