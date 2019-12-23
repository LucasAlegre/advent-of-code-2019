
def fft1(inp, phases=100):
    n = len(inp)
    p = (0,1,0,-1)
    for _ in range(phases):
        new_list = []
        for k in range(n):
            new_list.append(abs(sum( p[(i+1)//(k+1)%4] * inp[i] for i in range(n)) ) % 10)
        inp = new_list
    return inp

if __name__ == '__main__':

    with open('day16.txt') as f:
        str_inp = f.read().strip()
        inp = [int(x) for x in str_inp]
    
    # Part 1
    final_list = fft1(inp, phases=100)
    print(''.join([str(x) for x in final_list[:8]]))

    # Part 2
    offset = int(str_inp[:7])
    inp = (10000*inp)[offset:]
    for _ in range(100):
        for i in range(len(inp)-1, 0, -1): # need to do calculations from the end!!! that's the key idea!
            inp[i-1] = (inp[i-1]+inp[i]) % 10
    print(''.join(str(x) for x in inp[:8]))