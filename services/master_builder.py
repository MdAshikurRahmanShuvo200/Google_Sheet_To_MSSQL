from database.master_schema import MasterSchema


class MasterBuilder:

    def __init__(self):

        self.schema = MasterSchema()

    def build(self):

        print("=" * 60)

        print("Building Master Table...")

        self.schema.create_table()

        print("Master Table Ready")

        print("=" * 60)