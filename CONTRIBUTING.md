# Contributing to wagtail-drawio

Thanks for taking the time to contribute. This is a small project maintained on a best-effort basis, so please be patient — someone will look at your PR eventually.

## Getting started

Clone the repo and create the environment in one step:

```shell
git clone https://github.com/goutnet/wagtail-drawio.git
cd wagtail-drawio
make env
```

This creates a `env/` virtualenv and installs all runtime and dev dependencies.

## Running the tests

```shell
make test
```

This runs the full test suite with coverage. All tests must pass before submitting a PR. The CI runs on Python 3.10, 3.11, and 3.12.

To get a browsable HTML coverage report after running the tests:

```shell
make coverage
```

## Code style

This project uses [Black](https://black.readthedocs.io/) for formatting. Run it before committing:

```shell
make lint
```

No style debates, no exceptions — Black decides.

## Trying it out

A minimal Wagtail project is included under `webroot/` for manual testing:

```shell
make freshdb   # creates the database and an admin/admin superuser
make webtest   # starts the dev server on localhost:8000
```

Then visit `http://localhost:8000/admin/`.

## Submitting a PR

- Keep the scope focused — one feature or fix per PR.
- If you're adding something non-trivial, add a test for it.
- Write a clear PR description explaining *what* and *why*.
- Be kind. Everyone here is a volunteer.

Someone will review it. It may take a little while, but it won't be ignored.
