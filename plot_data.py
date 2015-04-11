import os, codecs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


TIME = "Time"
TOTAL_DOCS_IN_GROUP = "Total documents in group"
TOPIC = "Topic"
FRACTION_DOCS = "Fractional documents in topic in group"


def get_data(fname):
    try:
        df = pd.read_csv(
            fname,
            sep=',',
            encoding='utf-8',
            index_col=TIME)
        return df
    except:
        raise


def save_topics(fname="tweets-topk.csv", output="topics_mapping.txt"):
    # Load id->topic file
    df = None
    try:
        df = pd.read_csv(
            fname,
            sep=',',
            encoding='utf-8',
            index_col=TOPIC
        )
    except:
        raise
    terms = ["Term 1", "Term 2", "Term 3", "Term 4",
             "Term 5", "Term 6", "Term 7", "Term 8",
             "Term 9", "Term 10", "Term 11", "Term 12",
             "Term 13", "Term 14", "Term 15", "Term 16",
             "Term 17", "Term 18", "Term 19", "Term 20"]

    with codecs.open(output, 'w', 'utf-8') as f:
        for topic, data in df.iterrows():
            words = []
            for term in terms:
                words.append(data[term])
            words_line = ",".join(words)
            f.write(" : ".join([str(topic), words_line]) + "\n")


def convert_actual_time_to_secs(times):
    converted_to_minutes = []
    for time in times:
        hour, minute = time.split(":")
        cal = (int(hour)-1)*60 + int(minute)
        converted_to_minutes.append(cal)
    return converted_to_minutes


if __name__ == "__main__":
    datas = get_data("tweets-slice-usage.csv")
    # Time
    # Save x-axis value for each topic
    data_to_plot = dict()
    for i, data in datas.iterrows():
        if data[TOPIC] not in data_to_plot.keys():
            data_to_plot[data[TOPIC]] = [["""{0}:{1}""".format(str(i)[0], str(i)[1:]), float(data[FRACTION_DOCS])]]
        else:
            data_to_plot[data[TOPIC]].append(["""{0}:{1}""".format(str(i)[0], str(i)[1:]), float(data[FRACTION_DOCS])])
    #converted_y_values_into_secs = convert_actual_time_to_secs(y_axis)
    y_values = [x for x in range(0, 180)]
    print "Number of Topics:", len(data_to_plot.keys())
    plt.ylabel("Topic strength")
    plt.xlabel("Minutes since the debate started")
    # Draw graphical representation of topics
    #save_topics()
    filter_out_topics = []
    lines = []
    # Draw lines
    for topic in data_to_plot.keys():
        if topic in filter_out_topics:
            continue
        pair_of_values = data_to_plot[topic]
        # Manipulate data to make it matplotlib compatible
        minutes, topic_strength = zip(*pair_of_values)
        minutes_converted = convert_actual_time_to_secs(minutes)
        line = plt.plot(minutes_converted, topic_strength, label=str(topic))
    plt.legend()
    # Plot graph
    plt.show()
    save_topics()
