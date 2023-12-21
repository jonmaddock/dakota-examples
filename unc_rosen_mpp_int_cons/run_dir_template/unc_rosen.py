"""Uncertain constrained Rosenbrock example."""

import numpy as np
from typing import Tuple


def rosenbrock(x: np.ndarray) -> np.ndarray:
    """Rosenbrock function.

    Parameters
    ----------
    x : np.ndarray
        Optimisation parameter vector

    Returns
    -------
    np.ndarray
        Result of Rosenbrock function
    """
    a = 1
    b = 100
    return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2


def con1(x: np.ndarray, e: np.ndarray) -> np.ndarray:
    """Value of constraint 1.

    Parameters
    ----------
    x : np.ndarray
        Optimisation parameter vector
    e : np.ndarray
        Epistemic uncertainties

    Returns
    -------
    np.ndarray
        Value of constraint
    """
    # return (x[0] - 1) ** 3 - x[1] + 1 + (e[0] + 1) ** 2
    return (x[0] + 2 * e[0]) ** 3 - x[1]


def con2(x: np.ndarray, e) -> np.ndarray:
    """Value of constraint 2.

    Parameters
    ----------
    x : np.ndarray
        Optimisation parameter vector

    Returns
    -------
    np.ndarray
        Value of constraint
    """
    # Add linear shift away from local point
    # return x[0] + x[1] - 2 + e[1] - 0.2
    return x[0] + (x[1] + e[1]) ** 2 - 2


def constraints(x: np.ndarray, e: np.ndarray) -> np.ndarray:
    """Calculate values of all constraints.

    Parameters
    ----------
    x : np.ndarray
        Optimisation parameter vector
    e : np.ndarray
        Epistemic uncertainties

    Returns
    -------
    np.ndarray
        Values of all constraints
    """
    return np.array([con1(x, e), con2(x, e)])


def main(x: np.ndarray, e: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate objective function and constraint values.

    Parameters
    ----------
    x : np.ndarray
        Optimisation parameter vector
    e : np.ndarray
        Epistemic uncertainties

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Objective function and constraint values
    """
    obj_func = rosenbrock(x)
    constrs = constraints(x, e)
    return obj_func, constrs
