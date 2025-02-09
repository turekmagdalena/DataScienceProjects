# Apartment Prices in Poland

Project focused on predicting price of an apartament in Poland.

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
