import re 

command_synonyms = {
    "select": ["select", "show", "display", "print", "choose"],
    "insert": ["insert", "add", "include", "store"],
    "update": ["update", "modify", "change", "edit"],
    "delete": ["delete", "remove", "erase", "discard"]
}


def normalize_command(nl_query):
    nl_query = nl_query.lower().strip()

    for sql_command, synonyms in command_synonyms.items():
        for synonym in synonyms:
            if nl_query.startswith(synonym):
                nl_query =  nl_query.replace(synonym, sql_command, 1)
                break
            
    nl_query = re.sub(r"\b(all)\b", "*", nl_query)

    return nl_query


def clean_values(values):
    values = values.split(",")
    values = [f"'{val.strip()}'" if not val.strip().isdigit() else val.strip() for val in values]
    return ", ".join(values)

# Function to convert natural language to SQL
def nl_to_sql(nl_query):
# INSERT Queries (allow missing parentheses)
    insert_pattern = re.match(r"insert into (\w+) (.+) values (.+)", nl_query)
    if insert_pattern:
        table, columns, values = insert_pattern.groups()
        columns = columns.replace("(", "").replace(")", "").strip()  # Remove parentheses
        values = values.replace("(", "").replace(")", "").strip()
        values = clean_values(values)  # Handle missing quotes
        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values});"
        execute = True
        return sql_query

    # UPDATE Queries (allow missing quotes for values)
    update_pattern = re.match(r"update (\w+) set (.+) where (.+)", nl_query)
    if update_pattern:
        table, updates, condition = update_pattern.groups()
        updates = ", ".join([f"{col.strip()} = {clean_values(val.strip())}" for col, val in 
                            (pair.split("=") for pair in updates.split(","))])
        sql_query = f"UPDATE {table} SET {updates} WHERE {condition};"

        execute = True
        return sql_query

    # DELETE Queries
    delete_pattern = re.match(r"delete from (\w+)(?: where (.+))?", nl_query)
    if delete_pattern:
        table, condition = delete_pattern.groups()
        sql_query = f"DELETE FROM {table}"
        if condition:
            sql_query += f" WHERE {condition}"
        execute = False
        return sql_query + ";"
    

# Testing different formats
# queries = [
#     "show name, age from users where age > 20",  
#     "add into users name, age values Alice, 25", 
#     "modify users set age = 30 where name = Bob",
#     "remove from users where name = Charlie",  
#     "show all from users"
# ]

# for q in queries:
#     print(nl_to_sql(q))