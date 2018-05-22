a = 0
MAX = 128457
with open("corpus1.txt") as f:
    with open("hope.txt", "w") as f1:
        for line in f:
            if a > MAX * 2:
                break;
            f1.write(line)
            a += 1
