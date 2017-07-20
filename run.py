from tempfile import TemporaryDirectory
from time import sleep

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in

tmp_dir = TemporaryDirectory()

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in(tmp_dir.name, schema)
writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a",
                    content=u"This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b",
                    content=u"The second one is even more interesting!")
writer.commit()
from whoosh.qparser import QueryParser

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("first")
    results = searcher.search(query)
    results[0]
    print(results)
    print(results[0])

if __name__ == '__main__':
    print('yup')
    sleep(20)
