import numpy as np # Библиотека для численных вычислений 
import math # Библиотека для доступа к математическим функциям
from scipy import integrate # Библиотека, предоставляющая функции для численного интегрирования
import sympy # Библиотека для символьных математических вычислений


# Аналитическое вычисление интеграла с использованием SymPy
# 2. Задаем аналитически функцию F(x) = f(x) и находим ее первообразную
x = sympy.Symbol('x') # Для библиотеки SymPy создаем символьную переменную 
f = x * sympy.sin(x**2)# Определяем символьную функцию по 7 варианту
F = sympy.integrate(f, x) # Находим символьно первообразную 
print(f"Первообразная F(x): {F}")

# Вычисляем интеграл в пределах от 0 до pi
sym1 = 0 # Задание нижнего предела интегрирования
sym2 = math.pi # Теперь верхнего предела интегрирования
ex_val = F.subs(x, sym2) - F.subs(x, sym1) # Вычисляем значение интеграла от 0 до π (вариант 7) через подстановку значений в первообразную F(x) 
print(f"Точное значение интеграла: {ex_val}")

def f(x): # Функция, которую интегрируем по варианту 7
    return x * np.sin(x**2)

# 3. Численно вычислить интеграл, используя формулы прямоугольников, трапеций, парабол (Симпсона)
def rectangle(a, b, n, f): # Функция для численного интегрирования методом прямоугольников - разбиваем интервал на n частей и вычисляем сумму площадей прямоугольников
# Аппроксимируем площадь под кривой суммой площадей прямоугольников
# Высота каждого прямоугольника берется равной значению функции в некоторой точке внутри интервала (в середине - метод средних прямоугольников)
    h = (b - a) / n
    x = np.linspace(a + h/2, b - h/2, n)  # Берем середины отрезков
    y = f(x)
    integral = h * np.sum(y)
    return integral

def trapezoidal(a, b, n, f): # Функция для численного интегрирования методом трапеций
# Аппроксимируем площадь под кривой суммой площадей трапеций
# Основания трапеций расположены на границах интервалов, а высоты равны значениям функции в этих точках
    h = (b - a) / n # Вычисляем ширину каждого интервала трапеции
    x = np.linspace(a, b, n + 1) # Cоздаем массив x точек, равномерно распределенных в интервале [a, b]
    y = f(x) # Вычисляем значения функции f в каждой точке, содержащейся в массиве x
    integral = (h/2) * (y[0] + 2*np.sum(y[1:-1]) + y[-1]) #Вычисляем приближенное значение интеграла методом трапеций
    return integral

def simpson(a, b, n, f): # Функция для численного интегрирования методом Симпсона - проверяем, что количество разбиений n является четным
# Аппроксимируем функцию на каждом интервале квадратичным полиномом (параболой)
# Площадь под кривой аппроксимируется суммой площадей под параболами
# По скорости - самый быстрый метод, по точности также, погрешность меньше, чем у других методов
    if n % 2 != 0:
        raise ValueError("Количество разбиений (n) должно быть четным.")

# Вычисляем шаг h, для этого создаем массив точек x, и вычисляем значения функции f(x) в этих точках
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)  # Создаем массив точек x
    y = f(x)  # Вычисляем значения функции в точках x

    #Сумма площадей трапеций Симпсона
    integral = h/3 * (y[0] + 2*sum(y[2:n:2]) + 4*sum(y[1:n:2]) + y[n])
    return integral


# 1. Задаем параметры сетки a, b, N; находим h, xi
a = 0  # Нижний предел интегрирования
b = np.pi  # Верхний предел интегрирования
val = [10, 20, 50, 100]  # Разные значения N для сравнения

res = {} # Создаем пустой словарь  для хранения результатов вычислений

# 3. Вычисляем значения функции в точках xi (fi = F(xi)) -  происходит внутри каждой численной функции
# 4. Вычисляем интеграл по формулам (2, 3, 8) и выводим полученные значения
# Начинаем цикл по значениям N из списка val, создавая пустой словарь для хранения результатов для текущего N
for N in val: 
    res[N] = {}

    # 4.1 Метод прямоугольников
    i_rectangle = rectangle(a, b, N, f)
    res[N]['rectangle'] = i_rectangle # Вычисляем интеграл методом прямоугольников и сохраняем  в словаре res, аналогично для других методов

    # 4.2 Метод трапеций
    i_trapezoidal = trapezoidal(a, b, N, f)
    res[N]['trapezoidal'] = i_trapezoidal

    # 4.3 Метод Симпсона
    i_simpson = simpson(a, b, N, f)
    res[N]['simpson'] = i_simpson

    print(f"\nРезультаты для N = {N}:") # Вывод полученных значений для текущего N
    print(f"  Метод прямоугольников: {i_rectangle}")
    print(f"  Метод трапеций: {i_trapezoidal}")
    print(f"  Метод Симпсона: {i_simpson}")

# Вычисляем точного значения интеграла с использованием scipy.integrate.quad для сравнения
i_exact, err_est = integrate.quad(f, a, b) # 2. Вычисляем точное значение интеграла (аналитически)
print(f"\nТочное значение интеграла (scipy.integrate.quad): {i_exact}")

# 5. Сравниваем эти значения с точным интегралом, то есть находим так называемую прогрешность 
for N in val:
    print(f"\nСравнение для N = {N}:")
    print(f"  Погрешность (метод прямоугольников): {abs(res[N]['rectangle'] - i_exact)}")
    print(f"  Погрешность (метод трапеций): {abs(res[N]['trapezoidal'] - i_exact)}")
    print(f"  Погрешность (метод Симпсона): {abs(res[N]['simpson'] - i_exact)}")