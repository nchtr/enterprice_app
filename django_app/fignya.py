# n, s = map(int, input().split())
#
# print(n, s)
#
# gold = []
# silver = []
# bronze = []
#
# for _ in range(n):
#     a, b, c = map(int, input().split())
#     if c == 1:
#         gold.append((a, b))
#     elif c == 2:
#         silver.append((a, b))
#     else:
#         bronze.append((a, b))
#
# print(gold, silver, bronze)
#
# gold.sort(reverse=True, key=lambda x: x[1])
# silver.sort(reverse=True, key=lambda x: x[1])
# bronze.sort(reverse=True, key=lambda x: x[1])
#
# print(gold, silver, bronze)
#
# min_qualities = []
#
# for i in range(min(2, len(gold))):
#     for j in range(min(2, len(silver))):
#         for k in range(min(2, len(bronze))):
#             total_cost = gold[i][0] + silver[j][0] + bronze[k][0]
#             if total_cost <= s:
#                 min_qualities.append(min(gold[i][1], silver[j][1], bronze[k][1]))
#             print(min_qualities)
#             print(total_cost)
#             print(min(gold[i][1], silver[j][1], bronze[k][1]))
#
# print(min(2, len(gold)), min(2, len(silver)), min(2, len(bronze)))
# print(min_qualities)
#
# if min_qualities:
#     result = max(min_qualities)
#     print(result)
# else:
#     print("0")


# def gcd(a, b):
#     while b:
#         a, b = b, a % b
#     return a
#
#
# def array_gcd(arr):
#     result = arr[0]
#     for i in range(1, len(arr)):
#         result = gcd(result, arr[i])
#     return result
#
#
# def is_great_number(array_gcd, num):
#     return gcd(array_gcd, num) == 1
#
#
# # Чтение входных данных
# n, q = map(int, input().split())
# array = list(map(int, input().split()))
#
# # Нахождение НОД для изначального массива
# initial_gcd = array_gcd(array)
#
# # Обработка запросов
# for _ in range(q):
#     query = int(input())
#     result = "YES" if is_great_number(initial_gcd, query) else "NO"
#     print(result)


# def max_profit(n, k, s):
#     s.sort(reverse=True)  # Сортируем массив сумм денег в порядке убывания
#     total_profit = 0
#
#     for i in range(n):
#         max_price = s[i] - i * k  # Максимальная цена, которую клиент готов заплатить
#         if max_price > 0:
#             total_profit += max_price
#
#     return total_profit
#
#
# # Чтение входных данных
# n, k = map(int, input().split())
# s = list(map(int, input().split()))
#
# # Вывод результата
# result = max_profit(n, k, s)
# print(result)


# MOD = 10**9 + 7
#
#
# def calculate_sum(n, coordinates):
#     sum_x = sum(coordinates[i][0] for i in range(n))
#     sum_y = sum(coordinates[i][1] for i in range(n))
#     sum_xy = sum(
#         coordinates[i][0] * coordinates[j][1] for i in range(n) for j in range(i + 1, n)
#     )
#
#     result = (sum_x * sum_y - sum_xy) % MOD
#     return result
#
#
# # Чтение входных данных
# n = int(input())
# coordinates = [tuple(map(int, input().split())) for _ in range(n)]
#
# # Вывод результата
# result = calculate_sum(n, coordinates)
# print(result)


N = int(2e5 + 10)
mod = int(1e9) + 7
n, q, a, was = 0, 0, [0] * N, [False] * N
d = [[] for _ in range(N)]


def main():
    global n, q, a, was, d
    T = 1
    n, q = map(int, input().strip().split())

    for i in range(n):
        a[i] = int(input().strip())

    for i in range(2, N):
        if not d[i]:
            for j in range(i, N, i):
                d[j].append(i)

    for it in range(1, q + 1):
        f = False
        x = int(input().strip())

        for i in range(n):
            if f:
                break
            for p in d[a[i]]:
                if x % p == 0:
                    f = True
                    break

        if f:
            print("YES")
        else:
            print("NO")


if __name__ == "__main__":
    main()
