import numpy as np
from functools import wraps
from scipy.optimize import bisect
import inspect

# Helper function used for applying the bisection method to find the
# roots of a given function.
def apply_bisection(ratio, func, flag="sub"):
    if flag == "sub":
        mach_range = [np.spacing(1), 1]
    else:
        mach_range = [1, 100]

    M = np.zeros_like(ratio)
    for i, r in enumerate(ratio):
        M[i] = bisect(func, *mach_range, args=(r))
    return M


def convert_to_ndarray(x):
    """
    Check if the input parameter is of type np.ndarray.
    If not, convert it to np.ndarray and make sure it is at least
    1 dimensional.
    """
    if not isinstance(x, np.ndarray):
        return np.atleast_1d(np.array(x, copy=False, dtype=np.float64))
    if x.ndim == 0:
        return np.atleast_1d(np.array(x, copy=False, dtype=np.float64))
    return x

def _check_specific_heat_ratio(gamma):
    if gamma <= 1:
        raise ValueError("The specific heats ratio must be > 1.")

def _check_mach_number(M, value):
    if not np.all(M >= value):
        raise ValueError("The Mach number must be >= {}.".format(value))

def _check_flag(flag):
    flag = flag.lower()
    if flag not in ["sub", "super"]:
        raise ValueError("Flag can be either 'sub' or 'super'.")
    return flag

def ret_correct_vals(x):
    """ Many functions implemented in this package requires their input
    arguments to be Numpy arrays, hence a few decorators take care of the
    conversion before applying the function.
    However, If I pass a scalar value to a function, I would like it to return
    a scalar value, and not a Numpy one-dimensional or zero-dimensional array.
    These function extract the scalar array from a 0-D or 1-D Numpy array.
    """
    if isinstance(x, tuple):
        # Many functions return a tuple of elements. If I give in input a single
        # mach number, it may happens that the function return a tuple of 1-D
        # Numpy arrays. But I want a tuple of numbers. Hence, the following lines
        # of code extract the values from the 1-D array and return a modified
        # tuple of elements.
        new_x = []
        for e in x:
            new_x.append(ret_correct_vals(e))
        return new_x
    elif isinstance(x, dict):
        # Many functions may return a dictionary of elements. Each value may
        # be a 1-D one-element array. If that's the case, extract that number.
        x = {k: ret_correct_vals(v) for k, v in x.items()}
    if isinstance(x, np.ndarray) and (x.ndim == 1) and (x.size == 1):
        return x[0]
    elif isinstance(x, np.ndarray) and (x.ndim == 0):
        return x[()]
    return x

# Convert the arguments specified in index_list to np.ndarray.
# By applying this conversion, the function will be able to handle
# as argument both a number, a list of numbers or a np.ndarray.
def as_array(index_list=[0]):
    """
    Convert the arguments specified in index_list to np.ndarray.
    With this we can pass a number, a list of numbers or a np.ndarray.

    Parameters
    ----------
    original_function : callable
    index_list : list
    """
    def decorator(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):

            args = list(args)
            for i in index_list:
                if i < len(args):
                    args[i] = convert_to_ndarray(args[i])
            return original_function(*args, **kwargs)
        wrapper_function.__no_check = original_function
        return wrapper_function
    return decorator

def get_parameters_dict(original_function, *args, **kwargs):
    """
    Get a dictionary of parameters passed to the original_function.
    """
    # https://stackoverflow.com/a/53715901/2329968
    param = inspect.signature(original_function).parameters
    all_param = {
        k: args[n] if n < len(args) else v.default
        for n, (k, v) in enumerate(param.items()) if k != 'kwargs'
    }
    all_param.update(kwargs)
    return all_param

# This decorator is used to convert and check the arguments of the
# function in the modules: isentropic, fanno, rayleigh, generic
def check(var=None):
    def decorator(original_function):
        indeces = [0]
        if not callable(var):
            indeces = var

        @wraps(original_function)
        @as_array(indeces)
        def wrapper_function(*args, **kwargs):
            args = list(args)
            all_param = get_parameters_dict(original_function, *args, **kwargs)

            if "M" in all_param.keys():
                _check_mach_number(all_param["M"], 0)
            # TODO: the following check is used in the shockwave.mach_downstream
            # function. Ideally, it should be inside check_shockwave decorator,
            # but that already does a check for M1. Alternatives:
            # 1. build a new ad-hoc decorator only for shockwave.mach_downstream
            # 2. see if it's possible to pass comparison arguments to the decorator,
            # for example to say check M1 > 0.
            if "M1" in all_param.keys():
                _check_mach_number(all_param["M1"], 0)
            if "gamma" in all_param.keys():
                _check_specific_heat_ratio(all_param["gamma"])

            # all_param include all parameters, even if they were not specified.
            # therefore, I need to check if flag has been effectively given!
            if "flag" in all_param.keys():
                flag = _check_flag(all_param["flag"])
                if len(args) > 1:
                    args[1] = flag
                else:
                    kwargs["flag"] = flag
            res = original_function(*args, **kwargs)
            return ret_correct_vals(res)

        def no_check_function(*args, **kwargs):
            res = original_function(*args, **kwargs)
            return ret_correct_vals(res)
        wrapper_function.__no_check = no_check_function
        return wrapper_function

    if callable(var):
        return decorator(var)
    else:
        return decorator
