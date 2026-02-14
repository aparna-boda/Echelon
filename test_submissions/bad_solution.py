# two sum
def ts(n, t):
    for i in range(len(n)):
        for j in range(len(n)):
            if i != j:
                if n[i] + n[j] == t:
                    return [i, j]
