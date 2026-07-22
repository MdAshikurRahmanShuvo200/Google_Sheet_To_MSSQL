import re


def make_table_name(sheet_name):

    table_name = sheet_name.lower()

    table_name = table_name.replace(" ", "_")

    table_name = re.sub(r'[^a-z0-9_]', '', table_name)

    return table_name


def make_column_name(column_name):

    column = column_name.strip()

    column = column.replace("\n", " ")

    column = re.sub(r"\s+", " ", column)

    return column