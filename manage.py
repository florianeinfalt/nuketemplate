import os
import sys
import click
import twine
import subprocess


project_root = os.path.dirname(os.path.abspath(__file__))
NUKE_LOCATION = '/Applications/Nuke10.0v5/Nuke10.0v5.app/Contents/MacOS'


def run_tests():
    os.chdir(project_root)
    test_env = os.environ.copy()
    env = {
        'PYTHONDONTWRITEBYTECODE': '1',
        'COVERAGE_FILE': '{0}/.coverage'.format(project_root),
        'NUKE_INTERACTIVE': '1',
        'PATH': '{0}:{1}'.format(NUKE_LOCATION, test_env['PATH']),
        'PYTHONPATH':'/Users/florian/bin/build/lib/python2.7/site-packages:'
                     '/Users/florian/_/_development/git/projects/nukecontexts:'
                     '/Users/florian/_/_development/git/projects/nukeuuid:{0}'.format(project_root)
    }
    for env_var, env_val in env.iteritems():
        test_env[env_var] = env_val
    subprocess.Popen(['python', project_root+'/run_tests.py'],
                     env=test_env).wait()


def run_docs():
    os.chdir(project_root + '/docs')
    docs_env = os.environ.copy()
    env = {
        'PYTHONDONTWRITEBYTECODE': '1',
        'NON_PRODUCTION_CONTEXT': '1',
        'PYTHONPATH':'/Users/florian/bin/build/lib/python2.7/site-packages:'
                     '/Users/florian/_/_development/git/projects/nukecontexts:'
                     '/Users/florian/_/_development/git/projects/nukeuuid:{0}'.format(project_root)
    }
    for env_var, env_val in env.iteritems():
        docs_env[env_var] = env_val
    subprocess.Popen(['make', 'html'], env=docs_env).wait()


def run_deploy():
    os.chdir(project_root)
    subprocess.Popen(['python', 'setup.py', 'sdist', 'bdist_wheel']).wait()
    subprocess.Popen(['twine', 'upload', 'dist/*']).wait()


@click.command()
@click.option('--tests', is_flag=True)
@click.option('--docs', is_flag=True)
@click.option('--deploy', is_flag=True)
def cli(tests, docs, deploy):
    if tests:
        run_tests()
    if docs:
        run_docs()
    if deploy:
        run_tests()
        run_docs()
        run_deploy()


if __name__ == '__main__':
    cli()
