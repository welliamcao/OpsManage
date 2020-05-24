#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import sqlparse
from collections import namedtuple
from sqlparse.sql import IdentifierList, Identifier, Function
from sqlparse.tokens import Keyword, DML, DDL, Punctuation
from .patch import KEYWORDS

TableReference = namedtuple('TableReference', ['schema', 'name', 'alias', 'is_function'])
TableReference.ref = property(
    lambda self: self.alias or (
        self.name if self.name.islower() or self.name[0] == '"' else '"' + self.name + '"')
)

sqlparse.keywords.KEYWORDS = KEYWORDS
 
class SQLParse:
        
    def is_subselect(self, parsed):
        if not parsed.is_group:
            return False
        for item in parsed.tokens:
            if item.ttype is DML and item.value.upper() in ('SELECT', 'INSERT', 'CREATE'):
                return True
        return False

    def _identifiers(self, tok):
        if isinstance(tok, IdentifierList):
            for t in tok.get_identifiers():
                if isinstance(t, Identifier):
                    yield t
        elif isinstance(tok, Identifier):
            yield tok 

    def extract_column_names(self, sql):
        parsed = sqlparse.parse(sql)[0]
        if not parsed:
            return ()        
        
        idx, tok = parsed.token_next_by(t=DML)
        tok_val = tok and tok.value.lower()
     
        if tok_val in ('insert', 'update', 'delete'):
            idx, tok = parsed.token_next_by(idx, (Keyword, 'returning'))
        elif not tok_val == 'select':
            return ()
     
        idx, tok = parsed.token_next(idx, skip_ws=True, skip_cm=True)
        return tuple(t.get_name() for t in self._identifiers(tok)) 
 
    def _identifier_is_function(self, identifier):
        return any(isinstance(t, Function) for t in identifier.tokens)
 
 
    def extract_from_part(self, parsed, stop_at_punctuation=True):
        tbl_prefix_seen = False
        for item in parsed.tokens:
            if tbl_prefix_seen:
                if self.is_subselect(item):
                    for x in self.extract_from_part(item, stop_at_punctuation):
                        yield x
                elif stop_at_punctuation and item.ttype is Punctuation:
                    raise StopIteration

                elif item.ttype is Keyword and (
                        not item.value.upper() == 'FROM') and (
                        not item.value.upper().endswith('JOIN')):
                    tbl_prefix_seen = False
                else:
                    yield item
            elif item.ttype is Keyword or item.ttype is Keyword.DML:
                item_val = item.value.upper()
                if (item_val in ('COPY', 'FROM', 'INTO', 'UPDATE', 'TABLE') or
                        item_val.endswith('JOIN')):
                    tbl_prefix_seen = True

            elif isinstance(item, IdentifierList):
                for identifier in item.get_identifiers():
                    if (identifier.ttype is Keyword and
                            identifier.value.upper() == 'FROM'):
                        tbl_prefix_seen = True
                        break
 
 
    def extract_table_identifiers(self, token_stream, allow_functions=True):
     
        def parse_identifier(item):
            name = item.get_real_name()
            schema_name = item.get_parent_name()
            alias = item.get_alias()
            if not name:
                schema_name = None
                name = item.get_name()
                alias = alias or name
            schema_quoted = schema_name and item.value[0] == '"'
            if schema_name and not schema_quoted:
                schema_name = schema_name.lower()
            quote_count = item.value.count('"')
            name_quoted = quote_count > 2 or (quote_count and not schema_quoted)
            alias_quoted = alias and item.value[-1] == '"'
            if alias_quoted or name_quoted and not alias and name.islower():
                alias = '"' + (alias or name) + '"'
            if name and not name_quoted and not name.islower():
                if not alias:
                    alias = name
                name = name.lower()
            return schema_name, name, alias
     
        for item in token_stream:
            if isinstance(item, IdentifierList):
                for identifier in item.get_identifiers():
                    try:
                        schema_name = identifier.get_parent_name()
                        real_name = identifier.get_real_name()
                        is_function = (allow_functions and
                                       self._identifier_is_function(identifier))
                    except AttributeError:
                        continue
                    if real_name:
                        yield TableReference(schema_name, real_name,
                                             identifier.get_alias(), is_function)
            elif isinstance(item, Identifier):
                schema_name, real_name, alias = parse_identifier(item)
                is_function = allow_functions and self._identifier_is_function(item)
     
                yield TableReference(schema_name, real_name, alias, is_function)
            elif isinstance(item, Function):
                schema_name, real_name, alias = parse_identifier(item)
                yield TableReference(None, real_name, alias, allow_functions)
 
 
    def extract_tables(self,sql):
        parsed = sqlparse.parse(sql)
        if not parsed:
            return ()
     
        insert_stmt = parsed[0].token_first().value.lower() == 'insert'
        stream = self.extract_from_part(parsed[0], stop_at_punctuation=insert_stmt)
        
        identifiers = self.extract_table_identifiers(stream, allow_functions=not insert_stmt)
        return tuple(i for i in identifiers if i.name)

    def extract_sql_keyword(self, sql):
        sql_type = 'unknown'
        keywords = []
        parsed = sqlparse.parse(sql)
        if not parsed:
            return ()
        _first_token = sqlparse.sql.Statement(parsed[0].tokens).token_first().value.upper()
        for item in parsed[0].tokens:
            if item.ttype is DML:
                sql_type = 'dml'
            elif item.ttype is DDL:
                sql_type = 'ddl'            
            key = item.value.upper()
            if (item.ttype is Keyword or \
                item.ttype is Keyword.DDL or item.ttype is Keyword.DML) and key not in keywords:
                keywords.append(item.value.upper())
        return sql_type, _first_token , keywords

sql_parse = SQLParse()

if __name__ == "__main__":  
    sql = """
    SELECT
        a.*, f.ORG_NAME DEPT_NAME,
        IFNULL(d.CONT_COUNT, 0) SIGN_CONT_COUNT,
        IFNULL(d.TOTAL_PRICE, 0) SIGN_CONT_MONEY,
        IFNULL(c.CONT_COUNT, 0) SIGN_ARRI_CONT_COUNT,
        IFNULL(c.TOTAL_PRICE, 0) SIGN_ARRI_CONT_MONEY,
        IFNULL(b.CONT_COUNT, 0) TOTAL_ARRI_CONT_COUNT,
        IFNULL(b.TOTAL_PRICE, 0) TOTAL_ARRI_MONEY,
        0 PUBLISH_TOTAL_COUNT,
        0 PROJECT_COUNT,
        0 COMMON_COUNT,
        0 STOCK_COUNT,
        0 MERGER_COUNT,
        0 INDUSTRY_COUNT,
        0 BRAND_COUNT
    FROM
        (
            SELECT
                u.USER_ID,
                u.REAL_NAME,
                u.ORG_PARENT_ID,
                o.ORG_NAME,
                u.ORG_ID
            FROM
                SE_USER u
            INNER JOIN SE_ORGANIZ o ON u.ORG_PARENT_ID = o.ORG_ID
            WHERE
                u.`STATUS` = 1
            AND u.`LEVEL` IN (1, 2, 3)
            AND o.PARENT_ID <> 0
        ) a 
    LEFT JOIN SE_ORGANIZ f ON a.ORG_ID = f.ORG_ID 
    LEFT JOIN (
        SELECT
            CUST_MGR_ID,
            COUNT(CONT_ID) CONT_COUNT,
            SUM(TOTAL_PRICE) TOTAL_PRICE
        FROM
            SE_CONTRACT
        WHERE
            DATE_FORMAT(CREATE_TIME, '%Y-%m-%d') = '2012-06-08'
        GROUP BY
            CUST_MGR_ID
    ) d ON a.USER_ID = d.CUST_MGR_ID 
    LEFT JOIN (
        SELECT
            CUST_MGR_ID,
            COUNT(CONT_ID) CONT_COUNT,
            SUM(TOTAL_PRICE) TOTAL_PRICE
        FROM
            SE_CONTRACT
        WHERE
            (STATUS = 6 OR STATUS = 10)
        AND DATE_FORMAT(CREATE_TIME, '%Y-%m-%d') = '2012-06-08'
        GROUP BY
            CUST_MGR_ID
    ) c ON a.USER_ID = c.CUST_MGR_ID 
    LEFT JOIN (
        SELECT
            c.CUST_MGR_ID,
            COUNT(c.CONT_ID) CONT_COUNT,
            SUM(c.TOTAL_PRICE) TOTAL_PRICE
        FROM
            SE_CONTRACT c
        INNER JOIN SE_CONT_AUDIT a ON c.CONT_ID = a.CONT_ID
        WHERE
            (c. STATUS = 6 OR c. STATUS = 10)
        AND a.IS_PASS = 1
        AND DATE_FORMAT(a.AUDIT_TIME, '%Y-%m-%d') = '2012-06-08'
        GROUP BY
            c.CUST_MGR_ID
    ) b ON a.USER_ID = b.CUST_MGR_ID
    ORDER BY
        a.ORG_PARENT_ID,
        a.USER_ID
    """
    
    print(sql_parse.extract_tables(sql))   
    print(sql_parse.extract_column_names(sql))  
    print(sql_parse.extract_sql_keyword("use abc"))     
    print(sql_parse.extract_sql_keyword(sql)) 
    
