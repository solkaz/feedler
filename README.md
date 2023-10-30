# feedler

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](./CODE_OF_CONDUCT.md)

Experimental application to manage RSS feeds.

## Roadmap

- [ ] Ability to filter an RSS feed from a URL with a single constraint
- [ ] Ability to filter an RSS feed from a URL with multiple constraints
- [ ] Ability to combine RSS feeds from a URL or from a filtered feed created with Feedler
- [ ] Frontend to interact with server

## Development

You will need [`pipenv`](https://pipenv.pypa.io/en/latest/) to manage dependencies and virtual environments. Run `pipenv install` to install dependencies.

To start the server for local development, run `uvicorn feedler.main:app` in the project's root directory after having enabled the virtual environment.

## License

[GNU General Public License v3.0](./LICENSE)
