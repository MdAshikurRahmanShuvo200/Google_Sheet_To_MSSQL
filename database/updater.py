class DataUpdater:

    def __init__(self, repo):

        self.repo = repo

    def update_row(self, table_name, headers, row):

        if "Call ID" not in headers:
            return

        call_id_index = headers.index("Call ID")

        call_id = row[call_id_index]

        set_columns = []
        values = []

        for i, header in enumerate(headers):

            if header == "Call ID":
                continue

            set_columns.append(f"[{header}] = ?")

            values.append(row[i])

        set_columns.append("[updated_at] = GETDATE()")

        values.append(call_id)

        query = f"""
        UPDATE [{table_name}]
        SET
        {", ".join(set_columns)}
        WHERE [Call ID] = ?
        """

        self.repo.execute(query, values)