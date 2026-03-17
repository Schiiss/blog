# Blog

Personal tech blog built with Jekyll and the [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) theme, hosted on GitHub Pages.

## Local Development

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)

### Running locally

```bash
docker compose up
```

The first run will take a few minutes to build the image and install gems. Subsequent runs are fast thanks to the cached bundle volume.

Once running, open **http://localhost:4000/blog/**

The server watches for file changes and reloads automatically. `_config.yml` changes require a restart:

```bash
docker compose down
docker compose up
```

### Rebuilding after Gemfile changes

```bash
docker compose down -v
docker compose build --no-cache
docker compose up
```

## Deployment

Pushing to `master` triggers a GitHub Actions workflow that builds and deploys to GitHub Pages automatically.
