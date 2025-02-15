# -*- coding: utf-8 -*-
"""test_data_preparation_functions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FhG5waiGLzPhWLHZAgA0mqICM1Hbh3-F
"""

import pytest
import pandas as pd
import numpy as np
import data_preparation_functions as dpf
from sklearn.preprocessing import OneHotEncoder

@pytest.fixture
def sample_data_raw():
  path = "/content/drive/MyDrive/Data Analysis/Apartments-Prices-in-Poland/tests/sample.csv"
  return pd.read_csv(path)

@pytest.fixture
def sample_data_with_loc_cat(sample_data_raw):
  return dpf.categorize_location(sample_data_raw.copy())

@pytest.fixture
def sample_data_processed():
  path = "/content/drive/MyDrive/Data Analysis/Apartments-Prices-in-Poland/tests/sample_processed.csv"
  return pd.read_csv(path)


def test_categorize_location(sample_data_raw):
  result_df = dpf.categorize_location(sample_data_raw.copy())

  assert isinstance(result_df, pd.DataFrame)
  assert "locationCategory" in result_df.columns
  assert "latitude" not in result_df.columns
  assert "longitude" not in result_df.columns
  assert result_df["locationCategory"].dtype == np.int64
  assert result_df["locationCategory"].min() == 1


def test_fill_na_in_type(sample_data_with_loc_cat):
  result_df = dpf.fill_na_in_type(sample_data_with_loc_cat.copy())

  assert isinstance(result_df, pd.DataFrame)
  assert result_df["type"].isna().sum() == 0
  assert result_df["type"].dtype == object


def test_fill_na_per_city(sample_data_with_loc_cat):
  result_df = dpf.fill_na_per_city(sample_data_with_loc_cat.copy())

  assert isinstance(result_df, pd.DataFrame)
  assert result_df["buildYear"].isna().sum() == 0
  assert result_df["condition"].isna().sum() == 0
  assert result_df["floorCount"].isna().sum() == 0
  assert result_df["floor"].isna().sum() == 0

  feature_columns = [col for col in result_df.columns if 'has' in col]
  distance_columns = [col for col in result_df.columns if 'Distance' in col]

  for col in feature_columns + distance_columns:
    assert result_df[col].isna().sum() == 0


def test_handle_outliers_per_city(sample_data_processed):
  result_df = dpf.handle_outliers_per_city(sample_data_processed.copy())

  assert isinstance(result_df, pd.DataFrame)

  lower_limit_buildYear = sample_data_processed['buildYear'].le(1919).mean()
  expected_buildYear_min = sample_data_processed['buildYear'].quantile(lower_limit_buildYear)

  expected_squareMeters_max = sample_data_processed['squareMeters'].quantile(0.95)
  expected_poiCount_max = sample_data_processed['poiCount'].quantile(0.9)
  expected_price_per_m2_max = sample_data_processed['price_per_m2'].quantile(0.95)

  assert result_df['buildYear'].min() >= expected_buildYear_min
  assert result_df['squareMeters'].max() <= expected_squareMeters_max
  assert result_df['poiCount'].max() <= expected_poiCount_max
  assert result_df['price_per_m2'].max() <= expected_price_per_m2_max

  assert 'price_per_m2_log' in result_df.columns
  assert (result_df['price_per_m2_log'] > 0).all()


def test_split_into_bins(sample_data_processed):
  columns_to_bin = ['clinicDistance', 'kindergartenDistance', 'collegeDistance', 'pharmacyDistance']
  result_df, bins = dpf.split_into_bins(sample_data_processed.copy(), columns_to_bin)

  assert isinstance(result_df, pd.DataFrame)
  assert isinstance(bins, list)
  assert len(bins) == 11
  assert all(isinstance(b, (int, float)) for b in bins)

  max_val = sample_data_processed[columns_to_bin].max().max()
  assert bins[-1] == max_val

  for col in columns_to_bin:
    assert col not in result_df.columns
    assert f"{col}_binned" in result_df.columns
    assert result_df[f"{col}_binned"].between(0, 9).all()


def test_encode_city_column(sample_data_processed):
  result_df, ohe_city = dpf.encode_city_column(sample_data_processed.copy(), 'city')

  assert isinstance(ohe_city, OneHotEncoder)
  assert 'city' not in result_df.columns

  encoded_city_columns = [col for col in result_df.columns if col.startswith("city_")]
  assert len(encoded_city_columns) == sample_data_processed['city'].nunique()

  assert result_df[encoded_city_columns].isin([0, 1]).all().all()
  assert (result_df[encoded_city_columns].sum(axis=1) == 1).all()


def test_encode_cat_columns(sample_data_processed):
  cat_columns = sample_data_processed.select_dtypes('object').columns

  result_df, ohe_cat = dpf.encode_cat_columns(sample_data_processed.copy(), cat_columns)

  assert isinstance(ohe_cat, OneHotEncoder)
  assert not any(col in result_df.columns for col in cat_columns)

  encoded_cat_columns = [col for col in result_df.columns if any(col.startswith(c) for c in cat_columns)]
  expected_num_columns = sum(sample_data_processed[col].nunique() - 1 for col in cat_columns)
  assert len(encoded_cat_columns) == expected_num_columns

  assert result_df[encoded_cat_columns].isin([0, 1]).all().all()


def test_split_and_save_bins(sample_data_processed):
  result_df, bins_to_save = dpf.split_and_save_bins(sample_data_processed.copy())

  assert isinstance(result_df, pd.DataFrame)
  assert isinstance(bins_to_save, dict)

  distance_columns = [col for col in sample_data_processed.columns if 'Distance' in col]
  for col in distance_columns:
    assert col not in result_df.columns
    assert f"{col}_binned" in result_df.columns

  assert "distance_bins" in bins_to_save
  assert "centre_distance_bins" in bins_to_save
  assert isinstance(bins_to_save["distance_bins"], list)
  assert isinstance(bins_to_save["centre_distance_bins"], list)

  original_95th_percentile = np.percentile(sample_data_processed['centreDistance'], 95)
  last_edge = bins_to_save["centre_distance_bins"][-1]
  assert last_edge <= original_95th_percentile

def test_encode_and_save_encoder(sample_data_processed):
  result_df, ohe_dict = dpf.encode_and_save_encoder(sample_data_processed.copy())

  assert isinstance(result_df, pd.DataFrame)
  assert isinstance(ohe_dict, dict)

  assert "city_encoder" in ohe_dict
  assert "cat_column_encoder" in ohe_dict
  assert isinstance(ohe_dict["city_encoder"], OneHotEncoder)
  assert isinstance(ohe_dict["cat_column_encoder"], OneHotEncoder)

  assert result_df.select_dtypes(include="object").empty