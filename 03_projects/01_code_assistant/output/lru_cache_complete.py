class LRUCache:
    """
    LRU (Least Recently Used) 缓存实现
    容量固定，当缓存满时移除最久未使用的元素
    """
    
    def __init__(self, capacity):
        """初始化 LRU 缓存
        
        Args:
            capacity (int): 缓存容量
        """
        self.capacity = capacity
        self.cache = {}  # 存储键值对
        self.order = []  # 存储访问顺序，最近访问的在末尾
    
    def get(self, key):
        """获取缓存中的值
        
        Args:
            key: 要获取的键
            
        Returns:
            键对应的值，如果不存在返回 -1
        """
        if key in self.cache:
            # 将访问的键移到列表末尾（最近使用）
            self.order.remove(key)
            self.order.append(key)
            print(f"Get {key}: {self.cache[key]} (缓存命中)")
            return self.cache[key]
        else:
            print(f"Get {key}: -1 (缓存未命中)")
            return -1
    
    def put(self, key, value):
        """放入键值对到缓存中
        
        Args:
            key: 键
            value: 值
        """
        if key in self.cache:
            # 如果键已存在，更新值并移到最近使用位置
            self.cache[key] = value
            self.order.remove(key)
            self.order.append(key)
            print(f"Put ({key}, {value}): 更新现有键")
        else:
            # 如果键不存在
            if len(self.cache) >= self.capacity:
                # 缓存已满，移除最久未使用的键
                lru_key = self.order.pop(0)  # 移除最前面的键（最久未使用）
                del self.cache[lru_key]
                print(f"Put ({key}, {value}): 缓存已满，移除键 {lru_key}")
            else:
                print(f"Put ({key}, {value}): 直接添加")
            
            # 添加新键值对
            self.cache[key] = value
            self.order.append(key)
    
    def display(self):
        """显示当前缓存状态"""
        print(f"当前缓存: {dict(self.cache)}")
        print(f"访问顺序: {self.order}")
        print("-" * 40)
    
    def size(self):
        """返回当前缓存大小"""
        return len(self.cache)
    
    def is_full(self):
        """检查缓存是否已满"""
        return len(self.cache) >= self.capacity


def demo_lru_cache():
    """演示 LRU 缓存的各种操作"""
    print("=== LRU 缓存演示 (容量=3) ===")
    cache = LRUCache(3)
    
    print("1. 初始状态:")
    cache.display()
    
    print("2. 添加键值对 (1, 10):")
    cache.put(1, 10)
    cache.display()
    
    print("3. 添加键值对 (2, 20):")
    cache.put(2, 20)
    cache.display()
    
    print("4. 添加键值对 (3, 30):")
    cache.put(3, 30)
    cache.display()
    
    print("5. 获取键 1 (会改变访问顺序):")
    cache.get(1)
    cache.display()
    
    print("6. 添加键值对 (4, 40) - 缓存已满，需要淘汰:")
    cache.put(4, 40)
    cache.display()
    
    print("7. 获取键 2 (应该未命中，因为已被淘汰):")
    cache.get(2)
    cache.display()
    
    print("8. 获取键 3 (会改变访问顺序):")
    cache.get(3)
    cache.display()
    
    print("9. 添加键值对 (5, 50) - 再次淘汰:")
    cache.put(5, 50)
    cache.display()
    
    print("10. 更新现有键 1:")
    cache.put(1, 100)
    cache.display()
    
    print("11. 获取键 1:")
    cache.get(1)
    cache.display()
    
    print("12. 缓存状态检查:")
    print(f"缓存大小: {cache.size()}")
    print(f"缓存是否已满: {cache.is_full()}")


if __name__ == "__main__":
    demo_lru_cache()