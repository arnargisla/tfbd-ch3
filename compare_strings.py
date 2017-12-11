

def compare(a, b):
    difference = 0
    for i in range(int(len(a)/2)):
        chunk_a = a[i:i+2]
        chunk_b = b[i:i+2]
        v_a = int(chunk_a, 16)
        v_b = int(chunk_b, 16)
        difference += abs(v_a-v_b)
    return difference

if __name__ == "__main__":
    print(compare("aa", "bb"))
    print(compare("aa", "cc"))
    print(compare("aa", "aa"))
    print(compare("aabb", "aabb"))
    print(compare("aa", "11"))
    print(compare("aabb", "2211"))

