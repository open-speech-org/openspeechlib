import numpy as np
from sklearn.cluster import KMeans


def kmeans_first_and_last_second_minimum(energy_signal, bins_per_second, normalize=True, regularize_with=0):
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
    min_first_second = np.min(results_first_second.cluster_centers_)
    min_last_second = np.min(results_last_second.cluster_centers_)
    return ((min_first_second + min_last_second / 2) + regularize_with) / maximum_value
