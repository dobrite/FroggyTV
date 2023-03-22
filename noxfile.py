import nox


@nox.session
def tests(session):
    session.install('pytest')
    session.run('pytest')


@nox.session
def lint(session):
    session.install('flake8', 'flake8-import-order')
    session.run('flake8', 'src', '--import-order-style', 'google')
