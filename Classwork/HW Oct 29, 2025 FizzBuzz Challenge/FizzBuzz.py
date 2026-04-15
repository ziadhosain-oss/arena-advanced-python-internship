start = 1
end = 15

count = start
while count <= end:
    if count % 3 == 0 and count % 4 == 0:
        print("FizzBuzz")
    elif count % 3 == 0:
        print("Fizz")
    elif count % 4 == 0:
        print("Buzz")
    else:
        print(count)
    count = count + 1  