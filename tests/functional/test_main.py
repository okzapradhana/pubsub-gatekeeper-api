def test_invalid_operation_name(client):
    payload = {
        "activities": [
            {
                "operation": "other operation",
                "table": "table1",
                "value_to_delete": {
                    "col_names": ["a", "c", "e"],
                    "col_types": ["INTEGER", "TEXT", "TEXT"],
                    "col_values": [3, "2019-04-28 10:24:30.183414", "something"]
                }
            }
        ]
    }
    response = client.post("/api/activities", json=payload)
    result = response.get_json()

    assert result['error'] is not None
    assert result['status'] == 400
    assert result['message'] == "Invalid Schema"
    assert result['payload'] == payload


def test_missmatch_data_type_payload(client):
    payload = {
        "activities": [
            {
                "operation": "delete",
                "table": "table1",
                "value_to_delete": {
                    "col_names": [1, 2, "e"],
                    "col_types": ["INTEGER", "TEXT", "TEXT"],
                    "col_values": [3, "2019-04-28 10:24:30.183414", "something"]
                }
            }
        ]
    }
    response = client.post("/api/activities", json=payload)
    result = response.get_json()

    assert result['error'] is not None
    assert result['status'] == 400
    assert result['message'] == "Invalid Schema"
    assert result['payload'] == payload


def test_missing_required_field(client):
    payload = {
        "activities": [
            {
                "operation": "delete",
                "value_to_delete": {
                    "col_names": [1, 2, "e"],
                    "col_types": ["INTEGER", "TEXT", "TEXT"],
                    "col_values": [3, "2019-04-28 10:24:30.183414", "something"]
                }
            }
        ]
    }
    response = client.post("/api/activities", json=payload)
    result = response.get_json()

    assert result['error'] is not None
    assert result['status'] == 400
    assert result['message'] == "Invalid Schema"
    assert result['payload'] == payload


def test_only_delete_operation_payload(client):
    payload = {
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

    response = client.post("/api/activities", json=payload)
    result = response.get_json()

    assert result['error'] is None
    assert result['status'] == 200
    assert result['message'] == "Valid Schema"
    assert result['payload'] == payload


def test_only_insert_operation_payload(client):
    payload = {
        "activities": [
            {
                "operation": "insert",
                "table": "table1",
                "col_names": ["a", "c", "e"],
                "col_types": ["INTEGER", "TEXT", "TEXT"],
                "col_values": [3, "2019-04-28 10:24:30.183414", "something"]
            }
        ]
    }

    response = client.post("/api/activities", json=payload)
    result = response.get_json()

    assert result['error'] is None
    assert result['status'] == 200
    assert result['message'] == "Valid Schema"
    assert result['payload'] == payload


def test_valid_payload(client):
    payload = {
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

    response = client.post("/api/activities", json=payload)
    result = response.get_json()

    assert result['error'] is None
    assert result['status'] == 200
    assert result['message'] == "Valid Schema"
    assert result['payload'] == payload
