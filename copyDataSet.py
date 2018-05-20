a = 0
with open("corpus1.txt") as f:
    with open("hope.txt", "w") as f1:
        for line in f:
            if a > 128457:
                break;
            f1.write(line)
            a += 1
