from database.updater import DataUpdater


class DataInserter:

    def __init__(self, repo):

        self.repo = repo
        self.updater = DataUpdater(repo)

    def insert_rows(self, table_name, headers, rows):

        if len(rows) == 0:
            return

        # ==================================================
        # Special Case : webhook_events
        # ==================================================

        if table_name == "webhook_events":

            columns = ",".join(f"[{h}]" for h in headers)

            placeholders = ",".join("?" for _ in headers)

            insert_query = f"""
            IF NOT EXISTS
            (
                SELECT 1
                FROM webhook_events
                WHERE [Call ID] = ?
                AND event_name = ?
                AND webhook_delivered_at = ?
            )

            INSERT INTO webhook_events
            ({columns})

            VALUES
            ({placeholders})
            """

            call_id_index = headers.index("Call ID")
            event_index = headers.index("event_name")
            webhook_index = headers.index("webhook_delivered_at")

            inserted = 0

            for row in rows:

                params = (

                    row[call_id_index],

                    row[event_index],

                    row[webhook_index],

                    *row

                )

                self.repo.execute(
                    insert_query,
                    params
                )

                inserted += 1

            self.repo.commit()

            print(f"Inserted : {inserted}")

            print("Updated  : 0")

            return

        # ==================================================
        # Normal Tables
        # ==================================================

        if "Call ID" not in headers:

            print(f"{table_name} -> No Call ID Column")

            return

        call_id_index = headers.index("Call ID")

        existing_call_ids = self.repo.get_existing_call_ids(
            table_name
        )

        columns = ",".join(
            f"[{h}]"
            for h in headers
        )

        placeholders = ",".join(
            "?"
            for _ in headers
        )

        insert_query = f"""
        INSERT INTO [{table_name}]
        ({columns})
        VALUES
        ({placeholders})
        """

        insert_rows = []

        inserted = 0

        updated = 0

        for row in rows:

            call_id = row[call_id_index]

            if call_id in existing_call_ids:

                self.updater.update_row(
                    table_name,
                    headers,
                    row
                )

                updated += 1

            else:

                insert_rows.append(row)

                inserted += 1

        if insert_rows:

            self.repo.executemany(
                insert_query,
                insert_rows
            )

        self.repo.commit()

        print(f"Inserted : {inserted}")

        print(f"Updated  : {updated}")