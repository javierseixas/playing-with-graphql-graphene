import os
import unittest
from app import app

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #                                        os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/graphql', follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()