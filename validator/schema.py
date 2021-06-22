def get_schema():
    return {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "type": "object",
        "properties": {
            "activities": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {
                            "$ref": "#/definitions/delete"
                        },
                        {
                            "$ref": "#/definitions/insert"
                        }
                    ]
                },
            },
        },
        "definitions": {
            "insert": {
                "type": "object",
                "properties": {
                    "operation": {
                        "const": "insert"
                    },
                    "table": {
                        "type": "string",
                        "minLength": 1
                    },
                    "col_names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minLength": 1
                    },
                    "col_types": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minLength": 1
                    },
                    "col_values": {
                        "type": "array",
                        "minLength": 1
                    },
                },
                "required": [
                    "operation",
                    "table",
                    "col_names",
                    "col_types",
                    "col_values"
                ]
            },
            "delete": {
                "type": "object",
                "properties": {
                    "operation": {
                        "const": "delete",
                    },
                    "table": {
                        "type": "string",
                        "minLength": 1
                    },
                    "value_to_delete": {
                        "type": "object",
                        "properties": {
                            "col_names": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "minLength": 1
                            },
                            "col_types": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "minLength": 1
                            },
                            "col_values": {
                                "type": "array",
                                "minLength": 1
                            }
                        },
                        "required": [
                            "col_names",
                            "col_types",
                            "col_values"
                        ]
                    }
                },
                "required": [
                    "operation",
                    "table",
                    "value_to_delete"
                ]
            }
        }
    }
