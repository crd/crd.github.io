# corydonnelly.com

Personal site + blog built with Jekyll using the Minimal Mistakes theme (remote theme starter).

- Repo: https://github.com/crd/crd.github.io
- Prod URL: https://corydonnelly.com
- Credits: Theme by Michael Rose (mmistakes/minimal-mistakes). Site started from the Minimal Mistakes remote theme starter.

## Configuration (quick)

- `_config.yml` controls site metadata, theme options, nav defaults, etc.
- Minimal Mistakes config guide: https://mmistakes.github.io/minimal-mistakes/docs/configuration/
- Custom domain is set via CNAME (repo root). Enforce HTTPS in Pages settings.
- GitHub Pages + Jekyll basics: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll

## Prereqs

- Ruby (via rbenv or system) + Bundler.
- Clone the repo and install gems:

bundle install

## Local develop

bundle exec jekyll serve --livereload
# open http://127.0.0.1:4000

(Note) If you edit `_config.yml`, restart `jekyll serve`.

## Build & deploy

This repo is built and served by GitHub Pages. Push to the default branch to publish.

- GitHub Pages overview: https://pages.github.com/
- About GitHub Pages + Jekyll: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll
- Enforce HTTPS: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https

## Dependencies (keeping current)

# update locked gems (respecting Gemfile constraints)
bundle update
# then test locally
bundle exec jekyll serve

Minimal Mistakes install/upgrade docs:
https://mmistakes.github.io/minimal-mistakes/docs/installation/

## Resume (single source + print-ready)

- Web page lives at: /_pages/resume.md
- Normalize newly extracted Markdown and ensure front matter:

# Normalize the current page in-place
./scripts/normalize-resume.sh

## Writing new articles

- Minimal Mistakes “Working with Posts”:
  https://mmistakes.github.io/minimal-mistakes/docs/posts/
- Jekyll posts basics:
  https://jekyllrb.com/docs/posts/
- Typical new post:

# create: _posts/2025-09-23-my-title.md
cat > _posts/2025-09-23-my-title.md <<'MD'
---
title: "My Title"
layout: single
author_profile: true
read_time: true
comments: false
---
Hello world.
MD

## Things to know

- /_data/navigation.yml controls the top nav (e.g., link to /resume/).
- /_includes/head/custom.html can load custom CSS (e.g., assets/css/print-resume.css).
- Restart `jekyll serve` after `_config.yml` changes (Jekyll doesn’t reload it live).
- Minimal Mistakes quick-start:
  https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/
