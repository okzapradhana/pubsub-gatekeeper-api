def get_schema():
    return {
        "type": "object",
        "properties": {
            "activities": {
                "type": "array",
                "items": {
                    "anyOf": [
                      {
                          "$ref": "#/definitions/insert"
                      },
                        {
                          "$ref": "#/definitions/delete"
                      }
                    ]
                },
                "minItems": 1
            }
        },
        "definitions": {
            "insert": {
                "type": "object",
                "properties": {
                    "operation": {
                        "const": "insert"
                    },
                    "table": {
                        "type": "string"
                    },
                    "col_names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "col_types": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "col_values": {
                        "type": "array"
                    }
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
                        "const": "delete"
                    },
                    "table": {
                        "type": "string"
                    },
                    "value_to_delete": {
                        "type": "object",
                        "properties": {
                            "col_names": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "col_types": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "col_values": {
                                "type": "array"
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
