import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np

from utils import load_pickle, moving_average

matplotlib.rcParams['svg.fonttype'] = 'none'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Latin Modern Math'
matplotlib.rcParams['font.size'] = 10

# plt.figure(figsize=(3.5, HEIGHT)) one-column
# figsize=(7., HEIGHT) double-colum


class Plotter:
    def __init__(self):
        plt.figure(figsize=(3.5, 2.5))

    def plot_files(self,
                   *file_names,
                   param_name,
                   limit_x=None,
                   limit_x_range=None,
                   range_y=None,
                   y_ticks=None,
                   last_N=100,
                   legend=False):

        colors = ['blue', 'green', 'red', 'yellow', 'cyan']
        # import ipdb
        # ipdb.set_trace()
        for _ in range(len(file_names[0])):
            self.plot_general(
                file_name=file_names[0][_],
                param_name=param_name,
                color=colors[_],
                limit_x=limit_x,
                limit_x_range=limit_x_range,
                range_y=range_y,
                y_ticks=y_ticks,
                last_N=last_N,
            )
        if legend:
            patches = [
                mpatches.Patch(color=colors[_], label=file_names[0][_])
                for _ in range(len(file_names[0]))
            ]
            plt.legend(handles=patches)

    def plot_general(self,
                     file_name,
                     param_name,
                     last_N=100,
                     color='blue',
                     limit_x=None,
                     limit_x_range=None,
                     range_y=None,
                     y_ticks=None):
        # plt.rc('font', family='sans-serif')
        metadata = load_pickle(file_name)
        # import ipdb
        # ipdb.set_trace()
        score = metadata[param_name]
        mean, std = moving_average(score, last_N=last_N)
        if limit_x is not None:
            episodes = range(limit_x)
            mean = mean[:limit_x]
            std = std[:limit_x]
        elif limit_x_range is not None:
            episodes = metadata[limit_x_range]
            print(episodes)
        else:
            episodes = range(len(score))
            mean, std = moving_average(score, last_N=last_N)

        lower_bound = [a_i - 0.5 * b_i for a_i, b_i in zip(mean, std)]
        upper_bound = [a_i + 0.5 * b_i for a_i, b_i in zip(mean, std)]
        # plt.plot(episodes, score)
        plt.fill_between(episodes,
                         lower_bound,
                         upper_bound,
                         facecolor=color,
                         alpha=0.5)
        plt.plot(episodes, mean, color=color)
        if range_y is not None:
            plt.ylim(range_y)
        if y_ticks is not None:
            plt.yticks(np.arange(range_y[0], range_y[1] + 2 * y_ticks,
                                 y_ticks))
        if limit_x_range is not None:
            plt.xlabel(limit_x_range)
        else:
            plt.xlabel("episodes")
        plt.ylabel(param_name)

    def show(self):
        # plt.legend(loc='best')
        matplotlib.rcParams['font.size'] = 10
        plt.show()


if __name__ == '__main__':
    pp = Plotter()

    pp.plot_files(
        ['shield_updates_10_0', 'shield_updates_9_1', 'shield_updates_7_3'],
        param_name='shield_means',
        last_N=1,
        limit_x=200,
        limit_x_range=None,
        range_y=None,
        y_ticks=None,
        legend=True)

    # meta_data = {
    #     'score': [],
    #     'avg_return': [],
    #     'shield_means': [],
    #     'number_of_bad_engine_uses': [],
    #     'landed_inside': [],
    #     'number_of_crashes': [],
    #     'number_of_weird': []
    # }

    # pp.plot_files(['oracles_10_0', 'oracles_9_1', 'oracles_7_3'],
    #               param_name='kl',
    #               last_N=1,
    #               limit_x=None,
    #               limit_x_range=None,
    #               range_y=None,
    #               y_ticks=None,
    #               legend=True)

    # pp.plot_files(['means_vars_10_0', 'means_vars_9_1', 'means_vars_7_3'],
    #               param_name='means',
    #               last_N=1,
    #               limit_x=None,
    #               limit_x_range=None,
    #               range_y=None,
    #               y_ticks=None,
    #               legend=True)

    # pp.plot_files([
    #     'perfect_shield_21-02-2021 19:38:06',
    #     'without_shield_26-02-2021 22:25:35'
    # ],
    #               param_name='avg_return',
    #               last_N=100,
    #               limit_x=None,
    #               limit_x_range=None,
    #               range_y=None,
    #               y_ticks=None,
    #               legend=True)

    # unity
    # 'steps_return':
    # 'return':
    # 'steps_episode_lenght'
    # 'episode_lenght'

    # lunar landing
    # 'score'
    # 'avg_return'
    # 'shield_means'
    # 'number_of_bad_engine_uses'
    # 'landed_inside'

    # pp.plot_files(['0_25_6_ppl', '25_50_6_ppl', '50_75_6_ppl', '75_100_6_ppl'],
    #               param_name='episode_lenght',
    #               last_N=100,
    #               limit_x=None,
    #               limit_x_range='steps_episode_lenght',
    #               range_y=None,
    #               y_ticks=None,
    #               legend=True)

    # pp.plot_files(['00_25', '25_50', '50_75', '75_100'],
    #               param_name='return',
    #               last_N=100,
    #               limit_x=None,
    #               limit_x_range='steps_return',
    #               range_y=None,
    #               y_ticks=None,
    #               legend=True)

    # pp.plot_files(['0_25_6_ppl', '25_50_6_ppl', '50_75_6_ppl', '75_100_6_ppl'],
    #               param_name='return',
    #               last_N=100,
    #               limit_x=None,
    #               limit_x_range='steps_return',
    #               range_y=None,
    #               y_ticks=None,
    #               legend=True)

    pp.show()
