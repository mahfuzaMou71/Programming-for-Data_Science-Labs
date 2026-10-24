ch = input("Enter a character: ")

if len(ch) != 1 or not ch.isalpha():
    print("Invalid input")
elif ch.lower() in "aeiou":
    print(ch, "is a vowel")
else:
    print(ch, "is not a vowel")
