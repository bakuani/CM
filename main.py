from gauss_seidel import *

def is_diagonally_dominant(matrix):
    n = len(matrix)
    for i in range(n):
        diag = abs(matrix[i][i])
        row_sum = sum(abs(matrix[i][j]) for j in range(n) if j != i)
        if diag <= row_sum:
            return False
    return True

def rearrange_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        max_val = abs(matrix[i][i])
        for j in range(i, n):
            current_diag = abs(matrix[j][i])
            row_sum = sum(abs(matrix[j][k]) for k in range(n) if k != i)
            if current_diag > row_sum and current_diag > max_val:
                max_row = j
                max_val = current_diag
        if max_row != i:
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
    return matrix if is_diagonally_dominant(matrix) else None

def matrix_norm(matrix):
    return max(sum(abs(x) for x in row) for row in matrix)

def input_manual(n):
    while True:
        print(f"Введите матрицу коэффициентов {n}x{n}:")
        matrix = []
        for i in range(n):
            while True:
                row_input = input(f"Строка {i + 1}: ").strip().split()
                if len(row_input) != n:
                    print(f"Ожидается {n} чисел. Попробуйте снова.")
                    continue
                try:
                    row = [float(x) for x in row_input]
                    matrix.append(row)
                    break
                except ValueError:
                    print("Ошибка: вводите только числа!")
        return matrix

def input_file():
    while True:
        filename = input("Имя файла: ")
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip() != '']

            n = int(lines[0])
            if n < 1 or n > 20:
                print("Некорректная размерность в файле! Допустимо 1 ≤ n ≤ 20.")
                continue

            matrix = []
            valid_matrix = True
            for i in range(1, n + 1):
                row = list(map(float, lines[i].split()))
                if len(row) != n:
                    print(f"Неверное количество элементов в строке {i} матрицы, ожидается {n}.")
                    valid_matrix = False
                    break
                matrix.append(row)
            if not valid_matrix:
                continue

            b = list(map(float, lines[n + 1].split()))
            if len(b) != n:
                print("Неверная длина вектора b. Попробуйте снова.")
                continue

            epsilon = float(lines[n + 2])
            return n, matrix, b, epsilon

        except FileNotFoundError:
            print("Файл не найден. Попробуйте снова.")
        except Exception as e:
            print(f"Ошибка в файле: {e}. Проверьте формат данных.")

def generate_matrix(n):
    import random
    matrix = []
    for i in range(n):
        row = [random.uniform(-10, 10) for _ in range(n)]
        row[i] += 100
        matrix.append(row)
    return matrix

def get_input():
    while True:
        choice = input("Способ ввода (1-ручной, 2-файл, 3-генерация): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Неверный выбор. Попробуйте снова.")

    if choice == '1':
        while True:
            try:
                n = int(input("Введите размерность матрицы (n <= 20): "))
                if 1 <= n <= 20:
                    break
                else:
                    print("Некорректная размерность! Допустимо 1 ≤ n ≤ 20.")
            except ValueError:
                print("Ошибка: введите корректное число для размерности.")

        matrix = input_manual(n)

        while True:
            try:
                b = list(map(float, input("Введите вектор правых частей через пробел: ").split()))
                if len(b) != n:
                    print(f"Ожидается {n} чисел. Попробуйте снова.")
                else:
                    break
            except ValueError:
                print("Ошибка: вводите только числа для вектора правых частей.")

        while True:
            try:
                epsilon = float(input("Точность (ε): ").replace(',', '.'))
                break
            except ValueError:
                print("Ошибка: введите корректное число для точности.")

    elif choice == '2':
        n, matrix, b, epsilon = input_file()

    elif choice == '3':
        while True:
            try:
                n = int(input("Введите размерность матрицы (n <= 20): "))
                if 1 <= n <= 20:
                    break
                else:
                    print("Некорректная размерность! Допустимо 1 ≤ n ≤ 20.")
            except ValueError:
                print("Ошибка: введите корректное число для размерности.")

        matrix = generate_matrix(n)

        while True:
            try:
                b = list(map(float, input("Введите вектор правых частей через пробел: ").split()))
                if len(b) != n:
                    print(f"Ожидается {n} чисел. Попробуйте снова.")
                else:
                    break
            except ValueError:
                print("Ошибка: вводите только числа для вектора правых частей.")

        while True:
            try:
                epsilon = float(input("Точность (ε): "))
                break
            except ValueError:
                print("Ошибка: введите корректное число для точности.")

    return matrix, b, epsilon, choice

def main():
    while True:
        matrix, b, epsilon, choice = get_input()
        original_matrix = [row.copy() for row in matrix]

        if choice in ['2', '3']:
            print("\nИсходная матрица:")
            for row in original_matrix:
                print("[", end="")
                print(", ".join(f"{num:8.2f}" for num in row), end="")
                print("]")

        if not is_diagonally_dominant(matrix):
            print("Попытка перестановки строк для достижения диагонального преобладания...")
            adjusted_matrix = rearrange_matrix(matrix)
            if adjusted_matrix is None:
                print("Диагональное преобладание недостижимо!")
                continue
            matrix = adjusted_matrix

        norm = matrix_norm(matrix)
        x, iterations, errors = gauss_seidel(matrix, b, epsilon)

        print("\nРезультаты:")
        print(f"Норма матрицы: {norm:.4f}")
        print(f"Вектор неизвестных: {[round(val, 4) for val in x]}")
        print(f"Итераций: {iterations}")
        print(f"Погрешности: {[round(e, 6) for e in errors]}")

        if input("\nПовторить? (да/нет): ").strip().lower() != 'да':
            break

if __name__ == "__main__":
    main()
