import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np
from utils import running_mean

from utils import load_pickle, moving_average, save_pickle

matplotlib.rcParams['svg.fonttype'] = 'none'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Latin Modern Math'
matplotlib.rcParams['font.size'] = 10

# plt.figure(figsize=(3.5, HEIGHT)) one-column
# figsize=(7., HEIGHT) double-colum


class Plotter:

	def __init__(self):
		# plt.figure(figsize=(3.5, 2.5))
		plt.figure(figsize=(5.25, 3.75))

	def plot_files(self, *file_names, param_name, limit_x=None, limit_x_range=None, range_y=None, y_ticks=None, last_N=100, legend=False, x_label=None, just_mean=False):

		colors = ['blue', 'green', 'red', 'yellow', 'cyan', 'orange', 'olive', 'purple']
		# import ipdb
		# ipdb.set_trace()
		for _ in range(len(file_names[0])):
			self.plot_general(file_name=file_names[0][_],
			                  param_name=param_name,
			                  color=colors[_],
			                  limit_x=limit_x,
			                  limit_x_range=limit_x_range,
			                  range_y=range_y,
			                  y_ticks=y_ticks,
			                  last_N=last_N,
			                  x_label=x_label,
			                  just_mean=just_mean)
		if legend:
			patches = [mpatches.Patch(color=colors[_], label=file_names[0][_]) for _ in range(len(file_names[0]))]
			plt.legend(handles=patches)

	def plot_general(self, file_name, param_name, last_N=100, color='blue', limit_x=None, limit_x_range=None, range_y=None, y_ticks=None, x_label=None, just_mean=False):
		# plt.rc('font', family='sans-serif')
		metadata = load_pickle(file_name)

		# import ipdb
		# ipdb.set_trace()
		score = metadata[param_name]
		# if not just_mean:
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
			if not just_mean:
				mean, std = moving_average(score, last_N=last_N)
			else:
				mean = running_mean(score, last_N)

		if not just_mean:
			multiplier_std = 0.1
			lower_bound = [a_i - multiplier_std * b_i for a_i, b_i in zip(mean, std)]
			upper_bound = [a_i + multiplier_std * b_i for a_i, b_i in zip(mean, std)]
			plt.fill_between(episodes, lower_bound, upper_bound, facecolor=color, alpha=0.5)

		# plt.plot(episodes, score)
		plt.ylabel(param_name)
		if range_y is not None:
			plt.ylim(range_y)
		if y_ticks is not None:
			plt.yticks(np.arange(range_y[0], range_y[1] + 2 * y_ticks, y_ticks))
		if x_label is not None:
			plt.xlabel(limit_x_range)
		else:
			plt.xlabel("episodes")
		plt.xlabel("steps")
		# import ipdb
		# ipdb.set_trace()
		# mean[8000:] = [0] * (len(mean) - 1801)
		if not just_mean:
			# raise "WHAT THE FUCK"
			multiplier_std = 0.5
			lower_bound = [a_i - multiplier_std * b_i for a_i, b_i in zip(mean, std)]
			upper_bound = [a_i + multiplier_std * b_i for a_i, b_i in zip(mean, std)]
			plt.fill_between(episodes, lower_bound, upper_bound, facecolor=color, alpha=0.5)

		# import ipdb
		# ipdb.set_trace()
		plt.plot(episodes[:len(mean)], mean, color=color)

	def show(self):
		# plt.legend(loc='best')
		matplotlib.rcParams['font.size'] = 10
		plt.show()


if __name__ == '__main__':
	pp = Plotter()

	# pp.plot_files(['run_optimal_policy', 'run_reward_model'],
	#               param_name='return',
	#               last_N=200,
	#               limit_x=10000,
	#               limit_x_range=None,
	#               range_y=None,
	#               y_ticks=None,
	#               legend=True,
	#               just_mean=False)
	# pp.plot_files(['100'], param_name='loss', last_N=100, limit_x=None, limit_x_range=None, range_y=None, y_ticks=None, legend=True)
	# metadata = load_pickle("99")
	# line_1 = {'accuracy': [], 'loss': []}
	# line_1['accuracy'] = [1.0 for _ in range(len(metadata['loss']))]
	# line_1['loss'] = [1.0 for _ in range(len(metadata['loss']))]
	# save_pickle(line_1, "line_1")
	pp.plot_files(['100', '98', '95', '90', '80'],
	              param_name='accuracy',
	              last_N=100,
	              limit_x=None,
	              limit_x_range=None,
	              range_y=None,
	              y_ticks=None,
	              legend=True,
	              x_label="steps",
	              just_mean=True)

	# pp.plot_files(['sarl', 'sarl_pref'],
	#               param_name='time_per_episode',
	#               last_N=200,
	#               limit_x=None,
	#               limit_x_range=None,
	#               range_y=None,
	#               y_ticks=None,
	#               legend=True,
	#               x_label="episodes",
	#               just_mean=True)

	# pp.plot_files(['cadrl', 'cadrl_pref'],
	#               param_name='time_per_episode',
	#               last_N=200,
	#               limit_x=None,
	#               limit_x_range=None,
	#               range_y=None,
	#               y_ticks=None,
	#               legend=True,
	#               x_label="steps",
	#               just_mean=True)

	# metadata['reward'] = train_reward
	# metadata['collision_rate'] = train_cr
	# metadata['sucess_rate'] = train_sr
	# metadata['time_per_episode'] = train_time

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
