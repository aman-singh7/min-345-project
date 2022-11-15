import numpy as np
from .models import Fanno
from gasflow.utils import check
from gasflow.utils import apply_bisection


# Compute the Fanno's Critical Temperature Ratio T/T*.
@check
def critical_temperature_ratio(M, gamma=1.4):
    return ((gamma + 1) / 2) / (1 + ((gamma - 1) / 2) * M**2)


# Compute the Fanno's Critical Pressure Ratio P/P*.
@check
def critical_pressure_ratio(M, gamma=1.4):
    return (1 / M) * np.sqrt(((gamma + 1) / 2) / (1 + ((gamma - 1) / 2) * M**2))


# Compute the Fanno's Critical Density Ratio rho/rho*.
@check
def critical_density_ratio(M, gamma=1.4):
    return (1 / M) * np.sqrt((2 + (gamma - 1) * M**2) / (gamma + 1))


# Compute the Fanno's Critical Total Pressure Ratio P0/P0*.
@check
def critical_total_pressure_ratio(M, gamma=1.4):
    return (1 / M) * ((1 + ((gamma - 1) / 2) * M**2) / ((gamma + 1) / 2)) ** (
        (gamma + 1) / (2 * (gamma - 1))
    )


# Compute the Fanno's Critical Velocity Ratio U/U*.
@check
def critical_velocity_ratio(M, gamma=1.4):
    return M * np.sqrt(((gamma + 1) / 2) / (1 + ((gamma - 1) / 2) * M**2))


# Compute the Fanno's Critical Friction Parameter 4fL*/D.
@check
def critical_friction_parameter(M, gamma=1.4):
    f = np.zeros_like(M)
    f[M == 0] = np.inf
    f[M != 0] = ((gamma + 1) / (2 * gamma)) * np.log(
        ((gamma + 1) / 2) * M**2 / (1 + ((gamma - 1) / 2) * M**2)
    ) + (1 / gamma) * (1 / M**2 - 1)
    return f


# Compute the Fanno's Critical Entropy Parameter (s*-s)/R.
@check
def critical_entropy_parameter(M, gamma=1.4):
    return np.log(
        (1 / M)
        * ((1 + ((gamma - 1) / 2) * M**2) / (1 + ((gamma - 1) / 2)))
        ** ((gamma + 1) / (2 * (gamma - 1)))
    )


# Compute the Mach number given Fanno's Critical Temperature Ratio T/T*.
@check
def m_from_critical_temperature_ratio(ratio, gamma=1.4):
    upper_lim = critical_temperature_ratio(0, gamma)
    if np.any(ratio <= 0) or np.any(ratio >= upper_lim):
        raise ValueError("It must be 0 < T/T* < {}.".format(upper_lim))
    return np.sqrt(-ratio * (gamma - 1) * (2 * ratio - gamma - 1)) / (
        ratio * gamma - ratio
    )


# Compute the Mach number given Fanno's Critical Pressure Ratio P/P*.
@check
def m_from_critical_pressure_ratio(ratio, gamma=1.4):
    return np.sqrt(
        -ratio * (gamma - 1) * (ratio - np.sqrt(ratio**2 + gamma**2 - 1))
    ) / (ratio * gamma - ratio)


# Compute the Mach number given Fanno's Critical Density Ratio rho/rho*.
@check
def m_from_critical_density_ratio(ratio, gamma=1.4):
    lower_lim = np.sqrt((gamma - 1) / (gamma + 1))
    if np.any(ratio < lower_lim):
        raise ValueError("The critical density ratio must be >= {}.".format(lower_lim))
    return np.sqrt(2 / ((gamma + 1) * ratio**2 - (gamma - 1)))


# Compute the Mach number given Fanno's Critical Total Pressure Ratio P0/P0*.
@check
def m_from_critical_total_pressure_ratio(ratio, flag="sub", gamma=1.4):
    if np.any(ratio < 1):
        raise ValueError("It must be P/P* > 1.")

    func = lambda M, r: r - (1 / M) * (
        (1 + ((gamma - 1) / 2) * M**2) / ((gamma + 1) / 2)
    ) ** ((gamma + 1) / (2 * (gamma - 1)))

    return apply_bisection(ratio, func, flag=flag)


# Compute the Mach number given Fanno's Critical Velocity Ratio U/U*.
@check
def m_from_critical_velocity_ratio(ratio, gamma=1.4):
    lower_lim = np.sqrt((gamma - 1) / (gamma + 1))
    upper_lim = 1 / lower_lim
    if np.any(ratio < 0) or np.any(ratio >= upper_lim):
        raise ValueError("It must be 0 <= U/U* < {}.".format(upper_lim))
    return 2 * ratio / np.sqrt(2 * gamma + 2 - 2 * ratio**2 * gamma + 2 * ratio**2)


# Compute the Mach number given Fanno's Critical Friction Parameter 4fL*/D.
@check
def m_from_critical_friction(fp, flag="sub", gamma=1.4):
    if flag == "sub":
        if np.any(fp < 0):
            raise ValueError("It must be fp >= 0.")
    else:
        upper_lim = ((gamma + 1) * np.log((gamma + 1) / (gamma - 1)) - 2) / (2 * gamma)
        if np.any(fp < 0) or np.any(fp > upper_lim):
            raise ValueError("It must be 0 <= fp <= {}".format(upper_lim))

    func = lambda M, r: r - (
        ((gamma + 1) / (2 * gamma))
        * np.log(((gamma + 1) / 2) * M**2 / (1 + ((gamma - 1) / 2) * M**2))
        + (1 / gamma) * (1 / M**2 - 1)
    )

    return apply_bisection(fp, func, flag=flag)


# Compute the Mach number given Fanno's Critical Entropy Parameter (s*-s)/R.
@check
def m_from_critical_entropy(ep, flag="sub", gamma=1.4):
    if np.any(ep < 0):
        raise ValueError("It must be (s* - s) / R >= 0.")

    func = lambda M, r: r - np.log(
        (1 / M)
        * ((1 + ((gamma - 1) / 2) * M**2) / (1 + ((gamma - 1) / 2)))
        ** ((gamma + 1) / (2 * (gamma - 1)))
    )

    return apply_bisection(ep, func, flag=flag)


# Compute all fanno ratios given the Mach number.
@check
def get_ratios_from_mach(M, gamma=1.4):
    prs = critical_pressure_ratio(M, gamma)
    drs = critical_density_ratio(M, gamma)
    trs = critical_temperature_ratio(M, gamma)
    tprs = critical_total_pressure_ratio(M, gamma)
    urs = critical_velocity_ratio(M, gamma)
    fps = critical_friction_parameter(M, gamma)
    eps = critical_entropy_parameter(M, gamma)

    fanno = Fanno(
        mach=M,
        pressure_ratio=prs,
        density_ratio=drs,
        temperature_ratio=trs,
        total_pressure_ratio=tprs,
        velocity_ratio=urs,
        friction=fps,
        entropy=eps,
    )

    return fanno
