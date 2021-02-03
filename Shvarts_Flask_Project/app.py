from flask import Flask, render_template, request, jsonify
import pymongo
import json

app = Flask(__name__)
def get_poems_titles():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['admin']
    collection_60 = db.Shvarts_60
    titles = [title for title in collection_60.find({"title": {"$exists": True}})]
    return titles


def get_poems_texts(ID):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['admin']
    collection_60 = db.Shvarts_60
    poem_texts = [text for text in collection_60.find({"poem_text": {"$exists": True}, "ID":ID})]
    return poem_texts 

def search_result(word):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['admin']
    collection_60 = db.Shvarts_60
    # texts = [text for text in collection_60.find({"poem_text": {"$exists": True}}, 
    #                                              projection={"_id":False, "meta": False})]
    texts = [text for text in collection_60.find({"$text": {"$search": word}}, 
             projection={'_id':False, 'meta':False})]

    poems = []

    for text in texts:
        lst = []
        lst.append(text.get('ID'))
        lst.append(text.get('title'))
        poems.append(lst)

    return poems



@app.route('/')
def base():
    return render_template('base.html', page_name="swartz")

@app.route('/about/')
def index():
    return render_template('index.html', page_name='project')

@app.route('/list_of_texts/')
def get_list_of_texts():
    titles = get_poems_titles()
    return render_template('titles.html', page_name='list_of_texts', 
                            titles=titles)

@app.route('/texts_60_<int:ID>/')
def get_text(ID):
    poem_texts = get_poems_texts(ID)
    return render_template('text.html', page_name='texts', 
                            poem_texts=poem_texts)
def get_text_by_link(ID):
    poem_texts = get_poems_texts(ID)
    return render_template('text.html', page_name='texts', 
                            poem_texts=poem_texts)

@app.route('/search/')
def search():
    return render_template('search.html',
                            page_name='search')


@app.route('/background_process', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def background_process():
    try:
        word = request.args.get('search', 'text', type=str)
        result = search_result(word)
        return jsonify(result=result)
    except Exception as e:
        return str(e)

@app.route('/contrib/')
def contrib():
    return render_template('contrib.html',
                            page_name='contributions')


if __name__=='__main__':
    app.run(debug=True)

