# coding: utf8
from app.core.statuses import Statuses as Code


async def fake_execution(self, storage_query, query_name):
    return self.train.queries[query_name]


async def fake_execution_with_error(self, storage_query, query_name):
    self.train.exception = {
        "args": [], "__traceback__": ""
    }
    return self.train.queries[query_name]


async def fake_execution_empty(self, storage_query, query_name):
    return {}
