from collections import Mapping
import json
import os
import random
from six import string_types
from string import ascii_lowercase
import sys
import yaml

# set the base dir path
DIR = os.path.abspath(os.path.dirname(__file__))


def get_test_dirs():
    # get the list of directories to run tests on
    #  if provided on the command line
    if len(sys.argv) > 2:
        return [
            d for d in sys.argv[2].split(',')
            if '-' in d and len(d.split('-')) == 2
        ]
    # else get all of em
    else:
        return [
            os.path.join(DIR, d) for d in os.listdir(DIR)
            if os.path.isdir(os.path.join(DIR, d))
            and '-' in d
            and len(d.split('-')) == 2
        ]


def get_readme_path():
    # set README location
    # if commandline arg is docker
    if len(sys.argv) > 1 and sys.argv[1] == 'docker':
        return '/tmp/repo/README.md'
    # else local
    else:
        return os.path.join(DIR, 'README.md')


def get_json_path():
    # set README location
    # if commandline arg is docker
    if len(sys.argv) > 1 and sys.argv[1] == 'docker':
        return '/tmp/repo/results.json'
    # else local
    else:
        return os.path.join(DIR, 'results.json')



def get_config():
    # load the runtime config
    p = os.path.join(DIR, 'run_config.yaml')
    with open(p) as f:
        c = yaml.safe_load(f)

    if c:
        return c
    else:
        raise Exception('Issue loading config')


def get_solution(s=None):
    if s is None:
        s = CONFIG.get('solution', {}).get('value', '')
    t = CONFIG.get('solution', {}).get('type', 'string')

    if t == 'int':
        return int(s)
    elif t == 'float':
        return float(s)
    elif t == 'boolean':
        return bool(s)
    else:
        return str(s)


def get_letters():
    with open(os.path.join(DIR, 'data', 'letters.json')) as f:
        letters = json.load(f)

    return letters


def get_words():
    with open(os.path.join(DIR, 'data', 'dictionary.txt')) as f:
        words = f.read()

    return words.splitlines()


# Set contants
TEST_DIRS = get_test_dirs()
README = get_readme_path()
JSON = get_json_path()
CONFIG = get_config()
SOLUTION = get_solution()
SOLUTION_FIELD = CONFIG.get('leaderboard', {}).get('solutionField', 'Solution')
RANKING_FIELD = CONFIG.get('leaderboard', {}).get('rankingField', 'Time')
FIELDS = CONFIG.get('leaderboard', {}).get('fields', [])
OOPS_FIELDS = CONFIG.get('oops', {}).get('fields', [])
LETTERS = get_letters()
WORDS = get_words()


def build_test(d):
    if os.path.isfile(os.path.join(d, 'build.sh')):
        os.system('cd {} && bash build.sh'.format(d))


def run_test(d, test_input):
    test_out = os.popen(f'cd {d} && bash run.sh {test_input}').read()
    print(f'    {test_out}')
    return test_out


def transform_results(results):
    fields = CONFIG.get('leaderboard', {}).get('fields', [])
    temp_results = []
    for r in results:
        temp = {}
        for i, val in enumerate(r.replace('\n', '').split(',')):
            temp[fields[i]] = val.strip()
            if fields[i] == SOLUTION_FIELD:
                temp[SOLUTION_FIELD] = get_solution(temp[SOLUTION_FIELD])
            if fields[i] == RANKING_FIELD:
                temp[RANKING_FIELD] = float(temp[RANKING_FIELD])
        temp_results.append(temp)
    
    return temp_results

    # correct = [r for r in temp_results if r[SOLUTION_FIELD] == SOLUTION]
    # incorrect = [r for r in temp_results if r[SOLUTION_FIELD] != SOLUTION]
    # if correct:
    #     avg = sum(c[RANKING_FIELD] for c in correct) / len(correct)
    #     correct = correct[0]
    #     correct[RANKING_FIELD] = avg

    # if incorrect:
    #     solutions = ','.join([i[SOLUTION_FIELD] for i in incorrect])
    #     incorrect = incorrect[0]
    #     incorrect[SOLUTION_FIELD] = solutions

    # return correct, incorrect


def get_test_results(d, test_input):
    print('Building {}...'.format(d))
    build_test(d)
    results = []
    print('Running {}...'.format(d))
    for _ in range(CONFIG.get('testCount', 1)):
        results.append(run_test(d, test_input))

    return transform_results(results)


def get_readme():
    if os.path.isfile(README):
        with open(README) as f:
            readme = f.read()

        if readme:
            return readme

    raise Exception('No README file found at path: {}'.format(README))


def write_readme(readme):
    if os.path.isfile(README):
        with open(README, 'w') as f:
            f.write(readme)
    else:
        raise Exception('No README file found at path: {}'.format(README))


def strip_current_results(readme):
    leader = readme.find('### Leaderboard')
    oops = readme.find('### Oops')
    if leader:
        return readme[:leader]
    elif oops:
        return readme[:oops]

    return readme


def data_to_md_table(data, ordered_fields, title=None, sort_field=None,
                     extra=None):
    if not sort_field:
        sort_field = ordered_fields[0]

    # Transform data into table records
    # If data is a map, make it a list of maps
    if isinstance(data, Mapping):
        data = [data]

    # Data is a string, assume CSV in order. Go ahead and md-ify it
    if isinstance(data, string_types):
        data = ' | '.join(data.split(','))
    # else data is a list of dicts.
    else:
        if not ordered_fields:
            ordered_fields = sorted(list(data[0].keys()))

        data = '\n'.join([' | '.join([str(d.get(f)) for f in ordered_fields])
                         for d in sorted(
                             data, key=lambda k: k.get(sort_field))])

    # add header and divider
    header = ' | '.join(ordered_fields) + '\n'
    div = ' | '.join(['---' for _ in range(len(ordered_fields))]) + '\n'

    out = header + div + data + '\n\n'
    if extra:
        out = f'{extra}\n\n{out}'
    if title:
        if not title.endswith('\n\n'):
            title += '\n\n'

        out = title + out

    return out


def update_readme(correct, incorrect, inputs):
    readme = get_readme()
    readme = strip_current_results(readme)

    if correct:
        extra = 'Inputs: _{}_'.format(', '.join(inputs))
        readme += data_to_md_table(correct, FIELDS, title='### Leaderboard',
                                   sort_field=RANKING_FIELD, extra=extra)

    if incorrect:
        extra = 'Inputs: _{}_'.format(', '.join(inputs))
        readme += data_to_md_table(incorrect, OOPS_FIELDS, title='### Oops',
                                   extra=extra)

    write_readme(readme)


def get_random_letters():
    with open(os.path.join(DIR, 'data', 'letters.json')) as f:
        letters = json.load(f)

    word_length = random.randint(4, 10)
    word = ''

    while len(word) < word_length:
        l = random.choice(ascii_lowercase)
        if letters[l]['occurrence'] > 0:
            word += l
            letters[l]['occurrence'] -= 1

    vowel_check = [l for l in 'aeiouy' if l in word]
    if not vowel_check:
        return get_random_letters()
    else:
        return word


def sort_results(results, letters_in):
    for r in results:
        r.update({'input': letters_in})
    correct = []
    incorrect = []
    temp_correct = []
    results = sorted(results, key=lambda k: k[SOLUTION_FIELD], reverse=True)


    for r in results:
        if r[SOLUTION_FIELD] != results[0][SOLUTION_FIELD]:
            incorrect.append(r)
        else:
            temp_correct.append(r)

    for r in temp_correct:
        if r['Word'] not in WORDS:
            incorrect.append(r)
        elif not validate_score(r['Word'], r[SOLUTION_FIELD]):
            incorrect.append(r)
        else:
            correct.append(r)

    c_out = {}
    for c in correct:
        a = c.pop('Author')
        if a not in c_out:
            c_out[a] = []

        c_out[a].append(c)

    i_out = {}
    for i in incorrect:
        a = i.pop('Author')
        if a not in i_out:
            i_out[a] = []

        i_out[a].append(i)

    return c_out, i_out


def validate_score(word, score):
    calc = sum(LETTERS.get(l, {}).get('score', 0) for l in word)
    return score == calc


def dump_results(results):
    with open(JSON, 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == '__main__':
    master_results = {}
    for _ in range(5):
        letters_in = get_random_letters()
        master_results[letters_in] = {}
        results = []
        for d in TEST_DIRS:
            results += get_test_results(d, letters_in)
        
        correct, incorrect = sort_results(results, letters_in)
        if correct:
            master_results[letters_in]['correct'] = correct
        if incorrect:
            master_results[letters_in]['incorrect'] = incorrect

    print('Dumping results.json...')
    dump_results(master_results)
    # # need to then rank and update
    # print('Updating README.md...')
    # update_readme(correct, incorrect, list(master_results.keys()))
    print('Done')
