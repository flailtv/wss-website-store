
def q7():
    value = input("Enter Integer (0-99): ")
    type = input("Calculate addictive or multiplicative persistence (a or m): ")
    count = 0
    if str(type) == "m":
        while len(str(value)) > 1:
            numbers = []
            for i in str(value):
                numbers.append(i)
            value = int(numbers[0]) * int(numbers[1])
            print(f"{numbers[0]} * {numbers[1]} = {value}")
            count = count + 1
        return print(f"Multiplicative Persistence = {count}")
    elif str(type) == "a":
        while len(str(value)) > 1:
            numbers = []
            for i in str(value):
                numbers.append(i)
            value = int(numbers[0]) + int(numbers[1])
            print(f"{numbers[0]} + {numbers[1]} = {value}")
            count = count + 1
        return print(f"Addititve Persistence = {count}")

def q8():
    x = 2
    value = input("Input Integer: ")
    if int(value) <= 1:
        return print("Not Greater Than One")
    else:
        while int(value) > int(x):
            if int(value)%int(x) == 0:
                return print("Is Not Prime")
            else:
                x += 1
        return print("Is Prime")

while True:
    q8()
    select = input("Enter Another Number? y/n ")
    if select == "y":
        continue
    elif select == "n":
        break
    else:
        print("incorrect Input")