from collections import Mapping
from collections import OrderedDict
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
    # set test_results.json location
    # if commandline arg is docker
    if len(sys.argv) > 1 and sys.argv[1] == 'docker':
        return '/tmp/repo/test_results.json'
    # else local
    else:
        return os.path.join(DIR, 'test_results.json')


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


def get_dictionary():
    with open(os.path.join(DIR, 'data', 'dictionary.txt')) as f:
        words = [w.strip() for w in f.readlines() if len(w.strip()) <= 7]

    return words


def get_letters():
    with open(os.path.join(DIR, 'data', 'letters.json')) as f:
        return json.load(f)


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
WORDS = get_dictionary()
LETTERS = get_letters()


def build_test(d):
    if os.path.isfile(os.path.join(d, 'build.sh')):
        os.system('cd {} && bash build.sh'.format(d))


def run_test(d, test_case):
    test_out = os.popen(f'cd {d} && bash run.sh {test_case}').read().strip()
    print(f'    {test_out}')
    return parse_result(test_out)


def get_test_results(d, test_case):
    print(f'\nBuilding {d}...')
    build_test(d)
    results = []
    print('Running {}...'.format(d))
    for _ in range(CONFIG.get('testCount', 1)):
        results.append(run_test(d, test_case))

    return results


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
        if not extra.endswith('\n\n'):
            extra += '\n\n'

        out = extra + out

    if title:
        if not title.endswith('\n\n'):
            title += '\n\n'

        out = title + out

    return out


def update_readme(inputs, correct, incorrect):
    readme = get_readme()
    readme = strip_current_results(readme)

    if correct:
        fields = list(correct[0].keys())
        extra = '__Inputs__: _{}_'.format(', '.join(inputs))
        readme += data_to_md_table(correct, fields, title='### Leaderboard',
                                   sort_field=RANKING_FIELD, extra=extra)

    if incorrect:
        fields = list(incorrect[0].keys())
        readme += data_to_md_table(incorrect, fields, title='### Oops')

    write_readme(readme)


def run_test_set(test_case):
    results = []
    for d in TEST_DIRS:
        results += get_test_results(d, test_case)

    return results


def get_random_letters():
    with open(os.path.join(DIR, 'data', 'letters.json')) as f:
        letters = json.load(f)

    word_length = random.randint(4, 7)
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


def dump_json_results(results):
    print('\nDumping  test_results.json...')
    with open(JSON, 'w') as f:
        json.dump(results, f, indent=2)


def parse_result(result):
    result = [r.strip() for r in result.split(',')]
    out = OrderedDict()
    for i, f in enumerate(FIELDS):
        v = result[i]
        if f == SOLUTION_FIELD:
            v = get_solution(v)
        elif f == RANKING_FIELD:
            v = float(v)

        out[f] = v

    return out


def dict_check(word):
    return word in WORDS


def score_check(word, score):
    calc = sum(LETTERS.get(l, {}).get('score', 0) for l in word)
    return score == calc


def split_results(results):
    results = sorted(results, key=lambda k: k['Score'], reverse=True)
    correct = []
    incorrect = []
    top_score = None
    for r in results:
        if not dict_check(r['Word']) or not score_check(r['Word'], r['Score']):
            incorrect.append(r)
        elif top_score and r['Score'] != top_score:
            incorrect.append(r)
        elif not top_score:
            correct.append(r)
            top_score = r['Score']
        else:
            correct.append(r)

    return correct, incorrect


def consolidate_corrects(results):
    out = OrderedDict()
    all_c = []
    for k, v in results.items():
        all_c += v

    users = set([x['Author'] for x in all_c])
    for case, result in results.items():
        temp = []
        for u in users:
            match = [r for r in result if r['Author'] == u]
            if match:
                t = match[0]
                t['Time (ms)'] = \
                    sum(m['Time (ms)'] for m in match) / len(match)
            else:
                t = OrderedDict([
                    ('Author', u),
                    ('Time (ms)', max(r['Time (ms)'] for r in result)),
                    ('Notes','Max time penalty applied')
                ])
            temp.append(t)
        out[case] = sorted(temp, key=lambda k: k['Time (ms)'])

    all_c = []
    for k, v in out.items():
        all_c += v

    temp = []
    for u in users:
        match = [r for r in all_c if r['Author'] == u]
        t = match[0]
        t['Word'] = ', '.join(m['Word'] for m in match)
        t['Score'] = ', '.join(str(m['Score']) for m in match)
        t['Time (ms)'] = sum(m['Time (ms)'] for m in match) / len(match)
        temp.append(t)

    out['consolidated'] = sorted(temp, key=lambda k: k['Time (ms)'])

    return out


def consolidate_incorrects(results):
    out = []
    for case, r_set in results.items():
        users = set([r['Author'] for r in r_set])
        for u in users:
            match = [r for r in r_set if r['Author'] == u]
            t = OrderedDict([
                ('Author', u),
                ('Input', case),
                ('Words', ', '.join(m['Word'] for m in match)),
                ('Scores', ', '.join(m['Score'] for m in match))
            ])
            out.append(t)

    return out


if __name__ == '__main__':
    raw_results = OrderedDict()
    for _ in range(5):
        test_case = get_random_letters()
        results = run_test_set(test_case)
        raw_results[test_case] = results

    print('\nSorting and calculating rankings...')
    correct = OrderedDict()
    incorrect = OrderedDict()
    for test_case, results in raw_results.items():
        correct[test_case], incorrect[test_case] = split_results(results)

    correct = consolidate_corrects(correct)
    incorrect = consolidate_incorrects(incorrect)
    master_results = OrderedDict([
        ('Overall Rankings', correct.pop('consolidated')),
        ('Correct', correct),
        ('Incorrect', incorrect),
        ('Raw results', raw_results)
    ])

    dump_json_results(master_results)
    print('\nUpdating README.md...')
    inputs = list(correct.keys())
    update_readme(inputs, master_results['Overall Rankings'], incorrect)
    print('\nDone')
