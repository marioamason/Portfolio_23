import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def standard_eda(data):
    # Display the first few rows of the dataset
    print("First 5 rows of the dataset:")
    print(data.head())

    # Summary statistics
    print("Summary statistics:")
    print(data.describe())

    # Check the data types of each column
    print("Data types:")
    print(data.dtypes)

    # Check for missing values
    print("Missing values:")
    missing_values = data.isnull().sum()
    print(missing_values)

    # Visualize missing values
    if missing_values.sum() > 0:
        plt.figure(figsize=(10, 6))
        sns.heatmap(data.isnull(), cmap='viridis', cbar=False)
        plt.title("Missing Values Heatmap")
        plt.show()

    # Count numerical and categorical features
    numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = data.select_dtypes(include='object').columns

    print(f"Number of Numerical Features: {len(numerical_cols)}")
    print(f"Number of Categorical Features: {len(categorical_cols)}")

    # Distribution plots for numerical features
    for col in numerical_cols:
        plt.figure()
        sns.histplot(data[col], kde=True, color='skyblue')
        plt.xlabel(col)
        plt.ylabel("Density")
        plt.title(f"Distribution of {col}")
        plt.show()

    # Bar plots for categorical features
    for col in categorical_cols:
        plt.figure()
        sns.countplot(data[col], palette='Set2')
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.title(f"Bar plot of {col}")
        plt.show()
