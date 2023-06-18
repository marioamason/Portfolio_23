import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def file_reader(file_path):
    # Check the file extension
    file_extension = file_path.split(".")[-1]

    if file_extension == 'csv':
        # Read a CSV file
        return pd.read_csv(file_path)
    elif file_extension in ['xls', 'xlsx']:
        # Read an Excel file
        return pd.read_excel(file_path,delimiter=';')
    else:
        raise ValueError("Unsupported file type. Only 'csv', 'xls', and 'xlsx' are supported.")




def standard_eda(data):
    # Check for missing values and visualize if there are any
    missing_values = data.isnull().sum()
    if missing_values.sum() > 0:
        print("Missing Values:")
        print(missing_values)

        # Visualize missing values using a heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(data.isnull(), cmap="viridis", cbar=False)
        plt.title("Missing Values")
        plt.show()

    # Count the number of numerical and categorical features
    numerical_cols = data.select_dtypes(include=['int', 'float']).columns
    categorical_cols = data.select_dtypes(include=['object']).columns

    print(f"Number of Numerical Features: {len(numerical_cols)}")
    print(f"Number of Categorical Features: {len(categorical_cols)}")

    # Distribution plots for numerical features
    for col in numerical_cols:
        if col not in data.columns:
            continue
        plt.figure(figsize=(8, 6))
        sns.histplot(data[col].dropna(), kde=True, color='blue')
        plt.title(f"Distribution of {col}")
        plt.show()

    # Bar plots for categorical features
    for col in categorical_cols:
        if col not in data.columns:
            continue
        plt.figure(figsize=(8, 6))
        sns.countplot(data=data, x=col, palette='Set3')
        plt.title(f"Count of {col}")
        plt.show()