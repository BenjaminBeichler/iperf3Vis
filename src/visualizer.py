import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt


def plot_ribbon_plot(data, interval_string, output_file):
    data.index = data.index.floor(interval_string)

    interval_data = pd.concat([
        data.groupby(data.index).quantile(0.05).rename(columns={"Upload Speed (MBit/s)": "q5"}),
        data.groupby(data.index).quantile(0.10).rename(columns={"Upload Speed (MBit/s)": "q10"}),
        data.groupby(data.index).quantile(0.25).rename(columns={"Upload Speed (MBit/s)": "q25"}),
        data.groupby(data.index).quantile(0.50).rename(columns={"Upload Speed (MBit/s)": "q50"}),
        data.groupby(data.index).quantile(0.75).rename(columns={"Upload Speed (MBit/s)": "q75"}),
        data.groupby(data.index).quantile(0.90).rename(columns={"Upload Speed (MBit/s)": "q90"}),
        data.groupby(data.index).quantile(0.95).rename(columns={"Upload Speed (MBit/s)": "q95"}),
    ], axis=1)

    # Disclaimer: This was written by @rkost while he did not know anything about altair.
    # Suggestions welcome!
    alt.data_transformers.disable_max_rows()
    line = alt.Chart(interval_data.reset_index()).mark_line().encode(
        x='index',
        y='q50:Q'
    ).properties(width=1000, height=500)
    area50 = alt.Chart(interval_data.reset_index()).mark_area(opacity=0.2).encode(
        x='index',
        y='q75',
        y2='q25'
    )
    area80 = alt.Chart(interval_data.reset_index()).mark_area(opacity=0.2).encode(
        x='index',
        y='q90',
        y2='q10'
    )
    area90 = alt.Chart(interval_data.reset_index()).mark_area(opacity=0.2).encode(
        x='index',
        y='q95',
        y2='q05'
    )
    scatter = alt.Chart(data.reset_index()).mark_point(opacity=0.05, filled=True).encode(
        x='index',
        y='Upload Speed (MBit/s)'
    )

    plot = (line + area50 + area80 + area90 + scatter)
    plot.show()


def plot_box_plot(data, interval_string, output_file):
    data.index = data.index.floor(interval_string)
    fig = plt.figure(figsize=(24, 9))
    sns.set(style="ticks")
    sns.boxplot(data.index, data["Upload Speed (MBit/s)"])
    plt.show()
    # plt.savefig(output_file)
