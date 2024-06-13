import tkinter as tk
from tkinter import messagebox

def evaluate_expression():
    razmer = int(razmer_entry.get())
    expression = expression_entry.get()

    if not is_prime(razmer):
        messagebox.showerror("Ошибка", "Размерность поля Галуа должна быть простым числом.")
        return

    if expression == '':
        messagebox.showerror("Ошибка", "Введите выражение.")
        return

    if not is_valid_sim(expression):
        messagebox.showerror("Ошибка", "Выражение содержит недопустимые символы.")
        return

    if not is_valid_skobs(expression):
        messagebox.showerror("Ошибка", "Количество скобок не совпадает.")
        return

    result = operators_counter(expression, razmer)

    result_label = tk.Label(window, text=f"Результат выражения: {result}")
    result_label.pack()

def is_valid_skobs(expression):
    opening_skobs = 0
    closing_skobs = 0

    for char in expression:
        if char == "(":
            opening_skobs += 1
        elif char == ")":
            closing_skobs += 1

    return opening_skobs == closing_skobs

def is_prime(a):
    if a <= 1:
        return False
    for i in range(2, int(a**0.5) + 1):
        if a % i == 0:
            return False
    return True

def is_valid_sim(a):
    valid_sim = set("0123456789+-*/^&()")
    return all(char in valid_sim for char in a)


def operators_counter(expression, razmer):
    numbers = []
    operators = []
    its_number = ""

    for char in expression:
        if char.isdigit():
            its_number += char
        else:
            if its_number:
                numbers.append(int(its_number))
                its_number = ""
            if char == "(":
                operators.append(char)
            elif char == ")":
                while operators and operators[-1] != "(":
                    add_operation(numbers, operators, razmer)
                operators.pop()
            elif char in "+-*/^":
                while operators and get_precedence(operators[-1]) >= get_precedence(char):
                    add_operation(numbers, operators, razmer)
                operators.append(char)
            elif char == "&":
                if numbers:
                    numbers[-1] = find_inverse(numbers[-1], razmer)

    if its_number:
        numbers.append(int(its_number))

    while operators:
        add_operation(numbers, operators, razmer)

    return numbers[0]

def get_precedence(operator):
    if operator in "+-":
        return 1
    elif operator in "*/":
        return 2
    elif operator == "^":
        return 3
    elif operator == "&":
        return 3
    return 0

def sum_numbers(a, b):
    razmer = int(razmer_entry.get())

    result = a + b
    result = result % razmer

    return result

def min_numbers(a, b):
    razmer = int(razmer_entry.get())

    result = a - b
    result = result % razmer

    return result

def multiply_numbers(a, b):
    razmer = int(razmer_entry.get())

    result = a * b
    result = result % razmer

    return result

def divide_numbers(a, b):
    razmer = int(razmer_entry.get())

    inverse = find_inverse(b, razmer)
    result = (a * inverse) % razmer

    return result

def find_inverse(number, razmer):
    a = number
    b = int(razmer_entry.get())
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0 % razmer

def power(a, b):
    razmer = int(razmer_entry.get())

    result = 1
    for i in range(b):
        result *= a
        result = result % razmer

    return result

def add_operation(numbers, operators, razmer):
    if len(numbers) < 2:
        return
    operator = operators.pop()
    if operator == "+":
        numbers[-2] = sum_numbers(numbers[-2], numbers[-1])
    elif operator == "-":
        numbers[-2] = min_numbers(numbers[-2], numbers[-1])
    elif operator == "*":
        numbers[-2] = multiply_numbers(numbers[-2], numbers[-1])
    elif operator == "/":
        numbers[-2] = divide_numbers(numbers[-2], numbers[-1])
    elif operator == "^":
        numbers[-2] = power(numbers[-2], numbers[-1])
    elif operator == "&":
        numbers[-1] = find_inverse(numbers[-1], razmer)
    numbers.pop()

window = tk.Tk()
window.title("Вычисления в полях Галуа")
window.geometry("400x200")
razmer_label = tk.Label(window, text="Размерность поля Галуа:")
razmer_label.pack()
razmer_entry = tk.Entry(window)
razmer_entry.pack()
expression_label = tk.Label(window, text="\nДопустимы символы: +-*/^()\n& - найти обратный элемент\n\nЧисловое выражение:")
expression_label.pack()
expression_entry = tk.Entry(window, width=35)
expression_entry.pack()
start_button = tk.Button(window, text="Вычислить", command=evaluate_expression)
start_button.pack()
window.mainloop()