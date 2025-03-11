def gauss_seidel(A, b, epsilon, max_iterations=1000):
    n = len(b)
    x_prev = [0.0] * n
    iterations = 0
    errors = []

    while iterations < max_iterations:
        x_curr = x_prev.copy()
        max_error = 0.0

        for i in range(n):
            sum_new = sum(A[i][j] * x_curr[j] for j in range(i))
            sum_old = sum(A[i][j] * x_prev[j] for j in range(i + 1, n))
            x_curr[i] = (b[i] - sum_new - sum_old) / A[i][i]

            current_error = abs(x_curr[i] - x_prev[i])
            if current_error > max_error:
                max_error = current_error

        errors.append(max_error)
        if max_error < epsilon:
            break

        x_prev = x_curr.copy()
        iterations += 1

    return x_curr, iterations, errors

