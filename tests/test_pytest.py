import os
import tempfile
import json

import pytest

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

    rv = client.get('/graphql')
    response_body = json.loads(rv.data.decode('ascii'))
    assert_json("{\"hello\": \"World\"}", response_body)
