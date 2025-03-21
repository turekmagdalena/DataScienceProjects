# -*- coding: utf-8 -*-

import pandas as pd
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import OneHotEncoder
import numpy as np


# HELPER FUNCTIONS


def categorize_location(df):
    """Use latitude and longitude columns to create locationCategory"""
    # Approximate conversion factors
    LATITUDE_TO_METERS = 111_111  # 1 degree latitude in meters
    LONGITUDE_TO_METERS = 111_111 * np.cos(np.radians(50))  # Adjust for latitude
    GRID_SIZE_METERS = 1_000  # 1 km grid size

    # Convert latitude and longitude to grid indices
    df["lat_index"] = (df["latitude"] * LATITUDE_TO_METERS // GRID_SIZE_METERS).astype(
        int
    )
    df["lon_index"] = (
        df["longitude"] * LONGITUDE_TO_METERS // GRID_SIZE_METERS
    ).astype(int)

    # Combine grid indices into a category
    df["locationCategory"] = (
        df["lat_index"].astype(str) + "_" + df["lon_index"].astype(str)
    )

    # Encode location categories to numbers
    df["locationCategory"] = (
        pd.factorize(df["locationCategory"])[0] + 1
    )  # Start encoding from 1

    df = df.drop(columns=["latitude", "longitude", "lat_index", "lon_index"])

    return df


def fill_na_in_type(df):
    """Fill missing values in 'type' column using buildYear and locationCategory"""
    # Calculate global most popular type
    pop_type = df["type"].value_counts().idxmax()

    # Calculate most popular type within buildYear and locationCategory
    year_loc_type = (
        df.groupby(["buildYear", "locationCategory"])["type"]
        .apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        .reset_index(name="dominant_type")
    )

    # Calculate most popular type within locationCategory
    loc_type = (
        df.groupby("locationCategory")["type"]
        .apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        .to_dict()
    )

    # Merge with the original DataFrame using year_loc_type
    df_merged = df.merge(
        year_loc_type, on=["buildYear", "locationCategory"], how="left"
    )

    # Fill missing 'dominant_type' with locationCategory mapping
    df_merged["dominant_type"] = df_merged["dominant_type"].fillna(
        df_merged["locationCategory"].map(loc_type)
    )

    # Fill final missing values with the global most popular type
    df_merged["dominant_type"] = df_merged["dominant_type"].fillna(pop_type)

    # # Fill missing values in original DataFrame using new column
    df = df.reset_index(drop=True)
    df_merged = df_merged.reset_index(drop=True)
    df["type"] = df["type"].fillna(df_merged["dominant_type"])

    return df


def split_into_bins(df, columns):
    """Split numerical columns into 10 bins, using max value among all columns.

    Parameters:
    df: DataFrame with columns to split
    columns: List of column names to split

    Returns:
    df: DataFrame with split columns
    bins: List of bin edges

    """

    max_column = df[columns].max().idxmax()
    max_val = df[max_column].max()

    bins = np.linspace(0, max_val, 11)

    for col in columns:
        df[f"{col}_binned"] = pd.cut(
            df[col], bins=bins, labels=False, include_lowest=True
        )

    df = df.drop(columns=columns)

    return df, bins.tolist()


def encode_city_column(df, city_column):
    """Perform OneHotEnconding on city column. Keep all city options as features.

    Parameters:
    df: DataFrame with city column to encode
    city_column: Name of the city column

    Returns:
    df: DataFrame with encoded city column
    ohe_city: OneHotEncoder object for city column
    """

    # Initialize OneHotEncoder for city
    ohe_city = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded_city_array = ohe_city.fit_transform(df[[city_column]])

    # Get column names for the encoded features of 'city'
    encoded_city_feature_names = ohe_city.get_feature_names_out([city_column])

    # Create a DataFrame with the encoded columns for 'city'
    encoded_city_df = pd.DataFrame(
        encoded_city_array, columns=encoded_city_feature_names, index=df.index
    )

    # Concatenate the encoded columns with the original DataFrame (drop the original 'city' column)
    df = pd.concat([df.drop(columns=[city_column]), encoded_city_df], axis=1)

    return df, ohe_city


def encode_cat_columns(df, cat_columns):
    """Perform OneHotEnconding on categorical columns. Drop first column.

    Parameters:
    df: DataFrame with columns to encode
    cat_columns: List of column names to encode

    Returns:
    df: DataFrame with encoded categorical columns
    ohe_cat: OneHotEncoder object for categorical columns
    """

    # Initialize OneHotEncoder for categorical columns
    ohe_cat = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
    encoded_other_array = ohe_cat.fit_transform(df[cat_columns])

    # Get column names for the encoded features of categorical columns
    encoded_other_feature_names = ohe_cat.get_feature_names_out(cat_columns)

    # Create a DataFrame with the encoded columns for categorical columns
    encoded_other_df = pd.DataFrame(
        encoded_other_array, columns=encoded_other_feature_names, index=df.index
    )

    # Concatenate the encoded columns with the original DataFrame (drop the original categorical columns)
    df = pd.concat([df.drop(columns=cat_columns), encoded_other_df], axis=1)

    return df, ohe_cat


# FUNCTIONS PER CITY - functions that should be performed separately for each city


def fill_na_per_city(df):
    """Fill missing values based on statistical measures. The input DataFrame should be pre-filtered for a single city."""
    df = fill_na_in_type(df)

    df["buildYear"] = df.groupby("type")["buildYear"].transform(
        lambda x: x.fillna(round(x.median()))
    )

    df["condition"] = df["condition"].fillna("standard")

    df["floorCount"] = df["floorCount"].fillna(round(df["floorCount"].median()))

    df["floor"] = df.groupby("floorCount")["floor"].transform(
        lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else 1)
    )

    feature_columns = [col for col in df.columns if "has" in col]

    for col in feature_columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    distance_columns = [col for col in df.columns if "Distance" in col]

    for col in distance_columns:
        df[col] = df[col].fillna(df[col].mean())

    return df


def handle_outliers_per_city(df):
    """Handle outliers in the dataset using winsorization and log transformation.The input DataFrame should be pre-filtered for a single city."""
    lower_limit = df["buildYear"].le(1919).mean()
    df["buildYear"] = winsorize(df["buildYear"], limits=(lower_limit, 0))

    df["squareMeters"] = winsorize(df["squareMeters"], limits=(0, 0.05))

    df["poiCount"] = winsorize(df["poiCount"], limits=(0, 0.1))

    df["price_per_m2"] = winsorize(df["price_per_m2"], limits=(0, 0.05))
    df["price_per_m2_log"] = np.log(df["price_per_m2"])

    return df


# FUNCTIONS FOR WHOLE DATASET


def split_and_save_bins(df):
    """Split Distance columns into 10 bins, using max value among all columns.

    Parameters:
    df: DataFrame with columns to split

    Returns:
    df: DataFrame with split columns
    bins_to_save: Dictionary with bin edges
    """

    distance_columns = [col for col in df.columns if "Distance" in col]

    distance_columns.remove(
        "centreDistance"
    )  # centreDistance column has wider range and should be split separately

    df, distance_bins = split_into_bins(df, distance_columns)

    df["centreDistance"] = winsorize(
        df["centreDistance"], limits=(0, 0.05)
    )  # handle outliers

    df, centre_distance_bins = split_into_bins(df, ["centreDistance"])

    bins_to_save = {
        "distance_bins": distance_bins,
        "centre_distance_bins": centre_distance_bins,
    }

    return df, bins_to_save


def encode_and_save_encoder(df):
    """Perform OneHotEnconding on categorical columns. Treat separately city column.

    Parameters:
    df: DataFrame with columns to encode

    Returns:
    df: DataFrame with encoded categorical columns
    ohe_dict: Dictionary with OneHotEncoder objects for categorical columns
    """

    df, ohe_city = encode_city_column(df, "city")

    cat_columns = df.select_dtypes("object").columns

    df, ohe_cat = encode_cat_columns(df, cat_columns)

    ohe_dict = {"city_encoder": ohe_city, "cat_column_encoder": ohe_cat}

    return df, ohe_dict
