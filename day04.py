def valid_password(x):

    for i in range(len(x)-1):
        if x[i] > x[i+1]:
            return False
    
    for i in range(len(x)-1):
        for i in range(len(x)-1):
            if x[i] == x[i+1]:
                if (i > 0 and x[i-1] == x[i]) or (i < len(x) - 2 and x[i+2] == x[i+1]):
                    continue
                else:
                    return True


if __name__ == '__main__':

    with open('day04.txt') as f:
        low, high = [int (x) for x in f.read().split('-')]
    
    c = 0
    for i in range(low, high+1):
        if valid_password(str(i)):
            c += 1
    
    print(c)
    