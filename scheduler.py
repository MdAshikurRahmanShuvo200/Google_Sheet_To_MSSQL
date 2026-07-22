import time
from services.sync_service import SyncService


class Scheduler:

    def __init__(self, interval=60):

        self.interval = interval

    def start(self):

        while True:

            try:

                print("=" * 60)
                print("Starting Google Sheet Sync...")

                sync = SyncService()

                sync.run()

                print("Sync Completed Successfully.")

            except Exception as e:

                print(f"Error: {e}")

            print(f"Waiting {self.interval} seconds...")
            print("=" * 60)

            time.sleep(self.interval)