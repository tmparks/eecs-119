FROM ubuntu:rolling

# Install development tools
RUN apt-get update && apt-get install --yes \
        git \
        python3 \
        rust-all \
    && rm --recursive --force /var/lib/apt/lists/*

# Unprivileged user
USER ubuntu
WORKDIR /home/ubuntu
