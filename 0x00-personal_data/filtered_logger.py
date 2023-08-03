#!/usr/bin/env python3
"""log message obfuscated"""
from typing import List
import re
import os
import logging
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initializer"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using"""
        message = filter_datum(self.fields, self.REDACTION,
                               super(RedactingFormatter, self).format(record),
                               self.SEPARATOR)
        return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logging.getLogger('user_data').setLevel(logging.INFO)
    logging.getLogger('user_data').propagate = False
    logging.getLogger('user_data').addHandler(logging.StreamHandler())
    logging.StreamHandler().setFormatter(RedactingFormatter(PII_FIELDS))
    return logging.getLogger('user_data')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    cnx = mysql.connector.connection.MySQLConnection(
        user=username, password=password, host=host, database=db_name)
    return cnx


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


def main():
    """main function that takes no arguments and returns nothing"""
    cnx = get_db()
    cnx.cursor().execute("SELECT * FROM users;")
    fields = [i[0] for i in cnx.cursor().description]

    for row in cnx.cursor():
        row_ = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        get_logger().info(row_.strip())
    cnx.cursor().close()
    cnx.close()
