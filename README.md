# sorelferris.github.io

Personal site for **Sorel Ferris**. Built with [Jekyll](https://jekyllrb.com/)
+ [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes), deployed
on GitHub Pages.

## Local development

```bash
# Install Ruby + bundler (system-specific)
gem install bundler jekyll
bundle install
bundle exec jekyll serve --livereload
# → http://localhost:4000
```

## Structure

- `index.md` — landing page
- `roadmap.md` — 3-year career arc, updated monthly from `research/roadmap/`
- `reading.md` — paper reading queue, updated weekly from `research/papers/`
- `now.md` — operational focus (this week / this month), updated ~monthly
- `_config.yml` — Minimal Mistakes configuration
- `_includes/social-links.html` — sidebar social links

## Update cadence

- **On push:** GitHub Pages auto-builds within ~60s
- **Weekly cron** (planned): pull latest from `sorelferris/research`,
  regenerate reading page
- **Manual:** edit the `.md` files directly, push to main

## Theme override notes

This uses `minimal-mistakes-jekyll` as a remote theme (no vendored theme).
To customize deeply, fork Minimal Mistakes into a local theme and switch
the `theme:` field in `_config.yml`.
