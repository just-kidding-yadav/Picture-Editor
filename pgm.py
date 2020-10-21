# name: File path of the pgm image file
# Output is a 2D list of integers
def readpgm(name):
        image = []
        with open(name) as f:
                lines = list(f.readlines())
                if len(lines) < 3:
                        print("Wrong Image Format\n")
                        exit(0)

                count = 0
                width = 0
                height = 0
                for line in lines:
                        if line[0] == '#':
                                continue

                        if count == 0:
                                if line.strip() != 'P2':
                                        print("Wrong Image Type\n")
                                        exit(0)
                                count += 1
                                continue

                        if count == 1:
                                dimensions = line.strip().split(' ')
                                print(dimensions)
                                width = dimensions[0]
                                height = dimensions[1]
                                count += 1
                                continue

                        if count == 2:  
                                allowable_max = int(line.strip())
                                if allowable_max != 255:
                                        print("Wrong max allowable value in the image\n")
                                        exit(0)
                                count += 1
                                continue

                        data = line.strip().split()
                        data = [int(d) for d in data]
                        image.append(data)
        return image    

# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
        with open(file, 'w') as fout:
                if len(img) == 0:
                        pgmHeader = 'p2\n0 0\n255\n'
                else:
                        pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
                        fout.write(pgmHeader)
                        line = ''
                        for i in img:
                                for j in i:
                                        line += str(j) + ' '
                                line += '\n'
                        fout.write(line)
