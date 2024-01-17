import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the Excel file into a DataFrame
file_path =  "data/music_nonmusic.xlsx"
df = pd.read_excel(file_path)

# Extract 'group', 'bias', and 'threshold' columns
selected_columns = ['group(nonmusic=1, music=2)', 'bias', 'threshold']
df_selected = df[selected_columns]

# Rename the columns for easier handling
df_selected.columns = ['group', 'bias', 'threshold']

# Map numerical values to group labels
group_mapping = {1: 'nonmusic', 2: 'music'}
df_selected['group'] = df_selected['group'].map(group_mapping)

# Create a figure with subplots
fig, axs = plt.subplots(1, 2, figsize=(15, 6))

# Boxplot for 'bias'
sns.boxplot(x='group', y='bias', data=df_selected, palette='Set1', hue='group', ax=axs[0])
axs[0].set_title('Boxplot: Bias by Group')
axs[0].legend(title='Group')

# Add scatter plot for 'bias'
df_selected.loc[:, 'dummy'] = 'Scatter Plot'
sns.scatterplot(x='group', y='bias', data=df_selected[df_selected['dummy'] == 'Scatter Plot'], color='black', ax=axs[0], alpha=0.5, label='Scatter Plot')
df_selected.drop('dummy', axis=1, inplace=True)

# Boxplot for 'threshold'
sns.boxplot(x='group', y='threshold', data=df_selected, palette='Set2', hue='group', ax=axs[1])
axs[1].set_title('Boxplot: Threshold by Group')
axs[1].legend(title='Group')

# Add scatter plot for 'threshold'
df_selected.loc[:, 'dummy'] = 'Scatter Plot'
sns.scatterplot(x='group', y='threshold', data=df_selected[df_selected['dummy'] == 'Scatter Plot'], color='black', ax=axs[1], alpha=0.5, label='Scatter Plot')
df_selected.drop('dummy', axis=1, inplace=True)

plt.tight_layout()
plt.show()
