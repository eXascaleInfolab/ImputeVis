import json
from typing import List
import os
import numpy as np
import matplotlib.pyplot as plt

from Optimizer import util

LOWER_IS_BETTER = {'rmse', 'mae', 'time_taken'}  # Add other metrics to this set if needed
ONE_IS_BEST = ["corr"]


def compare_results(default_file_path: str, optimized_file_path: str, algorithm: str):
    """
    Compare the metrics and time taken for the 'cdrec' algorithm in the default settings
    versus the optimized settings and plot the results.

    Parameters
    ----------
    default_file_path : str
        Path to the JSON file containing the default settings results.
    optimized_file_path : str
        Path to the JSON file containing the optimized settings results.
    algorithm : str
        The used algorithm. This is used to name the output files.

    Returns
    -------
    None
        The function will plot the results, save them as PNG in the "figures" directory,
        and does not return any value.
    """

    # Load the JSON files
    with open(default_file_path, "r") as file:
        default_results = json.load(file)

    with open(optimized_file_path, "r") as file:
        optimized_results = json.load(file)

    # Prepare data for plotting
    # metrics = ['rmse_mae', 'mi_corr', 'rmse', 'mae', 'mi', 'corr', 'time_taken']
    metrics = ['rmse', 'mae', 'mi', 'corr', 'time_taken']
    default_values = {}
    optimized_values = {}

    for key, value in default_results.items():
        if key not in default_values:
            default_values[key] = {}
        for metric in metrics:
            default_values[key][metric] = value[metric]

    for key, value in optimized_results.items():
        prefix = key.rsplit('_', 1)[0]  # extract the prefix e.g. 'bafu' from 'bafu_corr'
        if prefix not in optimized_values:
            optimized_values[prefix] = {}
        for metric in metrics:
            # Take the mean of the metrics for different optimization settings
            if metric not in optimized_values[prefix]:
                optimized_values[prefix][metric] = []
            optimized_values[prefix][metric].append(value[metric])

    # Initialize a dictionary to keep track of the index of the best result for each dataset
    best_index_dict = {}

    # Plot the results
    for metric in metrics:
        plt.figure(figsize=(10, 5))
        labels = list(default_values.keys())
        default_metric_values = [default_values[label][metric] for label in labels]

        # Choose the best value from optimized variants
        if metric in LOWER_IS_BETTER:
            optimized_metric_values = []
            for label in labels:
                best_value_index = optimized_values[label][metric].index(min(optimized_values[label][metric]))
                best_index_dict[label] = best_value_index
                optimized_metric_values.append(optimized_values[label][metric][best_value_index])
        elif metric in ONE_IS_BEST:
            optimized_metric_values = []
            for label in labels:
                # Find the value with the smallest absolute difference from 1
                differences_from_one = [abs(value - 1) for value in optimized_values[label][metric]]
                best_value_index = differences_from_one.index(min(differences_from_one))
                best_index_dict[label] = best_value_index
                optimized_metric_values.append(optimized_values[label][metric][best_value_index])

        else:
            optimized_metric_values = []
            for label in labels:
                best_value_index = optimized_values[label][metric].index(max(optimized_values[label][metric]))
                best_index_dict[label] = best_value_index
                optimized_metric_values.append(optimized_values[label][metric][best_value_index])

        if metric == "time_taken":
            optimized_metric_values = [optimized_values[label][metric][best_index_dict[label]] for label in labels]

        # Check if it's time_taken and adjust label and units accordingly
        if metric == "time_taken":
            metric_display = "Time"
            ylabel = "Time [s]"
        else:
            metric_display = metric.upper()
            ylabel = metric_display

        # Define bar positions
        ind = np.arange(len(labels))
        width = 0.35

        labels = [label.title() for label in default_values.keys()]  # Title case looks better
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - width / 2, default_metric_values, width, label='Default')
        rects2 = ax.bar(ind + width / 2, optimized_metric_values, width, label='Optimized')

        ax.set_ylabel(ylabel)
        #ax.set_title(f'{algorithm} {metric_display}: Author vs. Optimized')

        # Set the tick positions and labels
        ax.set_xticks(ind)
        ax.set_xticklabels(labels)

        ax.legend()
        plt.tight_layout()

        # Save the figure to the 'figures' folder with a descriptive name
        file_name = f"figures/{algorithm}_comparison_of_{metric}_default_vs_optimized.png"
        plt.savefig(file_name)
        plt.show()


def plot_comparison_by_dataset(default_file_path: str, optimized_file_path: str, title_prefix: str = 'Dataset') -> None:
    """
    Plot the comparison of metrics for default and optimized data.

    Parameters
    ----------
    default_file_path : str
        Path to the JSON file containing default results.
    optimized_file_path : str
        Path to the JSON file containing optimized results.
    title_prefix : str, optional
        Prefix for the plot title, by default 'Dataset'.

    Returns
    -------
    None
        The function saves the plots to the 'figures' directory and displays them.
    """

    # Load the JSON files
    with open(default_file_path, "r") as file:
        default_results = json.load(file)

    with open(optimized_file_path, "r") as file:
        optimized_results = json.load(file)

    # Prepare data for plotting
    # metrics = ['rmse_mae', 'mi_corr', 'rmse', 'mae', 'mi', 'corr', 'time_taken']
    metrics = ['rmse', 'mae', 'mi', 'corr', 'time_taken']
    default_values = {}
    optimized_values = {}

    for key, value in default_results.items():
        if key not in default_values:
            default_values[key] = {}
        for metric in metrics:
            default_values[key][metric] = value[metric]

    for key, value in optimized_results.items():
        prefix = key.rsplit('_', 1)[0]  # extract the prefix e.g. 'bafu' from 'bafu_corr'
        if prefix not in optimized_values:
            optimized_values[prefix] = {}
        for metric in metrics:
            # Take the mean of the metrics for different optimization settings
            if metric not in optimized_values[prefix]:
                optimized_values[prefix][metric] = []
            optimized_values[prefix][metric].append(value[metric])

    # Initialize a dictionary to keep track of the index of the best result for each dataset
    best_index_dict = {}

    # Determine the best index for each dataset
    for label in default_values.keys():
        for metric in metrics:
            if metric in LOWER_IS_BETTER:
                best_value_index = optimized_values[label][metric].index(min(optimized_values[label][metric]))
            elif metric in ONE_IS_BEST:
                differences_from_one = [abs(value - 1) for value in optimized_values[label][metric]]
                best_value_index = differences_from_one.index(min(differences_from_one))
            else:
                best_value_index = optimized_values[label][metric].index(max(optimized_values[label][metric]))

            best_index_dict[label] = best_value_index

    # For each dataset, plot all metrics side by side
    for label in default_values.keys():
        ind = np.arange(len(metrics))
        width = 0.35

        # Get metric values for both default and optimized results
        default_metric_values = [default_values[label][metric] for metric in metrics]
        optimized_metric_values = [optimized_values[label][metric][best_index_dict[label]] for metric in metrics]

        fig, ax = plt.subplots(figsize=(10, 5))
        rects1 = ax.bar(ind - width / 2, default_metric_values, width, label='Default')
        rects2 = ax.bar(ind + width / 2, optimized_metric_values, width, label='Optimized')

        # Adjust the y-labels based on metrics
        metric_display_labels = ["Time [s]" if metric == "time_taken" else metric.upper() for metric in metrics]

        ax.set_ylabel('Value')
        #ax.set_title(f'{title_prefix} Metrics Comparison: {label.title()}')
        ax.set_xticks(ind)
        ax.set_xticklabels(metric_display_labels)
        ax.legend()

        plt.tight_layout()

        # Save the figure to the 'figures' folder with a descriptive name
        file_name = f"figures/dataset/all_{label}_comparison_of_metrics_default_vs_optimized.png"
        plt.savefig(file_name)
        plt.show()


def plot_best_algorithm_by_dataset_old(optimized_file_path: str, title_prefix: str = 'Dataset') -> None:
    """
    Plot the best algorithm for each metric in a dataset.

    Parameters
    ----------
    optimized_file_path : str
        Path to the JSON file containing optimized results.
    title_prefix : str, optional
        Prefix for the plot title, by default 'Dataset'.

    Returns
    -------
    None
        The function saves the plots to the 'figures' directory and displays them.
    """

    # Load the JSON file
    with open(optimized_file_path, "r") as file:
        optimized_results = json.load(file)

    # Prepare data for plotting
    metrics = ['rmse', 'mae', 'mi', 'corr', 'time_taken']

    # Extract dataset, algorithm, and configuration names
    datasets = set(key.split('_')[0] for key in optimized_results.keys())
    algorithms = set(key.split('_')[1] for key in optimized_results.keys())

    best_config_dict = {}

    for dataset in datasets:
        best_config_dict[dataset] = {}
        for algorithm in algorithms:
            best_config_dict[dataset][algorithm] = {}
            for metric in metrics:
                try:
                    value = optimized_results[f"{dataset}_{algorithm}"][metric]
                    best_config_dict[dataset][algorithm][metric] = value
                except KeyError:
                    continue

    # Plot the results
    for dataset in datasets:
        ind = np.arange(len(metrics))
        width = 0.15
        positions = [ind + i * width for i in range(len(algorithms))]

        fig, ax = plt.subplots(figsize=(12, 5))

        for idx, algorithm in enumerate(algorithms):
            algorithm_values = [best_config_dict[dataset][algorithm][metric] for metric in metrics]
            ax.bar(positions[idx], algorithm_values, width, label=util.mapper(algorithm))

        metric_display_labels = ["Time [s]" if metric == "time_taken" else metric.upper() for metric in metrics]

        ax.set_ylabel('Value')
        #ax.set_title(f'{title_prefix} Best Configuration per Algorithm for Metrics: {dataset.title()}')
        ax.set_xticks(ind + width * (len(algorithms) - 1) / 2)  # Center the tick marks under the group of bars
        ax.set_xticklabels(metric_display_labels)
        ax.legend()

        plt.tight_layout()

        # Save the figure to the 'figures' folder with a descriptive name
        file_name = f"figures/best_config_{dataset}_per_algorithm.png"
        plt.savefig(file_name)
        plt.show()


def plot_best_algorithm_by_dataset(optimized_paths: List[str], algorithm_names: List[str],
                                   title_prefix: str = 'Dataset') -> None:
    """
    Plot the comparison of metrics for the best performing configuration of each algorithm side by side.

    Parameters
    ----------
    optimized_paths : List[str]
        List of paths to the JSON files containing optimized results for each algorithm.
    algorithm_names : List[str]
        Names of the algorithms corresponding to the optimized paths.
    title_prefix : str, optional
        Prefix for the plot title, by default 'Dataset'.

    Returns
    -------
    None
        The function saves the plots to the 'figures' directory and displays them.
    """

    # Metrics to consider
    metrics = ['rmse', 'mae', 'mi', 'corr', 'time_taken']

    # Dictionary to store the best values for each algorithm and dataset
    best_values = {}

    # Go through each optimized path and determine the best values
    for path, algorithm in zip(optimized_paths, algorithm_names):
        with open(path, "r") as file:
            results = json.load(file)

        for key, values in results.items():
            dataset = key.rsplit('_', 1)[0]  # Extract dataset name

            if dataset not in best_values:
                best_values[dataset] = {}

            best_values[dataset][algorithm] = {}
            for metric in metrics:
                best_values[dataset][algorithm][metric] = values[metric]

    # Plotting
    for dataset, dataset_values in best_values.items():
        ind = np.arange(len(metrics))
        width = 0.35 / len(algorithm_names)  # Adjust width based on the number of algorithms

        fig, ax = plt.subplots(figsize=(10, 5))

        for idx, (algorithm, algo_values) in enumerate(dataset_values.items()):
            metric_values = [algo_values[metric] for metric in metrics]
            rects = ax.bar(ind + width * idx, metric_values, width, label=util.mapper(algorithm))

        # Adjust the y-labels based on metrics
        metric_display_labels = ["Time [s]" if metric == "time_taken" else metric.upper() for metric in metrics]

        ax.set_ylabel('Value')
        #ax.set_title(f'{title_prefix} Metrics Comparison: {dataset.title()}')
        ax.set_xticks(ind + width * (len(algorithm_names) - 1) / 2)  # Adjust xticks position
        ax.set_xticklabels(metric_display_labels)
        ax.legend()

        plt.tight_layout()

        # Save the figure to the 'figures' folder with a descriptive name
        file_name = f"figures/dataset/{dataset}_comparison_of_best_configs.png"
        plt.savefig(file_name)
        plt.show()


def plot_best_algorithm_by_dataset(optimized_file_paths: list) -> None:
    grouped_metrics = [['rmse', 'mae'], ['mi', 'corr']]
    special_metrics = ['time_taken']
    dataset_metrics_results = {}

    # 1. Data Extraction
    for file_path in optimized_file_paths:
        with open(file_path, 'r') as f:
            results = json.load(f)

        for key, value in results.items():
            dataset, metric_used_for_optimization = key.split('_', 1)
            if metric_used_for_optimization not in ["rmse_mae", "mi_corr"]:
                continue
            algorithm = value['algorithm']

            if dataset not in dataset_metrics_results:
                dataset_metrics_results[dataset] = {}
            if metric_used_for_optimization not in dataset_metrics_results[dataset]:
                dataset_metrics_results[dataset][metric_used_for_optimization] = {}

            # Store the results for this algorithm
            all_metrics = [metric for group in grouped_metrics for metric in group] + special_metrics
            dataset_metrics_results[dataset][metric_used_for_optimization][algorithm] = {
                metric: value[metric] for metric in all_metrics
            }

    # 2. Plotting
    for dataset, metrics_data in dataset_metrics_results.items():
        for metric_used_for_optimization, algorithms_data in metrics_data.items():
            for metric_group in grouped_metrics:
                plot_metrics(dataset, metric_used_for_optimization, algorithms_data, metric_group, width_factor=0.5)
            # Plot special metrics
            plot_metrics(dataset, metric_used_for_optimization, algorithms_data, special_metrics, width_factor=0.5,
                         log_scale=True)


def plot_metrics(dataset, metric_used_for_optimization, algorithms_data, metrics_to_use, width_factor=1.0,
                 log_scale=False):
    ind = np.arange(len(metrics_to_use))
    width = 0.35 / len(algorithms_data)

    fig, ax = plt.subplots(figsize=(10 * width_factor, 4.75))
    for idx, (algorithm, algo_values) in enumerate(algorithms_data.items()):
        metric_values = [algo_values[metric] for metric in metrics_to_use]
        rects = ax.bar(ind + width * idx, metric_values, width, label=util.mapper(algorithm))

    metric_display_labels = ["Time [s]" if metric == "time_taken" else metric.upper() for metric in metrics_to_use]

    ax.set_ylabel('Value')
    #ax.set_title(f'{dataset.title()} - Params Optimized on {util.mapper(metric_used_for_optimization).upper().replace("_", " & ")}')

    if log_scale:
        ax.set_yscale('log')
        ax.set_ylabel('Time [s]')  # Adjusting the y-label to reflect the log scale
        ax.set_xticks([])
        ax.set_xticklabels([])
    else:
        ax.set_xticks(ind + width * (len(algorithms_data) - 1) / 2)
        ax.set_xticklabels(metric_display_labels)

    ax.legend()

    plt.tight_layout()
    suffix = "_".join(metrics_to_use)
    plt.savefig(f"figures/dataset/{dataset}_comparison_{metric_used_for_optimization}_{suffix}.png", dpi=500)
    # plt.show()
    plt.close()


def plot_optimization_comparison(input_file_path: str,
                                 output_plot_path: str,
                                 algorithm_code: str,
                                 width: int,
                                 height: int,
                                 dpi: int) -> None:
    """
    Create comparison plots for different optimization methods across datasets.

    Parameters
    ----------
    input_file_path : str
        Path to the JSON file containing optimization results.
    output_plot_path : str
        Directory where generated plots will be saved.
    algorithm_code : str
        String representing the algorithm code. Used in plot title and filename.
    width : int
        Width of the generated plot.
    height : int
        Height of the generated plot.
    dpi : int
        Dots-per-inch setting for the generated plot.

    Returns
    -------
    None
        The function saves plots to the specified directory and does not return any values.

    """
    with open(input_file_path, 'r') as file:
        data = json.load(file)

    optimization_methods = list(data.keys())
    datasets = list(data[optimization_methods[0]].keys())
    datasets_labels = [name.title() for name in datasets]
    metrics = ["rmse", "mae", "mi", "corr", "time_taken"]

    bar_width = 0.25  # adjust this as needed based on the number of optimization methods
    index = np.arange(len(datasets))

    for metric in metrics:
        plt.figure(figsize=(width, height), dpi=dpi)

        for idx, opt_method in enumerate(optimization_methods):
            values = [data[opt_method][dataset][metric] for dataset in datasets]
            plt.bar(index + idx * bar_width, values, bar_width, label=util.mapper(opt_method))

        #plt.title(f'Comparison of {metric.upper()} for {algorithm_code}')
        plt.xlabel('Dataset')
        plt.ylabel(metric.upper())
        plt.xticks(index + bar_width, datasets_labels)  # to center the tick labels
        # Check if the metric is rmse or mae and set the y-axis to logarithmic scale
        if metric in ["rmse", "mae"]:
            plt.yscale("log")
            plt.grid(True, which="major", axis="y", ls="--", alpha=0.5)
        else:
            plt.grid(True, which="both", axis="y", ls="--")

        # Extract legend handles and labels for later use
        legend_handles, legend_labels = plt.gca().get_legend_handles_labels()

        #plt.legend(loc='lower right', fontsize='x-small')
        plt.tight_layout()
        # plt.show()
        plt.savefig(f'{output_plot_path}/{algorithm_code}_{metric}.png')
        plt.close()

    # Saving legend separately
    if legend_handles and legend_labels:
        fig_legend = plt.figure(figsize=(width, 1), dpi=400)  # adjust the height for a horizontal legend
        plt.figlegend(legend_handles, legend_labels, loc='center', ncol=len(legend_handles))
        fig_legend.savefig(f'{output_plot_path}/optimization-legend-horizontal.png', dpi=400, bbox_inches='tight')
        plt.close(fig_legend)


def plot_across_mcar_rates(metric: str, output_file_path: str,
                           width: int = 10, height: int = 6.5, dpi: int = 400) -> None:
    """
    Plots the metric across different MCAR rates for all datasets and algorithms.

    Parameters
    ----------
    metric : str
        The metric name (e.g., 'rmse') to plot.
    output_file_path : str
        Directory path to save the plots.
    width : int, optional
        Width of the plot, by default 10.
    height : int, optional
        Height of the plot, by default 6.
    dpi : int, optional
        Dots per inch for the saved plot, by default 100.
    """
    algorithms = ["cdrec", "iim", "mrnn", "stmvl"]
    datasets = ["bafu", "chlorine", "climate", "drift", "meteo"]
    mcar_rates = [1, 5, 10, 20, 40, 80]
    base_path = "results/{alg}/{alg}_optimized_summary_results_mcar_{mcar}.json"

    # Loop through each dataset
    for dataset in datasets:
        plt.figure(figsize=(width, height))
        # Loop through each algorithm
        for alg in algorithms:
            y_values = []
            for mcar_rate in mcar_rates:
                file_path = base_path.format(alg=alg, mcar=mcar_rate)
                result = util.read_json_for_metric(file_path, dataset + "_rmse_mae")
                y_values.append(result[metric])
            plt.plot(mcar_rates, y_values, label=util.mapper(alg), marker='o')

        #plt.title(f"{dataset.capitalize()} - {util.mapper(metric)} across MCAR Scenarios")
        plt.xlabel('MCAR Rate')
        plt.ylabel(util.mapper(metric))
        # plt.legend(fontsize='small')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.xticks(mcar_rates)

        file_name = f"{dataset}_{metric}_across_mcar_rates.png"
        plt.savefig(os.path.join(output_file_path, file_name), dpi=dpi)
        plt.close()


def save_legend_only(output_file_path: str, dpi: int = 100) -> None:
    """
    Generates and saves only the legend using representative data.

    Parameters
    ----------
    output_file_path : str
        Directory path to save the legend.
    dpi : int, optional
        Dots per inch for the saved legend, by default 100.
    """
    algorithms = ["cdrec", "iim", "mrnn", "stmvl"]
    mcar_rate = 1  # representative MCAR rate
    dataset = "bafu"  # representative dataset
    metric = "rmse"  # representative metric
    base_path = "results/{alg}/{alg}_optimized_summary_results_mcar_{mcar}.json"

    plt.figure(figsize=(10, 2))  # Adjust for desired legend size
    for alg in algorithms:
        file_path = base_path.format(alg=alg, mcar=mcar_rate)
        result = util.read_json_for_metric(file_path, dataset + "_rmse_mae")
        plt.plot([0, 1], [result[metric], result[metric]], label=util.mapper(alg))

    # Create horizontal legend
    legend = plt.legend(loc='center', frameon=False)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig(os.path.join(output_file_path, "legend_only.png"), dpi=dpi, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    # algorithm_names = ["CDRec",
    #                    "IIM",
    #                    "M-RNN",
    #                    "ST-MVL"]
    # filename_patterns = ["cdrec",
    #                      "iim",
    #                      "mrnn",
    #                      "stmvl"]
    #
    # for algo, pattern in zip(algorithm_names, filename_patterns):
    #     default_path = f"./results/{pattern}/{pattern}_default_summary_results.json"
    #     optimized_path = f"./results/{pattern}/{pattern}_optimized_summary_results.json"
    #     # compare_results(default_path, optimized_path, algo)
    #     # plot_comparison_by_dataset(default_path, optimized_path, 'DataSet')
    #     # plot_best_algorithm_by_dataset_old(optimized_path, 'DataSet')
    #     optimizations_path = f"./results/{pattern}/optimization/{pattern}_optimization_results_summary.json"
    #     plot_optimization_comparison(optimizations_path, f"figures/optimizations/{pattern}/", algo, width=4, height=4,
    #                                  dpi=400)

    # optimized_paths = [f"./results/{pattern}/{pattern}_optimized_summary_results.json" for pattern in filename_patterns]
    # plot_best_algorithm_by_dataset(optimized_paths, algorithm_names, 'DataSet')
    # plot_best_algorithm_by_dataset(optimized_paths)

    for metric_to_plot in ["rmse", "mi", "corr", "time_taken"]:
        plot_across_mcar_rates(metric_to_plot, 'figures/scenario', width=6, height=3.6, dpi=400)
    save_legend_only('figures/scenario', dpi=400)
