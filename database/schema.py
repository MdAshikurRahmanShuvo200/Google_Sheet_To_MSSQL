class SchemaManager:

    def __init__(self, repo):

        self.repo = repo

    # =====================================================
    # Dynamic Table Create (Google Sheet)
    # =====================================================

    def create_table(self, table_name, headers):

        columns = []

        columns.append(
            "[id] INT IDENTITY(1,1) PRIMARY KEY"
        )

        for header in headers:

            header = header.strip()

            if header == "":
                continue

            columns.append(
                f"[{header}] NVARCHAR(MAX)"
            )

        columns.append(
            "[created_at] DATETIME DEFAULT GETDATE()"
        )

        columns.append(
            "[updated_at] DATETIME NULL"
        )

        column_sql = ",\n".join(columns)

        query = f"""

        IF OBJECT_ID('{table_name}','U') IS NULL

        BEGIN

            CREATE TABLE [{table_name}]
            (

                {column_sql}

            )

        END

        """

        self.repo.execute(query)

        self.repo.commit()

    # =====================================================
    # Call History Table
    # =====================================================

    def create_call_history_table(self):

        query = """

        IF OBJECT_ID('call_history','U') IS NULL

        BEGIN

            CREATE TABLE call_history
            (

                id INT IDENTITY(1,1) PRIMARY KEY,

                call_id NVARCHAR(200) UNIQUE,

                agent_id NVARCHAR(100),

                call_date DATE,

                call_start DATETIME2(7),

                call_end DATETIME2(7),

                call_duration_seconds INT,

                call_duration VARCHAR(20),

                created_at DATETIME DEFAULT GETDATE(),

                updated_at DATETIME NULL

            )

        END

        """

        self.repo.execute(query)

        self.repo.commit()

    # =====================================================
    # Complaint Master Table
    # =====================================================

    def create_complain_master_table(self):

        query = """

        IF OBJECT_ID('complain_call_master','U') IS NULL

        BEGIN

            CREATE TABLE complain_call_master
            (

                id INT IDENTITY(1,1) PRIMARY KEY,

                call_id NVARCHAR(200) UNIQUE,

                created_at DATETIME DEFAULT GETDATE(),

                updated_at DATETIME NULL

            )

        END

        """

        self.repo.execute(query)

        self.repo.commit()

    # =====================================================
    # Create All System Tables
    # =====================================================

    def create_system_tables(self):

        self.create_call_history_table()

        self.create_complain_master_table()