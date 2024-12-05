# evaluate_breast_cancer_classifier.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.metrics import PredictionErrorDisplay

@click.command()
@click.option('--scaled-test-data', type=str, help="Path to scaled test data")
# @click.option('--columns-to-drop', type=str, help="Optional: columns to drop")
@click.option('--pipeline-from-ridge', type=str, help="Path to directory where the ridge fit pipeline object lives")
@click.option('--pipeline-from-tree', type=str, help="Path to directory where the tree fit pipeline object lives")
@click.option('--results-to', type=str, help="Path to directory where the plot will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(scaled_test_data, columns_to_drop, pipeline_from_ridge,pipeline_from_tree,results_to, seed):
    '''Evaluates the rental bike regressor on the test data 
    and saves the evaluation results.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # read in data & cancer_fit (pipeline object)
    rental_bike_test = pd.read_csv(scaled_test_data)
    # if columns_to_drop:
    #     to_drop = pd.read_csv(columns_to_drop).feats_to_drop.tolist()
    #     rental_bike_test = rental_bike_test.drop(columns=to_drop)
    with open(pipeline_from_ridge, 'rb') as f:
        rental_bike_fit_ridge = pickle.load(f)
    with open(pipeline_from_tree, 'rb') as f:
        rental_bike_fit_tree = pickle.load(f)

    # Compute accuracy
    accuracy_ridge = rental_bike_fit_ridge.score(
        rental_bike_test.drop("Rented Bike Count", axis=1),
        rental_bike_test["Rented Bike Count"]
    )

    accuracy_tree = rental_bike_fit_tree.score(
    rental_bike_test.drop("Rented Bike Count", axis=1),
    rental_bike_test["Rented Bike Count"]
    )

    test_scores = pd.DataFrame({'accuracy_ridge': [accuracy_ridge], 'accuracy_tree': [accuracy_tree]})
    test_scores.to_csv(os.path.join(results_to, "test_scores.csv"), index=False)

    # Plotting scatter plot for predicted value vs actual value on test set
    PredictionErrorDisplay.from_estimator(
        rental_bike_fit_ridge,
        rental_bike_test.drop("Rented Bike Count", axis=1),
        rental_bike_test["Rented Bike Count"],
        kind='actual_vs_predicted',
        scatter_kwargs={'alpha': 0.12, 's': 10}
    )

    # Plotting scatter plot for predicted value vs actual value on test set
    PredictionErrorDisplay.from_estimator(
        rental_bike_fit_tree,
        rental_bike_test.drop("Rented Bike Count", axis=1),
        rental_bike_test["Rented Bike Count"],
        kind='actual_vs_predicted',
        scatter_kwargs={'alpha': 0.12, 's': 10}
    )


if __name__ == '__main__':
    main()