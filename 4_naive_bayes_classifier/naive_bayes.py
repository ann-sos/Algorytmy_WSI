import numpy as np
import pandas as pd


def split_dataset(dataset: pd.DataFrame):
    # split dataset into training and testing sets
    training_df = dataset.sample(frac=0.6)
    testing_df = dataset.drop(training_df.index)
    return training_df, testing_df


class NaiveBayes:
    def __init__(self, training_set):
        self.wine_df = training_set
        self.features_list = wine_df.columns[:-1].values.tolist()
        # list quality values that are present in the training set
        self.quality_values = sorted(self.wine_df["quality"].unique().tolist())
        # calculate number of instances of any class: how many wines of a quality X are in the dataset
        self.class_instances = {}
        self.class_probabilities = {}
        for qv in self.quality_values:
            self.class_instances[qv] = self.wine_df[self.wine_df["quality"] == qv].shape[0]
            self.class_probabilities[qv] = self.class_instances[qv] / self.wine_df.shape[0]

    def likelihood(self, feature_name, feature_value, target_class):
        feature = self.wine_df.loc[wine_df["quality"] == target_class, feature_name]
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


if __name__ == "__main__":
    # import dataset
    wine_df = pd.read_csv(r'winequality-white.csv', delimiter=";")
    # split dataset
    wine_training_df, wine_testing_df = split_dataset(wine_df)
    # initialise the classifier instance with the training set
    myBayes = NaiveBayes(wine_training_df)
    nb = myBayes.naive_bayes(wine_testing_df)
    jb = pd.DataFrame({'calculated': nb, 'real': wine_testing_df['quality'],
                       'isRight': nb == wine_testing_df['quality']})
    print(jb)
    print(jb.isRight.value_counts())
