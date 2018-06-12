from flask import Flask, Response
import graphene, json


class Section(graphene.ObjectType):
    text = graphene.String()

    def resolve_text(self, info):
        return self.text


class Guide(graphene.ObjectType):
    sections = graphene.List(lambda: Section)
    name = graphene.String()

    def resolve_name(self, info):
        return 'Guide'

    def resolve_sections(self, info):
        return [Section(text='uno'), Section(text='dos')]


class Query(graphene.ObjectType):
    hello = graphene.String()
    guides = graphene.List(lambda: Guide)

    def resolve_hello(self, info):
        return 'World'

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
        text
      }
    }
  }
''')
    
    return Response(json.dumps(result.data, indent=4), mimetype='application/json')


if __name__ == '__main__':
    app.run()
