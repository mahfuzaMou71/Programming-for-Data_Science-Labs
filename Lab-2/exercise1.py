temp = int(input("Enter Temparature in Celsius:"))

if temp > 32:
    if temp > 38:
        print("it is very hot.")
    else:
        print("It is quite hot.")

else:
    print("The weather is pretty chill.")