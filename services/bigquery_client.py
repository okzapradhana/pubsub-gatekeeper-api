from google.api_core.exceptions import GoogleAPIError
from google.cloud import bigquery
import os
import re

from google.cloud.bigquery.table import _EmptyRowIterator
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/chapmon/bootcamps/blank-space-de-batch1/week-4/script/keyfile.json'


class BigQueryClient():
    def __init__(self):
        self.client = bigquery.Client()
        self.project_id = 'static-gravity-312212'
        self.dataset_id = 'dataset_api'

    def check_table(self, table):
        """Check existence of a table in BigQuery

        Args:
            table [(string)]: [table name that want to check]

        Returns:
            [boolean]: [True if the table exist and False if the table doesn't exist]
        """
        check_query = (f'''
            SELECT COUNT(1) as count
            FROM `{self.project_id}.{self.dataset_id}.__TABLES_SUMMARY__`
            WHERE table_id='{table}'
        ''')
        results = self.run_query(check_query)
        data = results.next()

        if data.count == 0:
            raise ValueError(f"Table {table} is not exist!")

    def get_table_columns(self, table):
        self.check_table(table)
        columns_query = (f'''
            SELECT
                column_name
                FROM
                `{self.project_id}.{self.dataset_id}.INFORMATION_SCHEMA.COLUMNS`
            WHERE table_name = '{table}'
        ''')
        results = self.run_query(columns_query)
        column_names = [result.column_name for result in results]
        return column_names

    def insert(self, table, values, **schema):
        self.create_table_if_not_exists(table, schema)
        self.alter_table_column_if_not_exists(table, schema)
        rows = str(tuple(values))
        columns = f"{','.join(schema['column_names'])}"

        insert_query = (f'''
            INSERT `{self.project_id}.{self.dataset_id}.{table}` ({columns})
            VALUES{rows}

        ''')

        results = self.run_query(insert_query)

    def run_query(self, query_str):
        query_job = self.client.query(query_str)
        results = query_job.result()
        return results

    def alter_table_column_if_not_exists(self, table_name, schema):
        paired_schema = self.generate_pair_schema('alter', schema)

        alter_table_query = (f'''
            ALTER TABLE {self.project_id}.{self.dataset_id}.{table_name}
            {paired_schema}
        ''')

        query_job = self.client.query(alter_table_query)
        results = query_job.result()
        print(results)

    def generate_pair_schema(self, operation, schema):
        paired_schema = ''
        column_names = schema['column_names']
        column_types = schema['column_types']
        column_types = [self.datatype_mapper(
            column_type) for column_type in column_types]

        if operation == 'alter':
            for index, (name, dtype) in enumerate(zip(column_names, column_types)):
                # Default to Add Column because the constraint only Alter Adding Column
                paired_schema += f'ADD COLUMN IF NOT EXISTS {name} {dtype}{"," if index != len(column_names)-1 else ""}'
        elif operation == 'create':
            for name, dtype in zip(column_names, column_types):
                paired_schema += f'{name} {dtype},'

        return paired_schema

    def datatype_mapper(self, column_type):
        """Mapping from MySQL column data type to BigQuery schema

        Args:
            column_type ([string]): [original column data type that comes from MySQL]

        Returns:
            [string]: [column data type that followings BigQuery Schema https://cloud.google.com/bigquery/docs/schemas]
        """
        if column_type == 'TEXT' or 'VARCHAR' in column_type:
            return 'STRING'
        elif column_type == 'INTEGER':
            return 'INT64'
        elif 'FLOAT' in column_type or 'DOUBLE' in column_type:
            return 'FLOAT64'
        elif column_type == 'BOOLEAN':
            return 'BOOL'
        elif 'DECIMAL' in column_type:
            regex_result = re.findall(
                r'DECIMAL\((\d+),(\d+)\)', column_type)[0]
            return f'NUMERIC({regex_result[0]}{regex_result[1]})'
        return 'STRING'

    def create_table_if_not_exists(self, table_name, schema):
        paired_schema = self.generate_pair_schema('create', schema)

        create_tbl_query = (f'''
            CREATE TABLE IF NOT EXISTS {self.project_id}.{self.dataset_id}.{table_name}
            ({ paired_schema })
            '''
                            )
        results = self.run_query(create_tbl_query)
        print(results)

    def delete(self, table, values, **schema):
        self.check_table(table)
        column_names = schema['column_names']

        current_table_column = self.get_table_columns(table)
        column_differences = set(column_names).symmetric_difference(
            set(current_table_column))

        if len(list(column_differences)) > 0:
            raise ValueError("Column {} are not exist in table {}!".format(
                ', '.join(column_differences), table))

        '''
            TODO:   
                    setup grafana prometheus native and scrap from http endpoint
                    unit test --> just test schema for now
                    load test
        '''

        where_clause = ' AND '.join([f"{name} = {value}"
                                    if isinstance(value, int)
                                    else f"{name} = '{value}'"
                                    for name, value in zip(column_names, values)])
        delete_query = (f'''
            DELETE FROM `{self.project_id}.{self.dataset_id}.{table}`
            WHERE {where_clause}
        ''')
        results = self.run_query(delete_query)

        if isinstance(results, _EmptyRowIterator):
            print("Empty Row Result!")


def process(transactions):
    bq = BigQueryClient()

    for activity in transactions['activities']:
        table = activity['table']
        if activity['operation'] == 'insert':
            values = activity['col_values']
            bq.insert(
                table,
                values,
                column_names=activity['col_names'], column_types=activity['col_types'])
        elif activity['operation'] == 'delete':
            values = activity['value_to_delete']['col_values']
            bq.delete(
                table,
                values,
                column_names=activity['value_to_delete']['col_names'],
                column_types=activity['value_to_delete']['col_types'])
