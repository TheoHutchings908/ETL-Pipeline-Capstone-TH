import os
import pandas as pd


def find_project_root(marker_file='README.md'):
    """
    Find the root directory of the project by looking for a marker file.

    Args:
        marker_file (str): The name of the marker file to look for.

    Returns:
        str: The absolute path to the root directory of the project.
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while current_dir != os.path.dirname(current_dir):
        if marker_file in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError(
        f"Marker file '{marker_file}' not found in any parent directories."
    )


ROOT_DIR = find_project_root()
INDEXES_PATH = os.path.join(ROOT_DIR, 'etl', 'sql', 'indexes')
QUERY_PATH = os.path.join(ROOT_DIR, 'etl', 'sql')


def save_dataframe_to_csv(
    df: pd.DataFrame, relative_output_dir: str, filename: str
) -> None:
    """
    Save a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_dir (str): The directory to save the file to.
        filename (str): The name of the file to save.
    """
    output_dir = os.path.join(ROOT_DIR, relative_output_dir)
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, filename), index=False)
    print(f"Data saved to {os.path.join(output_dir, filename)}")
