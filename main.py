from TwitterDirect.Api import Api
from PostgreSQL import Database
from config import Config


def main():
    user_name = input("Please enter the username you want to dig:")
    target_user_name = input(
        "Please enter the username you want to skip, if you don't want, I will pull all users:")

    api = Api(cookies=Config.cookies)

    current_user = api.pull_user_info(user_name)

    print("Get Friend of user:%s" % current_user['screen_name'])
    users = api.pull_friends(user_name)

    database = Database.DataBase(Config.postgresql_address, Config.postgresql_database, Config.postgresql_user, Config.postgresql_password)

    is_skip = True

    if target_user_name == '':
        is_skip = False

    # name: nickname, screen_name: username in general way....But it may misunderstand in database part
    for user in users:

        if is_skip:
            print("Skip user: %s" % user['screen_name'])
            if user['screen_name'] == target_user_name:
                is_skip = False
            else:
                continue
        else:
            target_user_name = user['screen_name']

        database.insert(current_user['screen_name'], current_user['name'], user['screen_name'], user['name'])

        print("Get Friend of user:%s" % user['screen_name'])

        friend_users = api.pull_friends(user['screen_name'])
        for friend_users_user in friend_users:
            database.insert(user['screen_name'], user['name'], friend_users_user['screen_name'], friend_users_user['name'])


if __name__ == "__main__":
    main()
