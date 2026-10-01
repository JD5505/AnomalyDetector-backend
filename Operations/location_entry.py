def enter_location(email: str, samples_tuples: list, cursor):
    rows = [
        (email, row[0], row[1], row[2])
        for row in samples_tuples
    ]

    cursor.executemany(
        """
        INSERT INTO location_data
        (email, latitude, longitude, timestamp)
        VALUES
        (%s, %s, %s, %s)
        ON CONFLICT (email, timestamp) DO NOTHING
        """,
        rows
    )
    return True