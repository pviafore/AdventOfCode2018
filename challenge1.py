import itertools

with open("input1.txt") as input_file:
    numbers = input_file.readlines()

    #part 1
    print(sum(int(n) for n in numbers))

    #part 2
    counter = 0
    seen = set([0])
    for n in itertools.cycle(numbers):
        counter += int(n)
        if counter in seen:
            print(counter)
            break

        seen.add(counter)

        

