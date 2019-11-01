import requests
import json
import random
import pyperclip


def make_url(uid, tokenid, phrase, format):
    url = 'http://www.stands4.com/services/v2/phrases.php'
    args = {'uid': uid, 'tokenid': tokenid, 'phrase': phrase, 'format': format}
    char = '?'
    for arg in args.keys():
        url += '{}{}={}'.format(char, arg, args[arg])
        char = '&'

    return url


def get_phrases_from_api(uid, tokenid, phrase, format):
    url = make_url(uid, tokenid, phrase, format)
    response_obj = requests.get(url)
    return response_obj.json()


def get_mock_response():
    with open('mock_response.json', encoding='utf-8') as f:
        content = json.load(f)

    return content


def init_credentials():
    with open('credentials.json', encoding='utf-8') as f:
        credentials = json.load(f)

    return credentials


def get_response(credentials):
    uid = credentials['uid']
    tokenid = credentials['tokenid']
    return get_phrases_from_api(uid, tokenid, 'fish', 'json')


def phrase_list_from_json(json_dict):
    phrase_list = []
    result = json_dict['result']
    for phrase in result:
        phrase_list.append(phrase['term'])

    return phrase_list


def get_phrases_with_text(phrase_list, text):
    phrases_with_text = []
    for phrase in phrase_list:
        if str.find(phrase, text) > -1:
            phrases_with_text.append(phrase)

    return phrases_with_text


def random_phrase(phrase_list):
    return random.choice(phrase_list)


def fish_to_phish(text):
    new_text = str.replace(text, 'fish', 'phish')
    return new_text


def sentencify(text):
    return '. '.join(i.strip().capitalize() for i in text.split('.'))


def main():
    try:
        print("Getting phrases from API...")
        credentials = init_credentials()
        response = get_response(credentials)
    except requests.exceptions.RequestException:
        print("API connection failed. Getting phrases from pre-made list...")
        response = get_mock_response()

    phrases = phrase_list_from_json(response)
    fish_phrases = get_phrases_with_text(phrases, 'fish')

    _phrase = random_phrase(fish_phrases)
    _phrase = fish_to_phish(_phrase)
    _phrase = sentencify(_phrase)

    pyperclip.copy(_phrase)

    print(_phrase)


if __name__ == '__main__':
    main()
