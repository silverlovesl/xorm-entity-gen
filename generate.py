# -*- coding: utf-8 -*-
import json
import pandas as pd
import pandas.io.sql as psql
import MySQLdb
import sys
import argparse
import re
import inflection


def parse_param():
    """
    Parse parameter
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='User for login if not current user')
    parser.add_argument('-p', '--passwd', help='Password to use when connecting to server.')
    parser.add_argument('-P', '--port', type=int, help='Port to use when connecting to server.', default=3306)
    parser.add_argument('-H', '--host', help='Server host', default='localhost')
    parser.add_argument('-d', '--database', help='Database to use')
    parser.add_argument('--package_name', help='Go package name', default="entities")
    parser.add_argument('-t', '--table_name', help='Table name')
    # parser.add_argument('-o', '--output_path', help='Output path', default='./')
    parser.add_argument('--charset', help='Charset,default [utf8]', default='utf8')
    return parser


def snake_to_camel(word):
    """
    Convert word to camel case ex: COMPANY_ID => CompanyId
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def fix_go_lint(word):
    """
    To avoid go lint warning, convert 
    """
    word = word.replace("Id", "ID")
    word = word.replace("Url", "URL")
    return word


def handle_col_extra(extra):
    extra = extra.lower()
    rtnV = ""
    if extra.startswith("auto_increment"):
        rtnV = " autoincr"
    return rtnV


def mapto_go_type(type_name, is_allow_null):
    """
    Map mysql and golang data type
    """
    type_name = type_name.lower()
    rtnV = ""
    if type_name.startswith("varchar") or type_name.startswith("char") or type_name.startswith("text"):
        rtnV = "string" if not is_allow_null else "null.String"
    elif type_name.startswith("int") or type_name.startswith("bigint"):
        rtnV = "int" if not is_allow_null else "null.Int"
    elif type_name.startswith("decimal") or type_name.startswith("numeric") or type_name.startswith("double"):
        rtnV = "float64" if not is_allow_null else "null.Float"
    elif type_name.startswith("bit") or type_name.startswith("tinyint"):
        rtnV = "bool" if not is_allow_null else "null.Bool"
    elif type_name.startswith("timestamp") or type_name.startswith("date") or type_name.startswith("datetime"):
        rtnV = "time.Time" if not is_allow_null else "null.Time"
    return rtnV


def init_engine(opt):
    """
    Map mysql and golang data type
    """
    connect = MySQLdb.connect(host=opt.host,
                              port=opt.port,
                              user=opt.user,
                              passwd=opt.passwd,
                              db=opt.database,
                              charset=opt.charset)
    return connect


def create_entity_for_xorm(df, package_name, table_name):
    table_name = snake_to_camel(table_name)
    singularized_table_name = inflection.singularize(table_name)
    entity_source = ["package {}\n".format(package_name)]
    entity_source.append("// {} Entity".format(singularized_table_name))
    entity_source.append("type {} struct {{".format(singularized_table_name))

    for index, row in df.iterrows():
        col_name = row["Field"]
        col_type = row["Type"]
        col_is_key = row["Key"].upper() == "PRI"
        col_allow_null = row["Null"].upper() == "YES"
        col_default = row["Default"]
        col_extra = row["Extra"]

        field_name = snake_to_camel(col_name)
        field_name = fix_go_lint(field_name)
        go_type = mapto_go_type(col_type, col_allow_null)
        extra_name = handle_col_extra(col_extra)

        key = " pk" if col_is_key else ""
        entity_source.append("{} {} `xorm:\"\'{}\'{}{}\"`".format(field_name, go_type, col_name, key, extra_name))

    entity_source.append("}")
    return "\n".join(entity_source)


def main():
    # DB connection
    conn = None
    parser = None

    try:
        parser = parse_param()
        args = parser.parse_args()
        conn = init_engine(args)
        df = psql.read_sql("DESC {}".format(args.table_name), con=conn)
        entity_code = create_entity_for_xorm(df, args.package_name, args.table_name)
        print(entity_code)
    except TypeError as e:
        print("\ndemo:\n\t python generate.py --user=root --passwd= --database=my_db --table_name=CUSTOMER > ./customer.go\n\n")
        parser.print_help(sys.stderr)
    except MySQLdb.Error as e:
        print("Bad connection, please check your argument\n")
        print(e)
        print(args)
    except psql.DatabaseError as e:
        print(e)
    finally:
        if not conn is None:
            conn.close()


if __name__ == '__main__':
    main()
