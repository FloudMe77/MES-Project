# Dariusz Marecik

import numpy as np
import matplotlib.pyplot as plt


def E(x):
    # return 2 if x <= 1 else 6
    return 2 if x <= 1 else 21-10*x


def e(i, h, x):
    xi = i*h
    if x < xi - h or x > xi+h:
        return 0
    if x < xi:
        return (x - xi + h) / h
    return (xi + h - x) / h

def e_prim(i, h, x):
    xi = i*h
    if x < xi - h or x > xi + h:
        return 0
    if x < xi:
        return 1/h
    return -1/h

def B(i, j, h, n):
    # przedziały się nie nakładają
    if abs(i-j) > 1:
        return 0

    # i odpowiada 
    start = 2 * max(max(i, j) - 1, 0) / n
    end = 2 * min(min(i, j) + 1, n) / n
    return 4 * e(i,h,0) * e(j,h,0) - gauss_quadrature(lambda x: E(x) * e_prim(j,h,x) * e_prim(i,h,x), start, end)

def L(j,h, n):
    start = 2 * max(j - 1, 0) / n
    end = 2 * min(j + 1, n) / n
    return -20 * e(j,h,0) + gauss_quadrature(lambda x: 1000 * np.sin(np.pi * x) * e(j,h,x), start ,end)

def gauss_quadrature(func, a, b, n = 50):
    # Pobieramy węzły i wagi dla kwadratury Gaussa
    nodes, weights = np.polynomial.legendre.leggauss(n)
    
    # Przekształcenie przedziału [-1, 1] na przedział [a, b]
    # x = 0.5 * ((b - a) * nodes + (b + a))
    # w = (b - a) / 2
    transformed_nodes = 0.5 * ((b - a) * nodes + (b + a))
    transformed_weights = 0.5 * (b - a) * weights

    # Obliczenie wartości całki
    integral = sum(w * func(x) for x, w in zip(transformed_nodes, transformed_weights))
    return integral

def fill_B(n):
    h = 2/n
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            # odwrócone i z j
            A[i][j] = B(i,j,h, n)
    return A

def fill_L(n):
    h = 2/n
    B = [0 for _ in range(n)]
    for i in range(n):
        B[i] = L(i,h, n)
    return B

def gauss_elimination(A, B):
    n = len(A)

    # Tworzymy rozszerzoną macierz [A | B]
    AB = [A[i] + [B[i]] for i in range(n)]

    # Eliminacja Gaussa
    for i in range(n):
        # Wybór elementu głównego
        max_row = max(range(i, n), key=lambda r: abs(AB[r][i]))
        AB[i], AB[max_row] = AB[max_row], AB[i]  # Zamiana wierszy

        # Normalizacja wiersza
        pivot = AB[i][i]
        if pivot == 0:
            raise ValueError("Macierz osobliwa - brak jednoznacznego rozwiązania.")
        AB[i] = [x / pivot for x in AB[i]]

        # Zerowanie elementów pod główną przekątną
        for j in range(i + 1, n):
            factor = AB[j][i]
            AB[j] = [xj - factor * xi for xi, xj in zip(AB[i], AB[j])]

    # Podstawianie wsteczne
    X = [0] * n
    for i in range(n - 1, -1, -1):
        X[i] = AB[i][-1] - sum(AB[i][j] * X[j] for j in range(i + 1, n))
    return X

def solve(n):
    B = fill_B(n)
    L = fill_L(n)
    sol = gauss_elimination(B, L)
    # dodanie 3, bo znaleźliśmy w, a szukamy u
    for i in range(len(sol)):
        sol[i] += 10
    sol.append(10)
    return sol

def draw_plot():
    n = int(input("podaj n: "))

    plt.plot(np.linspace(0, 2, n+1 ), solve(n))
    plt.grid()
    plt.title('Odkształcenie sprężyste, n = ' + str(n))
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.savefig('Odkształcenie_sprężyste_wykres_n'+str(n)+'.png')
    plt.show()

if __name__ == "__main__":
    draw_plot()