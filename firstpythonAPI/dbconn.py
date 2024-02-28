from sqlalchemy import create_engine
import json
rows=[]

engine = create_engine('postgresql://postgres:Password123.@localhost:5432/postgres')

from sqlalchemy.sql import text

stored_procedure = text("SELECT * FROM sp_get_school_list()")

with engine.connect() as connection:
    result = connection.execute(stored_procedure)

    for row in result:
        rows.append(dict(zip(result.keys(), row)))

    json_rows = json.dumps(rows)

print(json_rows)