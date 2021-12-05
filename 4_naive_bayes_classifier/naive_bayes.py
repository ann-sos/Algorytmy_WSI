import numpy as np
import pandas as pd


def proportion_split_dataset(dataset: pd.DataFrame, proportion: float):
    # split dataset into k sets
    training_df = dataset.sample(frac=proportion)
    testing_df = dataset.drop(training_df.index)
    return training_df, testing_df


def k_split_dataset(dataset: pd.DataFrame, k: int) -> list:
    # randomly sort the dataset
    dataset = dataset.sample(frac=1)
    # split dataset into k sets
    return np.array_split(dataset, k)


class NaiveBayes:
    def __init__(self, training_set):
        self.wine_df = training_set
        self.features_list = self.wine_df.columns[:-1].values.tolist()
        # list quality values that are present in the training set
        self.quality_values = sorted(self.wine_df["quality"].unique().tolist())
        # calculate number of instances of any class: how many wines of a quality X are in the dataset
        self.class_instances = {}
        self.class_probabilities = {}
        for qv in self.quality_values:
            self.class_instances[qv] = self.wine_df[self.wine_df["quality"] == qv].shape[0]
            self.class_probabilities[qv] = self.class_instances[qv] / self.wine_df.shape[0]

    def likelihood(self, feature_name, feature_value, target_class):
        feature = self.wine_df.loc[self.wine_df["quality"] == target_class, feature_name]
        return 1 / np.sqrt(2 * np.pi * feature.std() ** 2) * np.exp(
            -0.5 * ((feature_value - feature.mean()) / (feature.std())) ** 2)

    def naive_bayes(self, dataset: pd.DataFrame):
        calculated_predictions = {}
        for qv in self.quality_values:
            probability = self.class_probabilities[qv]
            for ftr in self.features_list:
                probability *= self.likelihood(ftr, dataset[ftr], qv)
            calculated_predictions[qv] = probability
        return pd.DataFrame(calculated_predictions).idxmax(axis=1)


def simple_validation(file, proportion):
    # import dataset
    wine_df = pd.read_csv(file, delimiter=";")
    # split dataset
    wine_training_df, wine_testing_df = proportion_split_dataset(wine_df, proportion)
    # initialise the classifier instance with the training set
    myBayes = NaiveBayes(wine_training_df)
    # run classifier for testing set
    nb = myBayes.naive_bayes(wine_testing_df)
    # compare results with expected values
    jb = pd.DataFrame({'calculated': nb, 'real': wine_testing_df['quality'],
                       'isRight': nb == wine_testing_df['quality']})
    # calculate accuracy
    vc = jb.isRight.value_counts()

    #print(f'Accuracy: {vc[True] / (vc[True] + vc[False]):.2f}')
    return vc[True] / (vc[True] + vc[False])


def cross_validation(file, k):
    accuracy = []
    # import dataset
    wine_df = pd.read_csv(file, delimiter=";")
    # split dataset
    datasets = k_split_dataset(wine_df, 5)
    for dset in datasets:
        # initialise the classifier instance with the training set
        training_dset = wine_df[~wine_df.isin(dset)].dropna(how='all')
        myBayes = NaiveBayes(training_dset)
        # run classifier for testing set
        nb = myBayes.naive_bayes(dset)
        # compare results with expected values
        jb = pd.DataFrame({'calculated': nb, 'real': dset['quality'],
                           'isRight': nb == dset['quality']})
        # calculate accuracy
        vc = jb.isRight.value_counts()
        a = vc[True] / (vc[True] + vc[False])
        accuracy.append(a)
        #print(f'Accuracy: {a:.2f}')
    return np.mean(accuracy)


if __name__ == "__main__":
    sv = simple_validation(r'winequality-white.csv', 0.6)
    print(f'Simple validation accuracy: {sv:.3f}', )
    cv = cross_validation(r'winequality-white.csv', 5)
    print(f'Cross validation mean accuracy: {cv:.3f}')
