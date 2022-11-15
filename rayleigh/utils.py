import numpy as np
from .models import Rayleigh
from gasflow.utils import check
from gasflow.utils import apply_bisection

# Compute the Rayleigh's Critical Total Temperature Ratio T0/T0*
@check
def critical_total_temperature_ratio(M, gamma=1.4):
    return (
        2
        * (1 + gamma)
        * M**2
        / (1 + gamma * M**2) ** 2
        * (1 + ((gamma - 1) / 2) * M**2)
    )


# Compute the Rayleigh's Critical Temperature Ratio T/T*.
@check
def critical_temperature_ratio(M, gamma=1.4):
    return M**2 * (1 + gamma) ** 2 / (1 + gamma * M**2) ** 2


# Compute the Rayleigh's Critical Pressure Ratio P/P*.
@check
def critical_pressure_ratio(M, gamma=1.4):
    return (1 + gamma) / (1 + gamma * M**2)


# Compute the Rayleigh's Critical Density Ratio rho/rho*.
@check
def critical_density_ratio(M, gamma=1.4):
    return (1 + gamma * M**2) / ((gamma + 1) * M**2)


#
@check
def critical_total_pressure_ratio(M, gamma=1.4):
    return (
        (1 + gamma)
        / (1 + gamma * M**2)
        * ((1 + (gamma - 1) / 2 * M**2) / ((gamma + 1) / 2)) ** (gamma / (gamma - 1))
    )


# Compute the Rayleigh's Critical Velocity Ratio U/U*.
@check
def critical_velocity_ratio(M, gamma=1.4):
    return (1 + gamma) * M**2 / (1 + gamma * M**2)


# Compute the Rayleigh's Critical Entropy parameter (s*-s)/R.
@check
def critical_entropy_parameter(M, gamma=1.4):
    return (
        -gamma
        / (gamma - 1)
        * np.log(M**2 * ((gamma + 1) / (1 + gamma * M**2)) ** ((gamma + 1) / gamma))
    )


# Compute the Mach number given Rayleigh's Critical Total Temperature Ratio T0/T0*.
@check
def m_from_critical_total_temperature_ratio(ratio, flag="sub", gamma=1.4):
    if np.any(ratio < 0) or np.any(ratio > 1):
        raise ValueError("It must be 0 <= T0/T0* <= 1.")

    r = np.ones_like(ratio)
    idx = ratio != 1
    den = np.abs(ratio[idx] * gamma**2 + 1 - gamma**2)
    if flag == "sub":
        r[idx] = (
            np.sqrt(
                -(ratio[idx] * gamma**2 + 1 - gamma**2)
                * (
                    ratio[idx] * gamma
                    - 1
                    - gamma
                    + np.sqrt(
                        -2 * ratio[idx] * gamma
                        - ratio[idx] * gamma**2
                        + 1
                        + 2 * gamma
                        + gamma**2
                        - ratio[idx]
                    )
                )
            )
            / den
        )
    else:
        r[idx] = (
            np.sqrt(
                -(ratio[idx] * gamma**2 + 1 - gamma**2)
                * (
                    ratio[idx] * gamma
                    - 1
                    - gamma
                    - np.sqrt(
                        -2 * ratio[idx] * gamma
                        - ratio[idx] * gamma**2
                        + 1
                        + 2 * gamma
                        + gamma**2
                        - ratio[idx]
                    )
                )
            )
            / den
        )
    r[ratio == 1] = 1
    return r

# Compute the Mach number given Rayleigh's Critical Temperature Ratio T/T*.
@check
def m_from_critical_temperature_ratio(ratio, flag="sub", gamma=1.4):
    upper_lim = critical_temperature_ratio(1 / np.sqrt(gamma))
    if np.any(ratio < 0) or np.any(ratio > upper_lim):
        raise ValueError("It must be 0 < T/T* < {}.".format(upper_lim))

    M = np.zeros_like(ratio)
    if flag == "sub":
        M[ratio == 0] = 0
        M[ratio != 0] = np.sqrt(-2 * ratio[ratio != 0] * (2 * ratio[ratio != 0] * gamma - 1 - 2 * gamma - gamma**2 + np.sqrt(1 - 4 * ratio[ratio != 0] * gamma - 8 * ratio[ratio != 0] * gamma**2 - 4 * ratio[ratio != 0] * gamma**3 + 4 * gamma + 6 * gamma**2 + 4 * gamma**3 + gamma**4))) / (2 * ratio[ratio != 0] * gamma)
    else:
        M[ratio == 0] = np.inf
        M[ratio != 0] = np.sqrt(-2 * ratio[ratio != 0] * (2 * ratio[ratio != 0] * gamma - 1 - 2 * gamma - gamma**2 - np.sqrt(1 - 4 * ratio[ratio != 0] * gamma - 8 * ratio[ratio != 0] * gamma**2 - 4 * ratio[ratio != 0] * gamma**3 + 4 * gamma + 6 * gamma**2 + 4 * gamma**3 + gamma**4))) / (2 * ratio[ratio != 0] * gamma)
    return M

# Compute the Mach number given Rayleigh's Critical Pressure Ratio P/P*.
@check
def m_from_critical_pressure_ratio(ratio, gamma=1.4):
    upper_lim = critical_pressure_ratio(0, gamma)
    if np.any(ratio < 0) or np.any(ratio > upper_lim):
        raise ValueError("It must be 0 <= P/P* <= {}.".format(upper_lim))
    M = np.zeros_like(ratio)
    M[ratio == 0] = np.inf
    M[ratio != 0] = np.sqrt(ratio[ratio != 0] * gamma * (1 + gamma - ratio[ratio != 0])) / (ratio[ratio != 0] * gamma)
    return M

# Compute the Mach number given Rayleigh's Critical Total Pressure Ratio P0/P0*.
@check
def m_from_critical_total_pressure_ratio(ratio, flag="sub", gamma=1.4):
    if flag == "sub":
        upper_lim = critical_total_pressure_ratio(0, gamma)
        if np.any(ratio < 1) or np.any(ratio >= upper_lim):
            raise ValueError("It must be 1 <= P0/P0* < {}".format(upper_lim))
    else:
        if np.any(ratio < 1):
            raise ValueError("It must be P0/P0* >= 1")

    func = lambda M, r: r - (1 + gamma) / (1 + gamma * M**2) * ((1 + (gamma - 1) / 2 * M**2) / ((gamma + 1 ) / 2))**(gamma / (gamma - 1))

    return apply_bisection(ratio, func, flag=flag)


# Compute the Mach number given Rayleigh's Critical Density Ratio rho/rho*.
@check
def m_from_critical_density_ratio(ratio, gamma=1.4):
    lower_lim = gamma / (gamma + 1)
    if np.any(ratio <= lower_lim):
        raise ValueError("It must be rho/rho* > {}.".format(lower_lim))
    return np.sqrt(1 / (ratio * (gamma + 1) - gamma))


# Compute the Mach number given Rayleigh's Critical Velocity Ratio U/U*.
@check
def m_from_critical_velocity_ratio(ratio, gamma=1.4):
    upper_lim = (1 + gamma) / gamma
    if np.any(ratio >= upper_lim) or np.any(ratio <= 0):
        raise ValueError("It must be 0 < U/U* < {}.".format(upper_lim))
    return -np.sqrt(-(ratio * gamma - 1 - gamma) * ratio) / (ratio * gamma - 1 - gamma)


# Compute the Mach number given Rayleigh's Critical Entropy (s*-s)/R.
@check
def m_from_critical_entropy(ratio, flag="sub", gamma=1.4):
    if np.any(ratio < 0):
        raise ValueError("It must be (s*-s)/R >= 0.")

    func = lambda M, r: r - (-gamma /(gamma - 1) * np.log(M**2 * ((gamma + 1) / (1 + gamma * M**2))**((gamma + 1) / gamma)))

    return apply_bisection(ratio, func, flag=flag)

# Compute all Rayleigh ratios given the Mach number.
@check
def get_ratios_from_mach(M, gamma=1.4):
    prs = critical_pressure_ratio(M, gamma)
    drs = critical_density_ratio(M, gamma)
    trs = critical_temperature_ratio(M, gamma)
    tprs = critical_total_pressure_ratio(M, gamma)
    ttrs = critical_total_temperature_ratio(M, gamma)
    urs = critical_velocity_ratio(M, gamma)
    eps = critical_entropy_parameter(M, gamma)

    rayleigh = Rayleigh(
        mach = M,
        pressure_ratio = prs,
        density_ratio = drs,
        temperature_ratio = trs,
        total_pressure_ratio = tprs,
        velocity_ratio = urs,
        total_temperature_ratio = ttrs,
        entropy = eps,
    )

    return rayleigh