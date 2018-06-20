import os
import tempfile
import json

import pytest
import httpretty
import http.client

from app import app
from pyjsonassert import assert_json



@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):

    # mock github api
    httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
    httpretty.register_uri(httpretty.GET, "https://yipit.com/",
                           body="World")

    # connection = http.client.HTTPSConnection("yipit.com")
    # connection.request("GET", "/")
    # response = connection.getresponse()

    rv = client.get('/graphql')
    response_body = json.loads(rv.data.decode('ascii'))
    assert_json("{\"hello\": \"World\"}", response_body)

    httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
    httpretty.reset()
