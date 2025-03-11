import matplotlib.pyplot as plt
import numpy as np

def countKoef():
    # Данные
    data = np.array([
        [1, 2],
        [2, 3],
        [3, 5],
        [4, 7],
        [5, 11]
    ])

    x = data[:, 0]
    y = data[:, 1]
    n = len(x)

    S_x = np.sum(x)
    S_y = np.sum(y)
    S_xy = np.sum(x * y)
    S_xx = np.sum(x ** 2)

    a = (n * S_xy - S_x * S_y) / (n * S_xx - S_x ** 2)
    b = (S_y - a * S_x) / n

    y_fit = a * x + b
    S_res = np.sum((y - y_fit) ** 2)

    sigma_a = np.sqrt(S_res / ((n - 2) * S_xx))
    sigma_b = np.sqrt(sigma_a / (n * S_xx - S_x ** 2))

    print(f"naklon (a): {a}")
    print(f"svobodny (b): {b}")
    print(f"pogr_nakl (sigma_a)): {sigma_a}")
    print(f"pogr_nakl (sigma_b)): {sigma_b}")
    return a, b
















# Задаем точки (x, y)
xCord = [1, 2, 3, 4, 5]
yCord = [2, 3, 5, 7, 11]

a, b = countKoef()
xApprox = np.linspace(xCord[0], xCord[len(xCord) - 1], 2) # от { } до { } (кол-во точек)
yApprox = a * xApprox + b
plt.plot(xCord, yCord, 'ro')
plt.plot(xApprox, yApprox, label=f'y = {a}x + {b}', color='blue')

#plt.legend(['First series','Second series'], loc=2)
#plt.title(f'График заданных величин')
#plt.xlabel('X', color = 'black')
#plt.ylabel('Y', color = 'black')

plt.grid(True) # сетка

plt.show()

