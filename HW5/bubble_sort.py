def my_map(func, lst):
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])


def my_filter(func, lst):
    if not lst:
        return []
    head, tail = lst[0], lst[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)


def my_reduce(func, lst, initializer=None):
    if initializer is None:
        if not lst:
            raise TypeError("reduce() of empty sequence with no initial value")
        return my_reduce(func, lst[1:], lst[0])
    if not lst:
        return initializer
    return my_reduce(func, lst[1:], func(initializer, lst[0]))


def repeat_list(n):
    if n <= 0:
        return []
    return [0] + repeat_list(n - 1)


def bubble_pass(lst):
    if not lst:
        return []
    
    def reducer(acc, x):
        prev_val, res = acc
        if prev_val is None:
            return (x, res)
        if prev_val > x:
            return (prev_val, res + [x])
        else:
            return (x, res + [prev_val])

    last_val, res = my_reduce(reducer, lst, (None, []))
    return res + [last_val]


def bubble_sort(lst):
    if not lst:
        return []
    
    dummy_range = repeat_list(len(lst))
    

    return my_reduce(lambda current_lst, _: bubble_pass(current_lst), dummy_range, lst)
