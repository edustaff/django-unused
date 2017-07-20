from tempfile import TemporaryDirectory

from whoosh import qparser
from whoosh.analysis import RegexTokenizer
from whoosh.util.text import rcompile

tokenizer = RegexTokenizer(expression=rcompile(r"[\w/.]+"))
for token in tokenizer(u"Hello there templates/app1/test.html!"):
    print(repr(token.text))

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in

tmp_dir = TemporaryDirectory()

schema = Schema(title=TEXT(stored=True),
                path=ID(stored=True),
                content=TEXT(analyzer=RegexTokenizer(expression=rcompile(r"[\w/.]+"))))
ix = create_in(tmp_dir.name, schema)
writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a",
                    content=u"this/is/a/test.html")
writer.add_document(title=u"Second document", path=u"/b",
                    content=u"this/is/a/hello.html   hello a yup")
writer.add_document(title=u"Second document", path=u"/b",
                    content=u"this is a hello.html   hello a yup")
writer.commit()
from whoosh.qparser import QueryParser

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema)
    query.remove_plugin_class(qparser.PhrasePlugin)
    # query.add_plugin(qparser.SequencePlugin("[\w/.]+"))
    query = query.parse('this/is/a/test.html')
    print(query)
    results = searcher.search(query)
    print(results)
    print(results[0])
    # print(results[1])

if __name__ == '__main__':
    print('yup')
    # sleep(20)
