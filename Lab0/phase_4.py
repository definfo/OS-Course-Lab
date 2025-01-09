def decrypt_method2(s, decrypt_map):
    """
    使用替换表反向解密
    decrypt_map: 是替换字符到原字符的映射字典
    """
    return ''.join(chr(decrypt_map.index(c) + 97) for c in s)

def decrypt_method1(s):
    """
    反向重排字符串
    """
    n = len(s)
    mid = (n + 1) // 2
    result = [''] * n
    
    # 还原偶数位置
    for i in range(mid):
        result[i*2] = s[i]
    
    # 还原奇数位置
    for i in range(n - mid):
        result[i*2 + 1] = s[mid + i]
    
    return ''.join(result)

def decrypt(s):
    """
    完整的解密过程
    """
    # 首先用method2解密
    decrypt_map = "qwertyuiopasdfghjklzxcvbnm"
    s = decrypt_method2(s, decrypt_map)
    # 然后用method1解密
    return decrypt_method1(s)

s = "isggstsvke"
print(decrypt_method1(s))
print(decrypt(s))
