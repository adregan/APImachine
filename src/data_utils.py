def convert_database_cursor(cursor):
    converted = [
        dict(list(
            zip([col[0] for col in cursor.description], row)
        )) for row in cursor.fetchall()
    ]

    return converted

def convert_to_json(schema, cursor_objects):
    data = [
        schema().dump(object).data 
        for object in cursor_objects
    ]

    return data
