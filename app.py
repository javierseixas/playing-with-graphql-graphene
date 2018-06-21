import graphene
import json
import http.client
from flask import Flask, Response


class Article(graphene.ObjectType):
    content = graphene.String()

    def resolve_content(self, info):
        return "hello I'm content"


class Section(graphene.ObjectType):
    name = graphene.String()
    article = graphene.Field(Article)

    # def resolve_name(self, info):
    #     return "Seccion"

    def resolve_article(self, info):
        return Article(content="This is content")


class Guide(graphene.ObjectType):
    sections = graphene.List(lambda: Section)
    name = graphene.String()

    def resolve_name(self, info):
        return 'Guide'

    def resolve_sections(self, info):
        return [Section(name='uno'), Section(name='dos')]


class Query(graphene.ObjectType):
    hello = graphene.String()
    guides = graphene.List(lambda: Guide)

    def resolve_hello(self, info):
        # connection = http.client.HTTPSConnection("yipit.com")
        # connection.request("GET", "/")
        # response = connection.getresponse()
        # return response.read().decode("utf-8")
        return "World"

    def resolve_guides(self, info):
        return [Guide()]


schema = graphene.Schema(query=Query)


app = Flask(__name__)


@app.route('/graphql')
def hello_world():
    result = schema.execute('''
  query {
    hello
    guides {
      name
      sections {
        name
        article {
          content
        }
      }
    }
  }
''')
    
    return Response(json.dumps(result.data, indent=4), mimetype='application/json')


if __name__ == '__main__':
    app.run()
