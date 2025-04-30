from main import *
from unittest.mock import patch
from json_functions import *
import matplotlib.pyplot as plt
import numpy as np

def evaluate_ai_no_bag():
    score_list = []
    num_lines_cleared_list =[]
    for i in range(10):
        with patch('builtins.input', side_effect=['2', 'y']):
            num_lines_cleared = do_tetris(score_list=score_list)
        num_lines_cleared_list.append(num_lines_cleared)
        print(score_list)
        average_score = sum(score_list) / len(score_list)
        print(average_score)  # Output: 3.0

        avg_lines_cleared = sum(num_lines_cleared_list) / len(num_lines_cleared_list)

        json_dict = {'bag_on?': "False",
                     'iteration': i,
                     "num_lines_cleared": num_lines_cleared,
                     "avg_lines_cleared": avg_lines_cleared,
                     'score': score_list[-1],
                     'avg_score': average_score,
                     "avg_points_per_line_cleared": (average_score/avg_lines_cleared)}
        append_to_json_file("./eval_ai_no_bag.json", json_dict)

def evaluate_ai_with_bag():
    score_list = []
    num_lines_cleared_list =[]
    for i in range(10):
        with patch('builtins.input', side_effect=['2', 'n']):
            num_lines_cleared = do_tetris(score_list=score_list)
        num_lines_cleared_list.append(num_lines_cleared)
        print(score_list)
        average_score = sum(score_list) / len(score_list)
        print(average_score)  # Output: 3.0

        avg_lines_cleared = sum(num_lines_cleared_list) / len(num_lines_cleared_list)

        json_dict = {'bag_on?': "True",
                     'iteration': i,
                     "num_lines_cleared": num_lines_cleared,
                     "avg_lines_cleared": avg_lines_cleared,
                     'score': score_list[-1],
                     'avg_score': average_score,
                     "avg_points_per_line_cleared": (average_score/avg_lines_cleared)}
        append_to_json_file("./eval_ai_with_bag.json", json_dict)


def plot_file_group_comparison(file1, file2, label1="File 1", label2="File 2"):
    data1 = load_filtered_metrics(file1)
    data2 = load_filtered_metrics(file2)

    metrics = ['avg_score', 'avg_num_lines_cleared', 'avg_points_per_line_cleared']
    display_names = ['Avg Score', 'Avg Lines Cleared', 'Avg Points/Line']

    # Compute actual averages
    def average(data, key):
        return sum(d[key] for d in data) / len(data)

    avg1 = [average(data1, m) for m in metrics]
    avg2 = [average(data2, m) for m in metrics]

    # Normalize per-metric (column-wise)
    norm1 = []
    norm2 = []
    for i in range(len(metrics)):
        max_val = max(avg1[i], avg2[i])
        norm1.append(avg1[i] / max_val)
        norm2.append(avg2[i] / max_val)

    # Plotting
    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 6))
    bars1 = ax.bar(x - width/2, norm1, width, label=label1)
    bars2 = ax.bar(x + width/2, norm2, width, label=label2)

    ax.set_ylabel("Relative Height (Per Metric)")
    ax.set_title("Comparison of Tetris Metrics Over 10 Runs (Independently Normalized)")
    ax.set_xticks(x)
    ax.set_xticklabels(display_names)
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    # Annotate bars with actual values
    for i in range(len(metrics)):
        ax.annotate(f'{avg1[i]:.0f}', (x[i] - width/2, norm1[i]),
                    textcoords="offset points", xytext=(0, 3),
                    ha='center', fontsize=9)
        ax.annotate(f'{avg2[i]:.0f}', (x[i] + width/2, norm2[i]),
                    textcoords="offset points", xytext=(0, 3),
                    ha='center', fontsize=9)

    plt.tight_layout()
    fig.savefig("my_plot.png")
    plt.show()

if __name__ == '__main__':
    plot_file_group_comparison("./eval_ai_with_bag.json", "./eval_ai_no_bag.json",
                               label1="performance with bag", label2="performance without bag")