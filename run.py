from elasticsearch_dsl import Search, Q
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

app = Flask(__name__)

# connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200/"])

# ambil semua berita dengan paginasi per 10 berita
@app.route("/news", methods=["GET"])
def get_all_news():
    page = request.args.get("page", default=1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    s = Search(using=es, index="news_indonesia")[start:end]
    response = s.execute()
    return jsonify([hit.to_dict() for hit in response])

# ambil berita berdasarkan sentimentasi
@app.route("/news/sentimen/<string:sentimen>", methods=["GET"])
def get_news_by_sentimen(sentimen):
    page = request.args.get("page", default=1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    s = Search(using=es, index="news_indonesia").query("match", sentimen=sentimen)[start:end]
    response = s.execute()
    return jsonify([hit.to_dict() for hit in response])

# start the server
if __name__ == "__main__":
    app.run(debug=True)