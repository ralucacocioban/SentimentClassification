def split_dataset(dataset, factor):
    limit = int(len(dataset) * factor)
    return dataset[:limit], dataset[limit:]
