import numpy as np

# Данные
data = np.array([
    [5, 1.58],
    [10, 1.95],
    [15, 2.1],
    [20, 2.34],
    [25, 2.66],
    [30, 2.98],
    [35, 3.27]
   
])


x = data[:, 0]
y = data[:, 1]
n = len(x)

# Вычисляем необходимые суммы
S_x = np.sum(x)
S_y = np.sum(y)
S_xy = np.sum(x * y)
S_xx = np.sum(x ** 2)

# Рассчитываем коэффициенты
m = (n * S_xy - S_x * S_y) / (n * S_xx - S_x ** 2)
b = (S_y - m * S_x) / n

# Вычисляем остатки
y_fit = m * x + b
S_res = np.sum((y - y_fit) ** 2)

# Погрешность наклона
sigma_m = np.sqrt(S_res / ((n - 2) * S_xx))
sigma_b = np.sqrt(sigma_m / (n * S_xx - S_x ** 2))

print(f"naklon (m): {m}")
print(f"svobodny (b): {b}")
print(f"pogr_nakl (o_m)): {sigma_m}")
print(f"pogr_nakl (o_b)): {sigma_b}")