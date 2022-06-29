from unittest.mock import patch
from gitpandas import Repository


def test_clone_repo(monkeypatch):
    with patch("gitpandas.repository.Repo.clone_from"):

        repo = Repository(working_dir='https://github.com/wdm0006/git-pandas.git', verbose=True)
        assert repo.repo_name == "git-pandas"

        repo = Repository(working_dir='git://github.com/wdm0006/git-pandas.git', verbose=True)
        assert repo.repo_name == "git-pandas"


def test_repo_name(repo1):
    assert repo1.repo_name == "repository1"


def test_branches(repo1):
    branches = repo1.branches()['branch'].values
    assert 'master' in branches


def test_tags(repo1):
    tags = repo1.tags()
    assert len(tags) == 0


def test_is_bare(repo1):
    assert not repo1.is_bare()


def test_commit_history(repo1):
    ch = repo1.commit_history(branch='master')
    assert ch.shape[0] == 6

    ch2 = repo1.commit_history(branch='master', ignore_globs=['*.[!p][!y]'])
    assert ch2.shape[0] == 5

    ch3 = repo1.commit_history(branch='master', limit=3)
    assert ch3.shape[0] == 3

    ch4 = repo1.commit_history(branch='master', days=5)
    assert ch4.shape[0] == 6

    fch = repo1.file_change_history(branch='master')
    assert fch.shape[0] == 6

    fch2 = repo1.file_change_history(branch='master', ignore_globs=['*.[!p][!y]'])
    assert fch2.shape[0] == 5

    fch3 = repo1.file_change_history(branch='master', limit=3)
    assert fch3.shape[0] == 3

    fcr = repo1.file_change_rates(branch='master')
    assert fcr.shape[0] == 6
    assert fcr['unique_committers'].sum() == 6
    assert fcr['net_change'].sum() == 11

    # we know this repo doesnt have coverage
    assert not repo1.has_coverage()

    # we know this repo only has one committer
    assert repo1.bus_factor(by='repository')['bus factor'].values[0] == 1

    # lets do some blaming

    blame = repo1.blame(ignore_globs=['*.[!p][!y]'])
    assert blame['loc'].sum() == 10
    assert blame.shape[0] == 1

    cblame = repo1.cumulative_blame()
    assert cblame.shape[0] == 8
    assert cblame[cblame.columns[-1]].sum() == 40

    revs = repo1.revs(num_datapoints=2)
    assert revs.shape[0] == 2
    revs = repo1.revs(limit=2)
    assert revs.shape[0] == 2
    revs = repo1.revs()
    assert revs.shape[0] == 6
