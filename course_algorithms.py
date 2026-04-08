
def insertion(L: list):
    n = len(L)
    for i in range(n):
        j = n - i - 1
        while j < n - 1 and L[j] > L[j + 1]:
            L[j], L[j + 1] = L[j + 1], L[j]
            j += 1


def bubble(L: list):

    n = len(L)

    for i in range(n-1):
        swapped = False
        for j in range(n-1- i):
            if L[j] > L[j+1]:
                L[j+1], L[j] = L[j], L[j+1]
                swapped = True
        if swapped == False:
            break