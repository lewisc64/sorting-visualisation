import threading
import random
import math

sorts = {}
def is_sort(func):
    global sorts
    sorts[func.__name__] = func
    return func

def perform(func, data):
    if isinstance(func, str):
        func = sorts[func]
    thread = threading.Thread(target=func, args=(data,))
    thread.start()
    return thread

@is_sort
def quick_sort(data, lo=None, hi=None):
    if lo is None:
        lo = 0
    if hi is None:
        hi = len(data) - 1
    if lo < hi:
        p = partition(data, lo, hi)
        quick_sort(data, lo, p - 1)
        quick_sort(data, p + 1, hi)

def partition(data, lo, hi):
    
    data.set_active_positions([x for x in range(lo, hi+1)])
    
    pivot = data[hi]
    i = lo
    for j in range(lo, hi):
        if data[j] < pivot:
            
            data.wait_for_step()
            
            data[i], data[j] = data[j], data[i]
            i += 1
    data[i], data[hi] = data[hi], data[i]
    return i

@is_sort
def radix_sort_lsd(data):
    buckets = [[] for x in range(10)]

    largest = 1
    digit = 1
    while 10 ** (digit - 1) <= largest:
        
        for i in range(len(data)):

            data.set_active_positions([i])
            data.wait_for_step()

            n = data[i]
            if digit == 1:
                if largest is None or n > largest:
                    largest = n
            
            buckets[(n // 10 ** (digit - 1)) % 10].append(n)

        i = 0
        for bucket in buckets:
            while len(bucket) > 0:

                data.set_active_positions([i])
                data.wait_for_step()
                
                data[i] = bucket.pop(0)
                i += 1
            
        digit += 1

@is_sort
def merge_sort(data, i=None, j=None):
    if i is None:
        i = 0
    if j is None:
        j = len(data) - 1
    if i == j:
        return i, j

    i1, j1 = merge_sort(data, i, (i + j) // 2)
    i2, j2 = merge_sort(data, (i + j) // 2 + 1, j)

    data.set_active_positions([x for x in range(i, j+1)])
    
    merge(data, i1, j1, i2, j2)
    return i, j

def merge(data, i1, j1, i2, j2):
    i = i1
    a1 = data[i1:j1+1]
    a2 = data[i2:j2+1]
    i1 = 0
    i2 = 0
    while i1 < len(a1) or i2 < len(a2):
        
        data.wait_for_step()
        
        if i1 >= len(a1) or (i2 < len(a2) and a1[i1] > a2[i2]):
            data[i] = a2[i2]
            i2 += 1
        else:
            data[i] = a1[i1]
            i1 += 1
        i += 1

@is_sort
def bubble_sort(data):
    for i in range(len(data) - 1, 1, -1):
        flag = False
        for j in range(i):
            if data[j] > data[j + 1]:
                flag = True
                
                data.set_active_positions([j, j + 1])
                data.wait_for_step()
                
                data[j], data[j + 1] = data[j + 1], data[j]
            
        data.sorted_positions.append(i)

        if not flag:
            break

@is_sort
def insertion_sort(data):
    for i in range(1, len(data)):
        
        v = data[i]
        j = i - 1
        
        while data[j] > v and j >= 0:
            
            data.set_active_positions([j])
            data.wait_for_step()
            
            data[j + 1] = data[j]
            j -= 1
            
        data[j + 1] = v
    
@is_sort
def bogo_sort(data):
    while True:
        data.wait_for_step()
        random.shuffle(data)
        last = 0
        for i in range(len(data)):
            
            data.set_active_positions([i])
            data.wait_for_step()
            
            x = data[i]
            if x < last:
                break
            last = x
        else:
            break
            
        data.set_active_positions([])
