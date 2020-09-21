import json
from social_core.backends.oauth import BaseOAuth2

class GitlabOAuth2(BaseOAuth2):
    """Gitlab v2 OAuth authentication backend"""

    name = 'gitlab'

    BASE_URL = 'https://gitlab.com'
    AUTHORIZATION_URL = BASE_URL + '/oauth/authorize'
    ACCESS_TOKEN_URL = BASE_URL + '/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    USER_INFO_URL = BASE_URL + '/api/v4/user'

    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = False
    STATE_PARAMETER = False
    SEND_USER_AGENT = False

    ID_KEY = 'username'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Hive account"""

        return {
            'username': response["username"],
            'first_name': response['name'],
            "email": response['email']
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""

        return self.get_json(self.USER_INFO_URL, method="GET", headers={
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        })
