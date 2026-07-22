from collections import defaultdict
from datetime import datetime


class MasterService:

    def __init__(self, repo):

        self.repo = repo

    # ==========================================
    # Read Webhook Events
    # ==========================================

    def get_webhook_events(self):

        query = """
        SELECT
            [Call ID],
            event_name,
            webhook_delivered_at,
            agent_id
        FROM webhook_events
        ORDER BY webhook_delivered_at
        """

        self.repo.execute(query)

        columns = [
            column[0]
            for column in self.repo.cursor.description
        ]

        rows = self.repo.fetchall()

        events = []

        for row in rows:

            item = {}

            for i, value in enumerate(row):

                item[columns[i]] = value

            events.append(item)

        return events

    # ==========================================
    # String To Datetime
    # ==========================================

    def to_datetime(self, value):

        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        text = str(value).replace("Z", "").replace("T", " ")

        formats = [
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S"
        ]

        for fmt in formats:

            try:

                return datetime.strptime(text, fmt)

            except:

                pass

        return None

    # ==========================================
    # Group By Call ID
    # ==========================================

    def build_call_history(self):

        events = self.get_webhook_events()

        grouped = defaultdict(list)

        for event in events:

            call_id = event["Call ID"]

            grouped[call_id].append(event)

        history = []

        for call_id, event_list in grouped.items():

            call_start = None
            call_end = None
            agent_id = None

            for item in event_list:

                event_name = str(
                    item["event_name"]
                ).lower()

                event_time = self.to_datetime(
                    item["webhook_delivered_at"]
                )

                if agent_id is None:

                    agent_id = item["agent_id"]

                if "started" in event_name:

                    if call_start is None:

                        call_start = event_time

                elif "ended" in event_name:

                    call_end = event_time

            duration = None

            if call_start and call_end:

                duration = int(
                    (call_end - call_start).total_seconds()
                )

            history.append({

                "call_id": call_id,

                "agent_id": agent_id,

                "call_date":
                    call_start.date()
                    if call_start else None,

                "call_start":
                    call_start,

                "call_end":
                    call_end,

                "duration":
                    duration

            })

        return history

    # ==========================================
    # Preview
    # ==========================================

    def preview(self):

        rows = self.build_call_history()

        print()

        print("=" * 60)

        print("CALL HISTORY PREVIEW")

        print("=" * 60)

        for row in rows[:5]:

            print()

            print("Call ID :", row["call_id"])

            print("Agent :", row["agent_id"])

            print("Date :", row["call_date"])

            print("Start :", row["call_start"])

            print("End :", row["call_end"])

            print("Duration :", row["duration"])