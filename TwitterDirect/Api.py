import re

import requests


class Api:
    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.headers.update({'Accept-Encoding': 'gzip, deflate, br',
                                     'Accept-Language': 'zh-CN,zh;q=0.9,en-XA;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5',
                                     'accept': 'application/json, text/javascript, */*; q=0.01',
                                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                                                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 '
                                                   'Safari/537.36',
                                     'Authority': 'twitter.com',
                                     'referer': 'https://twitter.com//following',
                                     'Cookie': cookies})

    def pull_friends(self, user_screen_name):
        data = []

        position = '-1'
        while True:
            return_data = self.session.get("https://twitter.com/" + user_screen_name + "/following/users",
                                           params={'include_available_features': 1, 'include_entities': 1,
                                                   'max_position': position,
                                                   'reset_error_state': 'false'}, stream=True)

            return_data = return_data.json()

            position = return_data['min_position']
            users = return_data['items_html']
            users = re.compile(
                r"<a class=\"ProfileCard-avatarLink js-nav js-tooltip\" href=\"/(.*?)\" title=\"(.*?)\" tabindex=\"-1\" aria-hidden=\"true\" >",
                flags=re.M).findall(users)
            for user in users:
                data.append({'screen_name': user[0], 'name': user[1]})
            if not return_data['has_more_items']:
                break
            else:
                print("Get: %i" % len(data))

        return data

    def pull_followers(self, user_screen_name):
        data = []

        position = '-1'
        while True:
            return_data = self.session.get("https://twitter.com/" + user_screen_name + "/followers/users",
                                           params={'include_available_features': 1, 'include_entities': 1,
                                                   'max_position': position,
                                                   'reset_error_state': 'false'}, stream=True)

            return_data = return_data.json()

            position = return_data['min_position']
            users = return_data['items_html']
            users = re.compile(
                r"<a class=\"ProfileCard-avatarLink js-nav js-tooltip\" href=\"/(.*?)\" title=\"(.*?)\" tabindex=\"-1\" aria-hidden=\"true\" >",
                flags=re.M).findall(users)
            for user in users:
                data.append({'screen_name': user[0], 'name': user[1]})
                print({'screen_name': user[0], 'name': user[1]})
            if not return_data['has_more_items']:
                break
            else:
                print("Get: %i" % len(data))

        return data

    def pull_user_info(self, user_screen_name):
        return_data = self.session.get("https://twitter.com/" + user_screen_name, stream=True)

        user = re.compile(
            r"<title>(.*?) \(@(.*?)\) \| Twitter</title>",
            flags=re.M).findall(return_data.text)

        return {'name': user[0][0], 'screen_name': user[0][1]}


if __name__ == "__main__":
    api = Api(cookies='only for test')

    print(api.pull_user_info("glzjin"))
