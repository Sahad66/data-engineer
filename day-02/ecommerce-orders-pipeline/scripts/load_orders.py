import csv
import psycopg

# Database connection details
DB_HOST = "localhost"
DB_NAME = "day-2"
DB_USER = "postgres"
DB_PASSWORD = "YOUR_POSTGRES_PASSWORD"  # আপনার পোস্টগ্রেস পাসওয়ার্ড এখানে দিন

def load_data():
    csv_file_path = r"day-02\ecommerce-orders-pipeline\data\orders.csv"
    
    print("Connecting to PostgreSQL database ('day-2')...")
    
    try:
        with psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cur:
                print("Connected successfully. Reading CSV file...")
                
                with open(csv_file_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    
                    row_count = 0
                    for row in reader:
                        # Data validation / handling missing customer_id
                        customer_id = row["customer_id"] if row["customer_id"].strip() != "" else None
                        
                        cur.execute(
                            """
                            INSERT INTO ecommerce_orders (order_id, customer_id, order_date, product, quantity, unit_price, status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                int(row["order_id"]),
                                customer_id,
                                row["order_date"],
                                row["product"],
                                int(row["quantity"]),
                                float(row["unit_price"]),
                                row["status"]
                            )
                        )
                        row_count += 1
                        
                conn.commit()
                print(f"Load completed successfully! Total rows inserted: {row_count}")
                
    except Exception as e:
        print(f"Error occurred during data loading: {e}")

if __name__ == "__main__":
    load_data()