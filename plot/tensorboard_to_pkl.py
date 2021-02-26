# tensorboard dev upload --logdir <logdir>.

from packaging import version

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats
import tensorboard as tb

major_ver, minor_ver, _ = version.parse(tb.__version__).release
assert major_ver >= 2 and minor_ver >= 3, \
    "This notebook requires TensorBoard 2.3 or later."
print("TensorBoard version: ", tb.__version__)

experiment_name = "0_25_6_ppl"
experiment_id = "IjHdr6FkQQWrYBGQwuXnsQ"
experiment = tb.data.experimental.ExperimentFromDev(experiment_id)
df = experiment.get_scalars()
df = df.drop(['run'], axis=1)
df_return = df.loc[df['tag'] == 'Environment/Cumulative Reward']
df_episode_lenght = df.loc[df['tag'] == 'Environment/Episode Length']

print(df)

df_return_dict = df_return.to_dict('list')
df_episode_lenght = df_episode_lenght.to_dict('list')

metadata = {
    'steps_return': df_return_dict['step'],
    'return': df_return_dict['value'],
    'steps_episode_lenght': df_episode_lenght['step'],
    'episode_lenght': df_episode_lenght['value']
}

from utils import save_pickle
save_pickle(metadata, experiment_name)
