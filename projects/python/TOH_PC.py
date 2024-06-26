def HanoiTower(n):
    for i in range(1, (1 << n)):
        start = (i & i-1) % 3
        end = ((i | i-1) + 1) % 3
        print(f"Move disc {n - i.bit_length() + 1} from {['A', 'B', 'C'][start]} to {['A', 'B', 'C'][end]}")
num_discs = 4
HanoiTower(num_discs)