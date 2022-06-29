import os
import shutil
import time
from pathlib import Path

import git
import pytest

from gitpandas import ProjectDirectory, Repository

PROJECT_DIR = Path(__file__).resolve().parent / "repos"
REPO1_DIR = PROJECT_DIR / "repository1"
REPO2_DIR = PROJECT_DIR / "repository2"


@pytest.fixture(scope="session")
def make_temp_repos():

    if PROJECT_DIR.exists():
        shutil.rmtree(PROJECT_DIR)

    PROJECT_DIR.mkdir()
    REPO1_DIR.mkdir()
    REPO2_DIR.mkdir()

    # create an empty repo (but not bare)
    grepo1 = git.Repo.init(REPO1_DIR)
    grepo2 = git.Repo.init(REPO2_DIR)

    # add a file
    with open(REPO1_DIR / 'README.md', 'w') as f:
        f.write('Sample README for a sample python project\n')

    # add a file
    with open(REPO2_DIR / 'README.md', 'w') as f:
        f.write('Sample README for a sample js project\n')

    # commit them
    grepo1.git.add('README.md')
    grepo1.git.commit(m='first commit')

    grepo2.git.add('README.md')
    grepo2.git.commit(m='first commit')

    # now add some other files:
    for idx in range(5):
        with open(REPO1_DIR / f'file_{idx}.py', 'w') as f:
            f.write('import sys\nimport os\n')

        grepo1.git.add(all=True)
        grepo1.git.commit(m=' "adding file_%d.py"' % (idx,))

        # now add some other files:
        with open(REPO2_DIR / f'file_{idx}.js', 'w') as f:
            f.write('document.write("hello world!");\n')

        grepo2.git.add(all=True)
        grepo2.git.commit(m=' "adding file_%d.js"' % (idx,))

        time.sleep(1.1)


@pytest.fixture
def proj_from_list(make_temp_repos):
    return ProjectDirectory(working_dir=[REPO1_DIR, REPO2_DIR], verbose=True)


@pytest.fixture
def proj_from_os_walk(make_temp_repos):
    return ProjectDirectory(working_dir=PROJECT_DIR, verbose=True)


@pytest.fixture
def repo1(make_temp_repos):
    return Repository(working_dir=REPO1_DIR, verbose=True)


@pytest.fixture
def repo2(make_temp_repos):
    return Repository(working_dir=REPO2_DIR, verbose=True)
