import time
import random
from locust import HttpUser, task, between


class GatekeeperApiUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def process_activities(self):
        insert_payload = {
            "activities": [
                {
                    "operation": "insert",
                    "table": "table1",
                    "col_names": ["a", "b", "c"],
                    "col_types": ["INTEGER", "TEXT", "TEXT"],
                    "col_values": [1, "Backup and Restore", "2018-03-27 11:58:28.988414"]
                }
            ]
        }

        delete_payload = {
            "activities": [
                {
                    "operation": "delete",
                    "table": "table1",
                    "value_to_delete": {
                        "col_names": ["a", "c", "e"],
                        "col_types": ["INTEGER", "TEXT", "TEXT"],
                        "col_values": [3, "2019-04-28 10:24:30.183414", "something"]
                    }
                }
            ]
        }

        full_payload = {
            "activities": [
                {
                    "operation": "delete",
                    "table": "table1",
                    "value_to_delete": {
                        "col_names": ["a", "c", "e"],
                        "col_types": ["INTEGER", "TEXT", "TEXT"],
                        "col_values": [3, "2019-04-28 10:24:30.183414", "something"]
                    }
                },
                {
                    "operation": "insert",
                    "table": "table1",
                    "col_names": ["a", "b", "c"],
                    "col_types": ["INTEGER", "TEXT", "TEXT"],
                    "col_values": [1, "Backup and Restore", "2018-03-27 11:58:28.988414"]
                }
            ]
        }

        data = [insert_payload, delete_payload, full_payload]
        self.client.post("/api/activities", json=random.choice(data))
