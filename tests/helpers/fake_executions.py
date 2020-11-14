# coding: utf8


async def fake_execution(train, __, query_name):
    return train.queries[query_name]


async def fake_execution_with_error(train, __, query_name):
    train.exception = {
        "args": [], "__traceback__": ""
    }
    return train.queries[query_name]


async def fake_execution_empty(*_):
    return {}
