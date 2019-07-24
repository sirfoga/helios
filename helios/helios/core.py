# -*- coding: utf-8 -*-

""" Interacts with EOS db """

from pymongo import MongoClient

# todo from helios.helios.io import AstraeusDataSaver
from helios.helios.io import AstraeusDataSaver
from helios.models.query.eos import EosQueryBuilder
from helios.models.query.sql import SqlQueryAdapter


class Helios:
    def __init__(self, config):
        self.config = config
        self.client = MongoClient(
            self.config.get_db_server(),
            self.config.get_db_port()
        )
        self.db_name = self.config.get_db_name()
        self.collection_name = self.config.get_coll_name()

        self.query_builder = self._get_query_builder()
        self.driver = self.client[self.db_name][self.collection_name]

        self.saver = AstraeusDataSaver(self.config.get_output())

    def with_params(self, raw_sql):
        try:
            query = SqlQueryAdapter().build(raw_sql)
            query.set_driver(self.query_builder.driver)

            return query
        except:
            raise ValueError('Cannot parse "{}" query'.format(raw_sql))

    def builder(self):
        return self.query_builder

    def save_to_disk(self, results):
        return self.saver.save_json(results)

    def get_download_link(self, val):
        return self.saver.get_download_key_for(val)

    def download(self, results):
        try:
            if len(results) > 1:
                return self.saver.download_multiple(results)
        except:
            pass  # todo

        return self.saver.download_as_json(results)

    def _get_query_builder(self):
        return EosQueryBuilder(
            self.client,
            self.db_name,
            self.collection_name
        )
