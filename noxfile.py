import nox


@nox.session
def tests(session):
    session.install("pytest")
    session.run("pytest")


@nox.session
def format(session):
    session.install("black")
    session.run("black", ".")


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", ".")


@nox.session
def check(session):
    session.install("pyright")
    session.run("pyright")
