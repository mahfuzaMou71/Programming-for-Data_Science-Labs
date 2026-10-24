base = float(input("Enter base: "))
exp = int(input("Enter exponent (non-negative integer): "))

result = 1
for _ in range(exp):
    result *= base

print(base, "^", exp, "=", result)
