import psycopg2
from datetime import datetime
from dateutil.relativedelta import relativedelta

def create_future_partitions(conn, months_ahead=12):
    """
    Automates the creation of monthly partitions for the next year.
    Ensures the 'Digital Backbone' is always ready for new data.
    """
    cursor = conn.cursor()
    # Start from the current month
    start_date = datetime.now().replace(day=1)

    for i in range(months_ahead):
        current_month = start_date + relativedelta(months=i)
        next_month = current_month + relativedelta(months=1)
        
        partition_name = f"transactions_{current_month.strftime('%Y_%m')}"
        
        sql = f"""
        CREATE TABLE IF NOT EXISTS {partition_name} 
        PARTITION OF transactions
        FOR VALUES FROM ('{current_month.strftime('%Y-%m-%d')}') 
        TO ('{next_month.strftime('%Y-%m-%d')}');
        """
        cursor.execute(sql)
    
    conn.commit()
    print(f"✅ Successfully ensured {months_ahead} future partitions.")
