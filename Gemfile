source "https://rubygems.org"

# Minimal Mistakes theme is provided via remote_theme in _config.yml
# (GitHub Pages does not bundle minimal-mistakes-jekyll gem in github-pages 232)

# Jekyll plugins
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-seo-tag", "~> 2.6"
  gem "jekyll-sitemap", "~> 1.4"
end

# Windows and JRuby do not include zoneinfo files
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :install_if => false
