WIDTH = 25
HEIGHT = 6
SIZE = WIDTH * HEIGHT

if __name__ == '__main__':

    with open('day08.txt') as f:
        image = f.read().strip()
    
    # Part 1
    i = 0
    layer = None
    zero_digits = 999999999
    while i < len(image):
        s = image[i:i+SIZE]
        i += SIZE
        if s.count('0') < zero_digits:
            zero_digits = s.count('0')
            layer = s
    print(layer.count('1') * layer.count('2'))

    # Part 2
    i = 0
    layers = []
    while i < len(image):
        s = image[i:i+SIZE]
        i += SIZE
        layers.append(s)
    
    final_image = []
    for i in range(SIZE):
        for j in range(len(layers)):
            if layers[j][i] != '2':
                final_image.append(layers[j][i])
                break
    
    for i in range(0, SIZE+1, WIDTH):
        print(' '.join(final_image[i:i+WIDTH]).replace('0', ' ').replace('1', '\u2588'))
