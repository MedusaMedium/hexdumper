'''
add_arithmetic_methods - https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
'''
import inspect
from functools import partial, wraps


ARITHMATIC_OPERATOR_NAMES_SHORT = [
    'add', 'sub', 'mul', 'matmul', 'truediv', 'floordiv',
    'mod', 'divmod', 'pow', 'lshift', 'rshift', 'and',
    'xor', 'or', 'radd', 'rsub', 'rmul', 'rmatmul',
    'rtruediv', 'rfloordiv', 'rmod', 'rdivmod', 'rpow',
    'rlshift', 'rrshift', 'rand', 'rxor', 'ror', 'iadd',
    'isub', 'imul', 'imatmul', 'itruediv', 'ifloordiv',
    'imod', 'ipow', 'ilshift', 'irshift', 'iand', 'ixor',
    'ior', 'neg', 'pos', 'abs', 'invert'
]
ARITHMATIC_OPERATOR_NAMES = [f'__{foo}__' for foo in ARITHMATIC_OPERATOR_NAMES_SHORT]


# TODO: add the rest of these
ITERATOR_OPERATOR_NAMES = [
    "__getitem__"
]


METHOD_NAMES = ARITHMATIC_OPERATOR_NAMES + ITERATOR_OPERATOR_NAMES


# TODO: refactor this
def setParentMethods(cls=None, methods:list=METHOD_NAMES):
    if cls is None:
        return partial(setParentMethods, methods=methods)
    
    def make_func(func_name):
        @wraps(func_name)
        def func(self, *args, **kwargs):
            super_method = getattr(super(cls, self), func_name)
            return type(self)(super_method(*args, **kwargs))

        func.__name__ = func_name
        func.__qualname__ = '{}.{}'.format(cls.__qualname__, func_name)
        func.__module__ = cls.__module__

        return func
    
    # im trying only to override the operators i have inherited
    # there is room for improvement here
    # override_funcs = set(target_methods) & set(dir(cls))
    # for func_name in target_methods:
    for func_name in methods:
        is_method = hasattr(cls, func_name) and callable(inspect.getattr_static(cls, func_name))
        if is_method:
            func = make_func(func_name)
            if func:
                setattr(cls, func_name, func)

    return cls