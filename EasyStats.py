import numpy as np

def LinearFitCasero(x, y):
    # https://en.wikipedia.org/wiki/Simple_linear_regression
    x_avg = _average(x)
    y_avg = _average(y)

    m_sum_0_x = [(x_i - x_avg) for x_i in x]
    m_sum_0_y = [(y_i - y_avg) for y_i in y]
    m_sum_0 = 0
    m_sum_1 = 0
    for i in range(len(x)):
        m_sum_0 += m_sum_0_x[i] * m_sum_0_y[i]
        m_sum_1 += m_sum_0_x[i]**2

    m = m_sum_0/m_sum_1
    b = y_avg-m*x_avg

    return [m*x_i + b for x_i in x], [m, b]

def LinearFit(x, y):
    poly = np.polyfit(x, y, 1)
    return [poly[0]*x_i + poly[1] for x_i in x], poly

def LinearFitOrigin(x, y):
    m = _dot_product(y, x) / _dot_product(x, x)
    return [m*x_i for x_i in x], [m, 0]

def QuadraticFit(x, y):
    poly = np.polyfit(x, y, 2)
    return [poly[0]*x_i**2 + poly[1]*x_i + poly[2] for x_i in x], [poly[0], poly[1], poly[2]]

def NRankFit(x, y, n):
    poly = np.polyfit(x, y, n)
    fit = []
    for x_i in x:
        res = 0
        for i in range(n+1):
            res += poly[i] * x_i**(n-i)
        fit.append(res)
    return fit, poly

# helper internal functions
def _average(a):
    return sum(a)/len(a)

def _dot_product(v, w):
    dot = 0
    for i in range(len(v)):
        dot += v[i] * w[i]
    return dot
