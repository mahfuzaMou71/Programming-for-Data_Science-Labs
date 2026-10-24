students = [
    [201, "Amina", [78, 85, 90]],
    [202, "Rahim", [65, 70, 68]],
    [203, "Nadia", [92, 88, 95]],
    [204, "Hasan", [55, 60, 65]],
    [205, "Tania", [80, 80, 80]]
]


def calculate_average(marks):
    if len(marks) == 0:
        raise ValueError("no marks recorded")
    for mark in marks:
        if mark < 0 or mark > 100:
            raise ValueError(f"invalid mark {mark} (must be 0-100)")
    return sum(marks) / len(marks)


def classify_performance(average):
    if average >= 80:
        return "Excellent"
    elif average >= 70:
        return "Good"
    elif average >= 60:
        return "Satisfactory"
    else:
        return "Needs Improvement"


def display_report(students):
    if len(students) == 0:
        print("No student records to display.")
        return
    for student in students:
        student_id, name, marks = student
        try:
            average = calculate_average(marks)
        except ValueError as error:
            print(f"ID: {student_id} | {name} | SKIPPED: {error}")
            continue
        category = classify_performance(average)
        print(f"ID: {student_id} | {name} | Average: {average:.2f} | {category}")


print("=== Sample data ===")
display_report(students)

print("\n=== Test 1: equal marks ===")
display_report([[301, "Equal", [70, 70, 70]]])

print("\n=== Test 2: tied averages ===")
display_report([[302, "Tie A", [60, 80, 70]],
                [303, "Tie B", [70, 70, 70]]])

print("\n=== Test 3: invalid mark ===")
display_report([[304, "Bad", [85, 120, 90]],
                [305, "Neg", [-5, 50, 60]]])

print("\n=== Test 4: no marks ===")
display_report([[306, "Empty", []]])
