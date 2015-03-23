def convert_database_cursor(cursor, single):
    keys = [col[0] for col in cursor.description]
    if single:
        results = cursor.fetchone()
        if not results:
            return
        converted = dict(zip(keys, results))

    else:
        results = cursor.fetchall()
        converted = [
            dict(list(
                zip(keys, values)
            )) for values in results
        ]

    return converted

def convert_to_json(schema, cursor_objects):
    if isinstance(cursor_objects, (list)):
        data = [
            schema().dump(object).data 
            for object in cursor_objects
        ]
    else:
        data = schema().dump(cursor_objects).data

    return data
