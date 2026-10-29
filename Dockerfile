FROM ruby:3.1

WORKDIR /site

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY Gemfile ./

RUN bundle install

# Fixes <video> playback under jekyll serve; the file comes from the /site mount at runtime
ENV RUBYOPT=-r/site/docker/webrick_range_fix.rb

EXPOSE 4000 35729

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--future", "--livereload"]
