import numpy as np
from sklearn.cluster import KMeans


def kmeans_first_and_last_second_minimum(energy_signal, bins_per_second, normalize=True):
    if normalize:
        signal = energy_signal / np.linalg.norm(energy_signal)
        maximum_value = 1
    else:
        signal = energy_signal
        maximum_value = np.max(signal)
    first_second_energy_bins = signal[:bins_per_second]
    kmeans = KMeans(n_clusters=2)
    results_first_second = kmeans.fit(first_second_energy_bins.reshape(-1, 1))
    last_second_energy_bins = signal[-bins_per_second:]
    results_last_second = kmeans.fit(last_second_energy_bins.reshape(-1, 1))
    return (results_first_second.results_[0] + results_last_second.results_[0] / 2) / maximum_value
