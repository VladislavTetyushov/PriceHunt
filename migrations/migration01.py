import SQLdata

create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
);
"""
create_messages_table = """
    CREATE TABLE IF NOT EXISTS messages (
        message TEXT PRIMARY KEY,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
);
"""

SQLdata.execute_query(create_users_table)
