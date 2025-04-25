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
    # for replacing * with all

    return nl_query


def clean_values(values):
    values = values.split(",")
    values = [f"'{val.strip()}'" if not val.strip().isdigit() else val.strip() for val in values]
    return ", ".join(values)


def nl_to_sql(nl_query):
    nl_query = normalize_command(nl_query.lower().strip())

    # SELECT Queries
    select_pattern = re.match(r"select (.+) from (\w+)(?: where (.+))?", nl_query)
    print(f"select_pattern: {select_pattern} ")
    if select_pattern:
        columns, table, condition = select_pattern.groups()
        print(" " + " " + table + " " + columns)
        if condition:
            print(condition)
        sql_query = f"SELECT {columns} FROM {table}"
        if condition:
            sql_query += f" WHERE {condition}"
            execute = True
        return sql_query + ";"

    return "Invalid Query"

