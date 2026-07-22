from database.repository import Repository


class MasterSchema:

    def __init__(self):

        self.repo = Repository()

    def create_table(self):

        query = """
        IF OBJECT_ID('complain_call_master','U') IS NULL
        BEGIN

            CREATE TABLE complain_call_master
            (

                id INT IDENTITY(1,1) PRIMARY KEY,

                [Call ID] NVARCHAR(100) UNIQUE,

                [Agent Name] NVARCHAR(MAX),
                [Agent ID] NVARCHAR(MAX),

                [From] NVARCHAR(MAX),
                [To] NVARCHAR(MAX),
                [Caller Number] NVARCHAR(MAX),

                [Call Type] NVARCHAR(MAX),
                [Call Summary] NVARCHAR(MAX),
                [PCA Status] NVARCHAR(MAX),

                [Factory Unit] NVARCHAR(MAX),

                [Grievience Categorization] NVARCHAR(MAX),

                [Call Ended Properly] NVARCHAR(MAX),

                [Employee Name] NVARCHAR(MAX),
                [Employee ID] NVARCHAR(MAX),

                [Message] NVARCHAR(MAX),
                [Type] NVARCHAR(MAX),
                [Timestamp] NVARCHAR(MAX),

                [Call Date] DATE,

                [Call Start] DATETIME,

                [Call End] DATETIME,

                [Call Duration] INT,

                created_at DATETIME DEFAULT GETDATE(),

                updated_at DATETIME
            )

        END
        """

        self.repo.execute(query)

        self.repo.commit()