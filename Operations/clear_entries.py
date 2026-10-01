def remove_entries_db(cursor):
    cursor.execute(
        """
        DELETE FROM location_data
        WHERE id IN (
        SELECT id
        FROM (
        SELECT
        id,
        ROW_NUMBER() OVER (
        PARTITION BY email
        ORDER BY timestamp DESC
        ) AS rn
        FROM location_data
        ) ranked
        WHERE rn > 100
        );
        """
    )

    cursor.connection.commit()