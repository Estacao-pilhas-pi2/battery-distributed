import sys
import random
import time

LOCKER_OPEN = "G0"
LOCKER_CLOSED = "G1"
AAA_EMPTY = "AAA0"
AAA_NEMPTY = "AAA1"
AA_EMPTY = "AA0"
AA_NEMPTY = "AA1"
V9_EMPTY = "9V0"
V9_NEMPTY = "9V1"
C_EMPTY = "C0"
C_NEMPTY = "C1"
D_EMPTY = "D0"
D_NEMPTY = "D1"
IMAGE_ANALYSE = "AI"

while True:
    option = random.randint(0, 4)

    if option == 0:
        print(IMAGE_ANALYSE, flush=True)
        print("Controller Mock:", input(), file=sys.stderr)

    if option == 1:
        print(AAA_EMPTY, flush=True)
    if option == 2:
        print(AA_EMPTY, flush=True)
    if option == 3:
        print(V9_EMPTY, flush=True)
    if option == 4:
        print(C_EMPTY, flush=True)
    if option == 5:
        print(D_NEMPTY, flush=True)

    time.sleep(50)
