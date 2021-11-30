import random
from pyfirmata import ArduinoMega, util

def find_all_holes(mem):
    holes = []
    start = 0
    end = 0
    inHole = False
    for i in range(len(mem)):
        if mem[i] == 0:
            if inHole:
                end = i
            else:
                start = i
                end = i
                inHole = True
        else:
            if inHole:
                holes.append([start, end, end - start + 1])
                inHole = False
    if inHole:
        holes.append([start, len(mem) - 1, len(mem) - start])
    return holes


def first_fit(mem, size):
    if size > len(mem):
        print("Unable to allocate more memory than the memory size")
        return mem
    holes = find_all_holes(mem)
    hsizes = [hole[2] - size for hole in holes]
    if all((x < 0 for x in hsizes)):
        print("Out of memory, please free memory")
        return mem
    print(hsizes)
    for hsize in hsizes:
        if hsize >= 0:
            hole_index = hsizes.index(hsize)
            break
    fill_index = holes[hole_index][1]
    for i in range(fill_index - size + 1, fill_index + 1):
        mem[i] = 1
    print("Memory allocation successful:")
    print(mem)
    return mem


def next_fit(mem, size, startingIndex):
    if size > len(mem):
        print("Unable to allocate more memory than the memory size")
        return [mem, startingIndex]
    holes = find_all_holes(mem)
    hsizes = [hole[2] - size for hole in holes]
    if all((x < 0 for x in hsizes)):
        print("Out of memory, please free memory")
        return [mem, startingIndex]
    before, after = [], []
    for hole in holes:
        if hole[0] >= startingIndex:
            after.append(hole)
        else:
            before.append(hole)
    bhsizes, ahsizes = [hole[2] - size for hole in before], [hole[2] - size for hole in after]
    foundAfter, foundBefore = False, False
    for ahsize in ahsizes:
        if ahsize >= 0:
            hole_index = ahsizes.index(ahsize)
            foundAfter = True
            break
    if foundAfter is False:
        for bhsize in bhsizes:
            if bhsize >= 0:
                hole_index = bhsizes.index(bhsize)
                foundBefore = True
                break
    if foundAfter is True:
        fill_index = after[hole_index][1]
    if foundBefore is True:
        fill_index = before[hole_index][1]
    for i in range(fill_index - size + 1, fill_index + 1):
        mem[i] = 1
    print("Memory allocation successful:")
    print(mem)
    return [mem, fill_index]


def best_fit(mem, size):
    if size > len(mem):
        print("Unable to allocate more memory than the memory size")
        return mem
    holes = find_all_holes(mem)
    hsizes = [hole[2] - size for hole in holes]
    if all((x < 0 for x in hsizes)):
        print("Out of memory, please free memory")
        return mem
    hole_index = hsizes.index(min([i for i in hsizes if i >= 0]))
    fill_index = holes[hole_index][1]
    for i in range(fill_index - size + 1, fill_index + 1):
        mem[i] = 1
    print("Memory allocation successful:")
    print(mem)
    return mem


def worst_fit(mem, size):
    if size > len(mem):
        print("Unable to allocate more memory than the memory size")
        return mem
    holes = find_all_holes(mem)
    hsizes = [hole[2] - size for hole in holes]
    if all((x < 0 for x in hsizes)):
        print("Out of memory, please free memory")
        return mem
    hole_index = hsizes.index(max([i for i in hsizes if i >= 0]))
    fill_index = holes[hole_index][1]
    for i in range(fill_index - size + 1, fill_index + 1):
        mem[i] = 1
    print("Memory allocation successful:")
    print(mem)
    return mem


memory = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0]
# memory = [0 for _ in range(20)]

def randomizeArray(size, randomAmt):
    arr = [0 for i in range(size)]
    for i in range(randomAmt):
        arr[random.randint(0,size-1)] = 1
    return arr

def lightMemory(mem, pinNumbers):
    for i in range(len(mem)):
        if mem[i] == 0:
            print("Would have writtein 0 here at pin {0}".format(pinNumbers[i]))
            #board.digital[pinNumbers[i]].write(0)
        if mem[i] == 1:
            print("Would have written 1 here at pin {0}".format(pinNumbers[i]))
            #board.digital[pinNumbers[i]].write(1)

print("Is an Arduino Mega connected to the device on port ttyUSB0? (y/n)")
arduinoCheck = input()
if 'y' in arduinoCheck:
    usingArduino = True
    #board = ArduinoMega('/dev/ttyUSB0')
    memory = randomizeArray(20, 5)
    pinNumbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
else:
    print("Size for array?\n")
    memSize = int(input())
    usingArduino = False
    memory = randomizeArray(memSize, int(memSize/4))
    print(memory)

startingIndex = 0
while (True):
    stringInput = '''
Memory is Currently: {mem}
Pick An Option:
  1. First
  2. Next
  3. Best
  4. Worst
  5. Reset
  6. Randomize
  7. Quit
'''
    print(stringInput.format(mem=memory))
    selection = int(input())
    if selection == 1:
        print("Select Size for Memory:\n")
        size = int(input())
        memory = first_fit(memory, size)
        if usingArduino is True:
            lightMemory(memory, pinNumbers)
    if selection == 2:
        print("Current starting index is {0}".format(startingIndex))
        print("Select Size for Memory:\n")
        size = int(input())
        returnVal = next_fit(memory, size, startingIndex)
        memory = returnVal[0]
        startingIndex = returnVal[1]
    if selection == 3:
        print("Select Size for Memory:\n")
        size = int(input())
        memory = best_fit(memory, size)
        if usingArduino is True:
            lightMemory(memory, pinNumbers)
    if selection == 4:
        print("Select Size for Memory:\n")
        size = int(input())
        memory = worst_fit(memory, size)
        if usingArduino is True:
            lightMemory(memory, pinNumbers)
    if selection == 5:
        memory = [0 for i in range(memSize)]
    if selection == 6:
        print("Max random 1s?")
        max = int(input())
        if max > memSize:
            print("Too big, defaulting to memSize / 4")
            memory = randomizeArray(memSize, int(memSize / 4))
        else:
            memory = randomizeArray(memSize, max)
    if selection == 7:
        break
