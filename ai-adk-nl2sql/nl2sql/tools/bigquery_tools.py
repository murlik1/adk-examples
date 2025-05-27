from google.cloud import bigquery
from typing import List, Dict, Any

def bigquery_metdata_extraction_tool(PROJECT: str,
    BQ_LOCATION: str,
    DATASET: str) -> List[Dict[str, Any]]:
    """
        This is python program that extracts the bigquery tables and columns 
        for the given dataset provides the information in the form of list of dictionary.
        
        Args:
        `PROJECT`: GCP Project to execute the query on
        `BQ_LOCATION`: Bigquery Location
        `DATASET`: Name of the dataset
        
        Returns:
        List of dictionaries, Each dictionary in list contains the keys table_name, column_name, data_type and description of the column
    """
    client = bigquery.Client(project=PROJECT)

    query = f"""
        select table_name, column_name, data_type, description
        from `region-{BQ_LOCATION}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`
        where table_catalog = "{PROJECT}"
        and table_schema = "{DATASET}"
    """

    query_job = client.query(query)
    query_list = []

    for row in query_job:
        query_list.append(dict(row.items()))
    return query_list


def bigquery_execution_tool(PROJECT:str,
    query:str)-> List[Dict[str, Any]]:
    """
    This function is to execute a given bigquery standard sql on bigquery
    and return the results as list of dictionaries
    
    Args:
    `PROJECT` - GCP Project to execute the sql query on
    `query` - bigquery standard sql query

    Returns:
    List of dictionaries

    """
    client = bigquery.Client(project=PROJECT)

    query_job = client.query(query)
    query_list = []

    for row in query_job:
        query_list.append(dict(row.items()))
    return query_list