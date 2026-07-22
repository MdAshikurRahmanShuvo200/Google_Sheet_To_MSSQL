from google_sheet.reader import GoogleSheetReader
from config import SHEET_ID, GOOGLE_CREDENTIAL

from database.repository import Repository
from database.schema import SchemaManager
from database.inserter import DataInserter

from utils.helper import make_table_name


class SyncService:

    def __init__(self):

        self.reader = GoogleSheetReader(
            SHEET_ID,
            GOOGLE_CREDENTIAL
        )

        # One Repository
        self.repo = Repository()

        # Same Repository Share
        self.schema = SchemaManager(
            self.repo
        )

        self.inserter = DataInserter(
            self.repo
        )

    def run(self):

        self.repo.execute(
            "SELECT @@VERSION"
        )

        print(self.repo.fetchone()[0])

        print("=" * 60)

        worksheets = self.reader.get_all_worksheets()

        for worksheet in worksheets:

            table_name = make_table_name(
                worksheet.title
            )

            print(f"\nWorksheet : {worksheet.title}")

            data = self.reader.get_sheet_data(
                worksheet
            )

            if len(data) <= 1:

                print("No Data")

                continue

            headers = data[0]

            rows = data[1:]

            self.schema.create_table(
                table_name,
                headers
            )

            self.inserter.insert_rows(
                table_name,
                headers,
                rows
            )

        self.repo.close()