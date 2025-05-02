from kaggle.api.kaggle_api_extended import KaggleApi

# 1) Authenticate & download+unzip the files into ./data/
api = KaggleApi()
api.authenticate()
api.dataset_download_files(
    "suraj520/car-sales-data",
    path="data",       # <-- will create ./data/car_sales_data.csv
    unzip=True
)