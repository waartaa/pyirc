# -*- coding: utf-8 -*-
import asyncio

from uuid import uuid1

from ircb.lib.dispatcher import Dispatcher


class BaseStore(object):
    CREATE_SIGNAL = None
    CREATED_SIGNAL = None
    UPDATE_SIGNAL = None
    UPDATED_SIGNAL = None
    DELETE_SIGNAL = None
    DELETED_SIGNAL = None
    CREATE_OR_UPDATE_SIGNAL = None

    callbacks = {
        'create': set(),
        'update': set(),
        'delete': set()
    }

    raw_callbacks = {
        'create': set(),
        'update': set(),
        'delete': set()
    }

    model = None

    @classmethod
    def initialize(cls):
        signals = [cls.CREATED_SIGNAL, cls.UPDATED_SIGNAL, cls.DELETED_SIGNAL]
        for signal in signals:
            if signal is None:
                continue
            dispatcher.register(cls._on_message, signal=signal)

    @classmethod
    async def get(cls, data, raw=False):
        result = await cls._get(data)
        if isinstance(result, dict):
            result = cls.model.from_dict(result) if raw is False else result
        elif isinstance(result, tuple):
            if raw:
                result = result
            else:
                result = [cls.model.from_dict(item) for item in result]
        return result

    @classmethod
    async def create(cls, data, isasync=False, timeout=10):
        result = await cls._create(data, isasync)
        return cls.model(**result)

    @classmethod
    async def update(cls, data):
        result = await cls._update(data)
        return cls.model(**result)

    @classmethod
    async def delete(cls, data):
        result = await cls._delete(data)
        return result

    @classmethod
    async def create_or_update(cls, data):
        result = await cls._create_or_update(data)
        return cls.model.from_dict(result)

    @classmethod
    async def _get(cls, data):
        task_id = cls.get_task_id(data)
        fut = asyncio.Future()

        def callback(signal, data, taskid=None):
            if taskid == task_id:
                fut.set_result(data)

        dispatcher.register(callback, signal=cls.GOT_SIGNAL)
        dispatcher.send(cls.GET_SIGNAL, data, taskid=task_id)

        result = await fut
        return fut.result()

    @classmethod
    async def _create(cls, data, isasync=False):
        task_id = cls.get_task_id(data)
        fut = asyncio.Future()

        def callback(signal, data, taskid=None):
            if taskid == task_id:
                fut.set_result(data)

        dispatcher.register(callback, signal=cls.CREATED_SIGNAL)
        dispatcher.send(cls.CREATE_SIGNAL, data, taskid=task_id)

        result = await fut
        return fut.result()

    @classmethod
    async def _update(cls, data):
        task_id = cls.get_task_id(data)
        future = asyncio.Future()

        def callback(signal, data, taskid=None):
            if taskid == task_id:
                future.set_result(data)
        dispatcher.register(callback, signal=cls.UPDATED_SIGNAL)
        dispatcher.send(cls.UPDATE_SIGNAL, data, taskid=task_id)

        result = await future
        return result

    @classmethod
    async def _delete(cls, data):
        task_id = cls.get_task_id(data)
        future = asyncio.Future()

        def callback(signal, data, taskid=None):
            if taskid == task_id:
                future.set_result(data)
        dispatcher.register(callback, signal=cls.DELETED_SIGNAL)
        dispatcher.send(cls.DELETE_SIGNAL, data, taskid=task_id)

        result = await future
        return result

    @classmethod
    async def _create_or_update(cls, data, isasync=False):
        task_id = cls.get_task_id(data)
        fut = asyncio.Future()

        def callback(signal, data, taskid=None):
            if taskid == task_id:
                fut.set_result(data)

        dispatcher.register(callback, signal=cls.CREATED_SIGNAL)
        dispatcher.register(callback, signal=cls.UPDATED_SIGNAL)
        dispatcher.send(cls.CREATE_OR_UPDATE_SIGNAL, data, taskid=task_id)

        result = await fut
        return fut.result()

    @classmethod
    def on(cls, action, callback, remove=False, raw=False):
        callbacks = cls.raw_callbacks if raw else cls.callbacks
        if remove:
            callbacks[action].remove(callback)
        else:
            callbacks[action].add(callback)

    @classmethod
    def _on_message(cls, signal, data, taskid=None):
        callbacks = None
        raw_callbacks = None
        if signal == cls.CREATED_SIGNAL:
            callbacks = cls.callbacks['create']
            raw_callbacks = cls.raw_callbacks['create']
        elif signal == cls.UPDATED_SIGNAL:
            callbacks = cls.callbacks['update']
            raw_callbacks = cls.raw_callbacks['update']
        elif signal == cls.DELETED_SIGNAL:
            callbacks = cls.callbacks['delete']
            raw_callbacks = cls.raw_callbacks['delete']
        if callbacks:
            for callback in callbacks:
                callback(cls.model.from_dict(data))
        if raw_callbacks:
            for callback in raw_callbacks:
                callback(data)

    @classmethod
    def get_task_id(self, data):
        return str(uuid1())

    @classmethod
    def fields(cls):
        return [col.name for col in cls.model.__table__.columns]


def init():
    global dispatcher
    dispatcher = Dispatcher(role='storeclient')

dispatcher = None
