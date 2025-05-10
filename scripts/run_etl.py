from etl.extract.extract import extract_data
from etl.transform.transform import transform_sales, load_population_monthly
from etl.load.load import write_sales, write_population


def main():
    # 1) Extract
    raw_sales = extract_data()

    # 2) Transform
    sales_df = transform_sales(raw_sales)
    pop_df = load_population_monthly()

    # 3) Load
    write_sales(sales_df)
    write_population(pop_df)


if __name__ == "__main__":
    main()
