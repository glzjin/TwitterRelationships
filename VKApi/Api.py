#By: glzjin

import vk

class Api:
    def __init__(self, cookies = None):
        self.session = vk.InteractiveAuthSession(app_id='6754031')
        self.api = vk.API(self.session)

    def pull_friends(self, user_screen_name=None):
        data = []

        users = self.api.friends.get(v='5.87', user_id=user_screen_name, fields='first_name,last_name')

        for user in users['items']:
            data.append({'name': user['first_name'] + ' ' + user['last_name'], 'screen_name': user['id']})

        return data

    def pull_followers(self, user_screen_name=None):
        return self.pull_friends(user_screen_name)

    def pull_user_info(self, user_screen_name=None):
        user = self.api.users.get(v='5.87', user_ids=user_screen_name)

        return {'name': user[0]['first_name'] + ' ' + user[0]['last_name'], 'screen_name': user[0]['id']}


if __name__ == "__main__":
    api = Api()
    print(api.pull_user_info())
