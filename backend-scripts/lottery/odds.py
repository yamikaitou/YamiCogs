import random

total = 1000000
for icons in range(3,10):
    gthree = 0
    gtwo = 0
    for j in range(100):
        three = 0
        two = 0
        for k in range(total):
            num1 = random.randrange(0,icons)
            num2 = random.randrange(0,icons)
            num3 = random.randrange(0,icons)

            if num1 == num2 and num1 == num3:
                three += 1
            elif num1 == num2 or num1 == num3 or num2 == num3:
                two += 1
        #print(f"Round {j} | Icons: {icons} | Two: {round(two/total*100,2)}% | Three: {round(three/total*100,2)}%")
        gtwo += two
        gthree += three
    print(f"Final | Icons: {icons} | Two: {round(gtwo/(total*100)*100,2)}% | Three: {round(gthree/(total*100)*100,2)}%")