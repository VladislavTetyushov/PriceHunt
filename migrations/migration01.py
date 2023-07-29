import SQLdata

create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        message TEXT
);
"""

# connection = SQLdata.create_connection("../" + SQLdata.data_filename)

SQLdata.execute_query(create_users_table)
