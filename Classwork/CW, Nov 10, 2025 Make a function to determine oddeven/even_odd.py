def greetings(number):
    result = number % 2 == 0  
    if result:
        print("even")         
    else:
        print("odd")
    return result              
    
num = greetings(2)
print(type(num))