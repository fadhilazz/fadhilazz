import numpy as np
import matplotlib.pyplot as plt

# Constants for water properties used in calculation
WATER_DENSITY = 1000.0      # kg/m3
WATER_CP = 4.186e3          # J/(kg*C)


def sample_distribution(values, size):
    """Return random samples given (min, most likely, max) values."""
    if not isinstance(values, (list, tuple)):
        values = [values]
    vals = [float(v) for v in values]
    if len(vals) == 1:
        return np.full(size, vals[0])
    if len(vals) == 2:
        left, right = vals
        mode = 0.5 * (left + right)
        return np.random.triangular(left, mode, right, size)
    if len(vals) == 3:
        left, mode, right = vals
        return np.random.triangular(left, mode, right, size)
    raise ValueError("Invalid parameter specification")


def monte_carlo_power(params, iterations=10000):
    """Run Monte Carlo simulation for geothermal power."""
    area = sample_distribution(params['area_km2'], iterations) * 1e6  # km2 to m2
    thickness = sample_distribution(params['thickness_m'], iterations)
    density = sample_distribution(params['rock_density'], iterations)
    porosity = sample_distribution(params['porosity'], iterations)
    heat_capacity = sample_distribution(params['rock_cp_kj'], iterations) * 1e3  # kJ to J
    sw = sample_distribution(params['water_saturation'], iterations)
    recovery_factor = sample_distribution(params['recovery_factor'], iterations)
    delta_t = sample_distribution(params['cutoff_temp_c'], iterations)
    eff = sample_distribution(params['efficiency'], iterations) / 100.0
    life_years = sample_distribution(params['life_years'], iterations)

    volume = area * thickness
    term_rock = (1 - porosity) * density * heat_capacity
    term_water = porosity * sw * WATER_DENSITY * WATER_CP
    energy_joule = volume * (term_rock + term_water) * delta_t
    recoverable = energy_joule * recovery_factor
    power_watt = recoverable * eff / (life_years * 365.0 * 24.0 * 3600.0)
    power_mwe = power_watt / 1e6
    return power_mwe


def summarize(power_samples):
    p10 = np.percentile(power_samples, 10)
    p50 = np.percentile(power_samples, 50)
    p90 = np.percentile(power_samples, 90)
    return {'P10': p10, 'P50': p50, 'P90': p90}


def plot_results(power_samples):
    counts, bin_edges = np.histogram(power_samples, bins=50, density=False)
    cumulative = np.cumsum(counts)
    cumulative_prob = cumulative / cumulative[-1]

    fig, ax1 = plt.subplots()
    ax1.plot(bin_edges[1:], cumulative_prob, color='tab:blue')
    ax1.set_xlabel('Power (MWe)')
    ax1.set_ylabel('Cumulative Probability', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(bin_edges[1:], cumulative, color='tab:orange')
    ax2.set_ylabel('Cumulative Frequency', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    fig.tight_layout()
    plt.show()


def main():
    # Example parameters: provide (min, mode, max) or single values
    params = {
        'area_km2': [1.0, 2.0, 3.0],
        'thickness_m': [500, 700, 900],
        'rock_density': [2500],
        'porosity': [0.05, 0.1, 0.15],
        'rock_cp_kj': [0.85],
        'water_saturation': [0.8, 0.9],
        'recovery_factor': [0.2, 0.25, 0.3],
        'cutoff_temp_c': [180],
        'efficiency': [10],
        'life_years': [30]
    }

    samples = monte_carlo_power(params)
    stats = summarize(samples)
    print('P10 = {:.2f} MWe'.format(stats['P10']))
    print('P50 = {:.2f} MWe'.format(stats['P50']))
    print('P90 = {:.2f} MWe'.format(stats['P90']))

    plot_results(samples)


if __name__ == '__main__':
    main()
