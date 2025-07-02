import random

def get_GCD(a: int, b: int) -> int:
    long = a if a >= b else b
    short = a if a != long else b
    for i in range(short, 0, -1):
        if a % i == 0 and b % i == 0:
            res = i
            break
    return res


def gcd(a, b):
    while(b != 0):
        t = a
        a = b
        b = t % b
    return a

lst = [[3,7], [4,16], [81, 18], [25, 200], [51, 28]]

for pair in lst:
    a = pair[0]
    b = pair[1]
    print(f"Numbers: {a}, {b}.")
    res = gcd(a, b)
    print(res)







