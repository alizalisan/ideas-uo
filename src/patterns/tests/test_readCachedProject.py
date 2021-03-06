from gitutils.tests.testutils import *
from gitutils.utils import *
os.environ['PYTEST_RUNNING'] = 'true'

from patterns.fetcher import Fetcher
from os.path import abspath, dirname
cache_dir = abspath(dirname(__file__))

#from pathlib import Path
#cache_dir = os.path.dirname(Path(__file__))


def test_readCachedProject(capsys, caplog):
    fetcher = Fetcher(project_name='testrepo')
    fetcher.update_cache_info(cache_dir=cache_dir,cache_file='.testrepo.pickle')
    print(fetcher.cache)
    try:
        success = fetcher.fetch()
    except Exception as e:
        success = err("Could not load ideas-uo cached project: %s" % str(e))
    assert success is True