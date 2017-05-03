# Ansible Role: Docker

[![Build Status](https://travis-ci.org/geerlingguy/ansible-role-docker.svg?branch=master)](https://travis-ci.org/geerlingguy/ansible-role-docker)

An Ansible Role that installs [Docker](https://www.docker.com) on Linux.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    docker_package: "docker-engine"

The Docker package to install.

    docker_install_compose: true
    docker_compose_version: "1.11.2"
    docker_compose_path: /usr/local/bin/docker-compose

Docker Compose installation options.

    docker_apt_repository: "deb https://apt.dockerproject.org/repo {{ ansible_distribution|lower }}-{{ ansible_distribution_release }} main"

(Used only for Debian/Ubuntu.) Add 'testing' if you don't want stable.

    docker_yum_repo_version: 'main' # 'testing', 'beta', 'nightly'

(Used only for RedHat/CentOS.)

## Dependencies

None.

## Example Playbook

    - hosts: all
      roles:
        - geerlingguy.docker

## License

MIT / BSD

## Author Information

This role was created in 2017 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).
