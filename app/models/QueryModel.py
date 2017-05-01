import requests
import json

from config import config


class QueryModel:
    def __init__(self, settings):
        self.url = "%s/%s/%s/_search" % (settings['url'], settings['index'], settings['type'])

    def searchField(self, field, query, genres, imdb_score):
        payload = {}
        payload["size"] = 20
        payload["query"] = {"bool": {"should": []}}
        payload["query"]["bool"]["should"].append({"match": {field: query}})

        if len(genres):
            genres = genres.split(",")

            if len(genres):
                for genre in genres:
                    payload["query"]["bool"]["should"].append({"match": {"genres": genre}})
        print(imdb_score)
        if len(imdb_score):
            range_query = {"range": {"imdb_score": {"gte": imdb_score}}}
            payload["query"]["bool"]["filter"] = range_query

        data = json.dumps(payload)
        print(self.url, data)
        r = requests.get(self.url, data=data)
        if r.status_code == 200:
            return r.content
        else:
            return False
