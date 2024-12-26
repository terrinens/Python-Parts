import time
import numpy as np
from typing import List


def timer(fun, *args):
    st = time.perf_counter()
    result = fun(*args)
    ed = time.perf_counter()
    return result, f'{ed - st:.6f}'


def is_sorted(arr: List[int]) -> (bool, List[int]):
    incorrect_indices = []

    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            incorrect_indices.append(i)

    return len(incorrect_indices) == 0, incorrect_indices


def int_array_test(fun, size=None, result_print=False):
    if size is None:
        size = [10, 100, 1000, 10000, 50000]

    for s in size:
        arr = np.random.randint(0, 1000, s).tolist()
        memory = arr.copy()
        result, elapsed_time = timer(fun, arr)
        current, incorrect_indices = is_sorted(arr)

        print(f'생성된 크기 : {s} / 경과 시간 : {elapsed_time}/s {"" if current else current}')
        if not current:
            print('오답 정렬 요소들')
            for index in incorrect_indices:
                print(f'배열번호 {index}부터 오답')
                print(arr[index:min(index + 10, len(arr))])
                print()
        if not current: print(f'오답 케이스 : \n{memory}')
        if result_print: print(f'결과물 : \n{result}')


def simple_int_array_test(fun, size=4):
    test = 0
    sr, si = True, []
    memory = []
    arr = []
    while sr and test < 1000:
        test += 1
        arr = np.random.randint(0, 1000, size).tolist()
        memory = arr.copy()
        fun(arr)
        sr, si = is_sorted(arr)

    print(f'{sr} : {si} : {test}')
    if not sr:
        print(f'원본 : {memory}')
        print(f'결과 : {arr}')
