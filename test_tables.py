import pandas as pd
from db_connection import engine

query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
"""

df = pd.read_sql(query, engine)
print(df)