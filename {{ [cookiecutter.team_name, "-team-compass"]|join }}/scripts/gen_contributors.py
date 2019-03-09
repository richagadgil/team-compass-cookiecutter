
"""Generate HTML Contributors tables for team pages
"""
import pandas as pd
import os
import os.path as op
from ruamel import yaml

# Variables
N_PER_ROW = 4

# Init
path_data = op.join(op.dirname(op.abspath(__file__)), '..', 'team')
yaml = yaml.YAML()

template_start = '<td align="center" class="contrib_entry"><a href="{HANDLE_URL}"><img src="{AVATAR_URL}" class="headshot" alt="{NAME}" /><br /><p class="name"><b>{NAME}</b></p></a><p class="contrib_affiliation">{AFFILIATION}</p>'
template_contributions = '<p class="contributions">{CONTRIBUTIONS}</p></td>'
templates = {'jupyterhub': template_start + template_contributions }

def _generate_contributors(contributors, kind):
    """Generate an HTML list of contributors, given a dataframe of their information."""
    s = ['<table class="docutils contributors">', '<tr class="row-even">']
    for ix, person in contributors.iterrows():
        if ix % N_PER_ROW == 0 and ix != 0:
            s += ['</tr><tr class="row-even">']

        # Build contrib text
        this_contrib = person['contributions'].split(',')
        contrib_text = []
        for contrib in this_contrib:
            contrib_text += ['<span class="contribs contribs_text">{CONTRIB}</span>'.format(CONTRIB=contrib)]

        contrib_text = '<span class="contribs">,</span>'.join(contrib_text)

        # Find user gravatar url
        avatar_url = 'https://github.com/{HANDLE}.png?size=200'.format(HANDLE=person['handle'].lstrip('@'))

        # Add user
        format_dict = dict(HANDLE=person['handle'], HANDLE_URL="https://github.com/{HANDLE}".format(HANDLE=person['handle'].lstrip('@')),
                           AFFILIATION=person['affiliation'],
                           AVATAR_URL=avatar_url, NAME=person['name'], CONTRIBUTIONS=contrib_text)
        if kind == 'binder':
            format_dict.update(dict(TEAM=person['team']))

        # Render
        template = templates[kind]
        s += [template.format(**format_dict)]
    s += ['</table>']
    final_text = ['.. raw:: html', '']
    for line in s:
        final_text += ['   ' + line]
    final_text = '\n'.join(final_text)
    return final_text

contributors_files = [op.join(path_data, 'contributors-team.yaml')]
for ifile in contributors_files:
    with open(ifile, 'r') as ff:
        data = yaml.load(ff)
    people = pd.DataFrame(data)
    kind = 'binder' if 'binder' in ifile else 'jupyterhub'
    table = _generate_contributors(people, kind)
    new_name = os.path.splitext(ifile)[0]
    with open(new_name+'.txt', 'w') as ff:
        ff.write(table)