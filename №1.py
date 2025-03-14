import numpy as np
import matplotlib.pyplot as plt
import math

def phys_round(value, error):
    """
    Округляет (value ± error) по "классическим" физическим правилам:
      1) Если первая значащая цифра error = 1 или 2, оставляем 2 значащие цифры,
         иначе 1.
      2) value округляем до того же разряда, на котором стоит последняя значащая
         цифра ошибки.
    Возвращает (val_str, err_str) — уже в виде строк.
    """

    if error == 0:
        # Если ошибка вдруг ноль, вернём 3 знака после запятой
        return f"{value:.3f}", "0.000"

    # 1) Определяем порядок error, чтобы перевести в "научную" форму e * 10^exponent
    abs_err = abs(error)
    exponent = math.floor(math.log10(abs_err))   # например, error=0.055 => log10(0.055) ~ -1.259 => floor=-2
    e = abs_err / 10**exponent                  # теперь e ~ 5.5

    # 2) Смотрим первую (старшую) цифру e (целую часть)
    first_digit = int(e)  # например, 5
    if first_digit in [1, 2]:
        digits = 2
    else:
        digits = 1

    # 3) Округляем e до нужного количества значащих цифр
    #    Если digits=1, round(e,0); если digits=2, round(e,1); и т.д.
    e_rounded = round(e, digits - 1)

    # 4) Если получилось >= 10, сдвигаем разряд ещё на 1
    if e_rounded >= 10:
        e_rounded /= 10
        exponent += 1

    # 5) Это будет окончательная ошибка
    err_final = e_rounded * 10**exponent

    # 6) Определяем, на каком десятичном разряде стоит последняя цифра ошибки
    exponent_final = math.floor(math.log10(err_final))  # например, если err_final=0.06 => ~ -1.22 => floor=-2
    # Учитывая количество значащих цифр digits, определяем число знаков после запятой:
    decimal_place = -exponent_final + (digits - 1)
    decimal_place = max(0, decimal_place)

    # 7) Округляем value до того же разряда
    val_final = round(value, decimal_place)

    # 8) Формируем строковый вывод
    val_str = f"{val_final:.{decimal_place}f}"
    err_str = f"{err_final:.{decimal_place}f}"
    return val_str, err_str


# --- ДАННЫЕ ЭКСПЕРИМЕНТА ---
delta_T = np.array([3.4, 3.3, 3.2, 3.1,])    # Значения ΔT __X__
delta_P = np.array([9, 8.7, 7.9, 6.8])       # Значения ΔP (атм) __Y__
delta_P_err = 0.3  # Погрешность по оси Y

# --- ЛИНЕЙНАЯ АППРОКСИМАЦИЯ (МНК) ---
coeff, cov = np.polyfit(delta_T, delta_P, deg=1, cov=True)
k, b = coeff
k_err, b_err = np.sqrt(np.diag(cov))

# 1) "Сырые" данные с точностью до 5 знаков после запятой (выводим в консоль)
print("Коэффициенты (с точностью до 5 знаков после запятой):")
print(f"k = {k:.5f} ± {k_err:.5f}")
print(f"b = {b:.5f} ± {b_err:.5f}")

# 2) Для легенды округляем "физически" по правилу (1 или 2 -> две значащие цифры, иначе одна)
k_str, k_err_str = phys_round(k, k_err)
b_str, b_err_str = phys_round(b, b_err)

# --- ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКА ---
delta_T_fit = np.linspace(delta_T.min(), delta_T.max()+0.2, 200)
delta_P_fit = k * delta_T_fit + b

# --- ПОСТРОЕНИЕ ГРАФИКА ---
plt.figure(figsize=(8, 6))

# Точки с вертикальными погрешностями (но без легенды)
plt.errorbar(delta_T, delta_P, yerr=delta_P_err, xerr=0.1, fmt='o',
             ecolor='black', capsize=3, label='_nolegend_')

# Фиктивный объект, чтобы в легенде была метка "Эксперимент"
plt.plot([], [], 'o', color='blue', label='Эксперимент')

# Прямая аппроксимации
plt.plot(delta_T_fit, delta_P_fit, 'r',
         label='Линейная аппроксимация: $y = kx + b$')

# Отдельные строки для k и b
#k_label = rf"$k = ({k_str} \pm {k_err_str})$"
#b_label = rf"$b = ({b_str} \pm {b_err_str})$"

#plt.plot([], [], ' ', label=k_label)
#plt.plot([], [], ' ', label=b_label)

# Оформление
plt.xlabel(r'$ \frac{1}{T} \cdot 10^{-3}, \frac{1}{К} \cdot 10^{-3}$', fontsize=15)
plt.ylabel(r'$ \mu \cdot 10^{-6}, \frac{K}{ПA} \cdot 10^{-6} $', fontsize=15)
plt.grid(True)
plt.legend(loc='best')
plt.title(r'График зависимости $\mu (\frac{1}{T})$', fontsize=12)


plt.show()
