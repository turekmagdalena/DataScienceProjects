# Apartment Prices in Poland

Apartment prices in Poland have been rising steadily, making it difficult for many people to decide where and what kind of apartment they can afford. This project aims to provide a simple tool that predicts apartment prices based on location and key property parameters. By selecting a city and specifying apartment details, users can receive an estimated price per square meter, helping them explore affordability and make informed decisions about potential purchases.

### Objective
* Develop a predictive model that estimates apartment prices based on location and apartment features.
* Provide an easy-to-use interface for users to input key details.
* Help users determine where they may want to move or what type of apartment fits their budget.


## Table of Contents

1. [Project Architecture](#project-architecture)
2. [File Descriptions](#file-descriptions)
3. [Executive Summary](#executive-summary)


## Project Architecture

```bash
├── config
├── data
│   ├── processed
│   └── raw
├── docs
├── models
├── notebooks
│   ├── all_cities
│   └── krakow
```

## File Descriptions
[config](config): folder containing configuration files
* [bins.json](config/bins.json): bins used for splitting data in 'distance' columns. File is used for feature engineering new data from user.

[data](data): folder containing all data files 
* [processed](data/processed): datasets that undergone preliminary cleansing, transformations and other preparatory steps
  * [processed_data_all.csv](data/processed/processed_data_all.csv): processed data for all cities from original dataset
  * [processed_data_Krakow.csv](data/processed/processed_data_Krakow.csv): data filtered by city of Krakow and processed
* [raw](data/raw): original datasets
  * [apartments_pl_2024_06.csv](data/raw/apartments_pl_2024_06.csv): original dataset with apartment prices from June 2024

[models](models): folder containing trained algorithms
* [encoders.pkl](models/encoders.pkl): trained OneHotEncoder for all categorical columns
* [xgboost_all_cities.pkl](models/xgboost_all_cities.pkl): XGBoost model trained on data for all cities
* [xgboost_krakow.pkl](models/xgboost_krakow.pkl): XGBoost model trained on data for city of Krakow

[notebooks](notebooks): folder containing notebooks with all project steps
* [all_cities](notebooks/all_cities): notebooks for processing dataset with all cities included
  * [create_model_for_all_cities.ipynb](notebooks/all_cities/create_model_for_all_cities.ipynb): notebook with use of pre-defined functions for data preparation and model training for dataset with all cities included
  * [data_preparation_functions.py](notebooks/all_cities/data_preparation_functions.py): functions for feature selection and engineering
  * [prediction_app.ipynb](notebooks/all_cities/prediction_app.ipynb): notebook with the application that makes a prediction based on user's input
* [krakow](notebooks/krakow): notebooks for processing dataset filtered by city of Krakow
  * [1_data_and_feature_preparation.ipynb](notebooks/krakow/1_data_and_feature_preparation.ipynb): notebook with data exploration and preparation based on dataset filtered by city of Krakow
  * [2_model_training_and_evaluation.ipynb](notebooks/krakow/2_model_training_and_evaluation.ipynb): notebook with steps for training and selecting the best model
 

  
## Executive Summary
