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


## Executive Summary
