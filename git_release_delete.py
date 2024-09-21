import json
import subprocess


def command(*add):
    return [
        r'C:\Users\WorkSpace\Downloads\curl-8.10.0_1-win64-mingw\bin\curl.exe',
        '-H', 'Accept: application/vnd.github.v3+json',
        '-H', f'Authorization: {token}',
        *add
    ]


def version_key(version):
    version = version.replace('-Alpha', '')
    return tuple(map(int, version.split('.')))


def get_releases():
    releases_command = command('-X', 'GET', f'{releases}')
    res = (subprocess
           .run(releases_command, shell=True, capture_output=True, text=True, encoding='utf-8')
           .stdout
           )
    res = json.loads(res)

    same_tags_ = []

    for r in res:
        if r['tag_name'].endswith('Alpha'):
            same_tags_.append((r['tag_name'], r['id']))

    return sorted(same_tags_, key=lambda x: version_key(x[0]))


def get_tags():
    get_tags_command = command('-X', 'GET', 'https://api.github.com/repos/SleepAswell/SAW_BackEnd/tags')

    res = (subprocess
           .run(get_tags_command, capture_output=True, text=True, encoding='utf-8')
           .stdout
           )

    res = json.loads(res)

    return [x['name'] for x in filter(lambda x: str(x['name']).endswith('-Alpha'), res)]


def get_del_releases_commands(same_tags_):
    del_urls_ = []
    for tag_, id_ in same_tags_:
        if version_key(tag_) <= version_key(deleteEndTag):
            url = f'{releases}/{id_}'
            del_urls_.append(url)

    del same_tags_
    del_commands_ = []
    for del_url in del_urls_:
        del_commands_.append(command('-X', 'DELETE', del_url))

    return del_commands_


def get_del_tags_commands(used_tags_):
    owned_tags = sorted(get_tags(), key=version_key)
    for tag, _ in used_tags_:
        owned_tags.remove(tag)

    del used_tags_

    del_tag_command_ = []
    for tag in owned_tags:
        del_tag_rul = f'https://api.github.com/repos/SleepAswell/SAW_BackEnd/git/refs/tags/{tag}'
        del_tag_command_.append(command('-X', 'DELETE', del_tag_rul))

    return del_tag_command_


if __name__ == '__main__':
    with open('http-client.env.json', 'r') as key:
        keys = json.loads(key.read())
        token = keys['git_del_rel']['git_token']

    print(token)

    releases = r'https://api.github.com/repos/SleepAswell/SAW_BackEnd/releases'
    deleteEndTag = '0.0.5'

    same_tags = get_releases()
    del_commands = get_del_releases_commands(same_tags)
    del same_tags

    for command in del_commands:
        subprocess.run(command, shell=True)

    used_tags = get_releases()
    del_tags_commands = get_del_tags_commands(used_tags)
    del used_tags
    for command in del_tags_commands:
        subprocess.run(command, shell=True)
