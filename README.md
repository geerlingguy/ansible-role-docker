# Ansible Role: Docker

[![CI](https://github.com/geerlingguy/ansible-role-docker/workflows/CI/badge.svg?event=push)](https://github.com/geerlingguy/ansible-role-docker/actions?query=workflow%3ACI)

An Ansible Role that installs [Docker](https://www.docker.com) on Linux.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    # Edition can be one of: 'ce' (Community Edition) or 'ee' (Enterprise Edition).
    docker_edition: 'ce'
    docker_packages:
        - "docker-{{ docker_edition }}"
        - "docker-{{ docker_edition }}-cli"
        - "docker-{{ docker_edition }}-rootless-extras"
    docker_packages_state: present

The `docker_edition` should be either `ce` (Community Edition) or `ee` (Enterprise Edition). 
You can also specify a specific version of Docker to install using the distribution-specific format: 
Red Hat/CentOS: `docker-{{ docker_edition }}-<VERSION>` (Note: you have to add this to all packages);
Debian/Ubuntu: `docker-{{ docker_edition }}=<VERSION>` (Note: you have to add this to all packages).

You can control whether the package is installed, uninstalled, or at the latest version by setting `docker_package_state` to `present`, `absent`, or `latest`, respectively. Note that the Docker daemon will be automatically restarted if the Docker package is updated. This is a side effect of flushing all handlers (running any of the handlers that have been notified by this and any other role up to this point in the play).

    docker_service_manage: true
    docker_service_state: started
    docker_service_enabled: true
    docker_restart_handler_state: restarted

Variables to control the state of the `docker` service, and whether it should start on boot. If you're installing Docker inside a Docker container without systemd or sysvinit, you should set `docker_service_manage` to `false`.

    docker_install_compose_plugin: false
    docker_compose_package: docker-compose-plugin
    docker_compose_package_state: present

Docker Compose Plugin installation options. These differ from the below in that docker-compose is installed as a docker plugin (and used with `docker compose`) instead of a standalone binary.

    docker_install_compose: true
    docker_compose_version: "1.26.0"
    docker_compose_arch: "{{ ansible_architecture }}"
    docker_compose_path: /usr/local/bin/docker-compose

Docker Compose installation options.

    docker_repo_url: https://download.docker.com/linux

The main Docker repo URL, common between Debian and RHEL systems.

    docker_apt_release_channel: stable
    docker_apt_arch: "{{ 'arm64' if ansible_architecture == 'aarch64' else 'amd64' }}"
    docker_apt_repository: "deb [arch={{ docker_apt_arch }}] {{ docker_repo_url }}/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} {{ docker_apt_release_channel }}"
    docker_apt_ignore_key_error: True
    docker_apt_gpg_key: "{{ docker_repo_url }}/{{ ansible_distribution | lower }}/gpg"

(Used only for Debian/Ubuntu.) You can switch the channel to `nightly` if you want to use the Nightly release.

You can change `docker_apt_gpg_key` to a different url if you are behind a firewall or provide a trustworthy mirror.
Usually in combination with changing `docker_apt_repository` as well.

    docker_yum_repo_url: "{{ docker_repo_url }}/{{ (ansible_distribution == 'Fedora') | ternary('fedora','centos') }}/docker-{{ docker_edition }}.repo"docker_edition }}.repo
    docker_yum_repo_enable_nightly: '0'
    docker_yum_repo_enable_test: '0'
    docker_yum_gpg_key: "{{ docker_repo_url }}/centos/gpg"

(Used only for RedHat/CentOS.) You can enable the Nightly or Test repo by setting the respective vars to `1`.

You can change `docker_yum_gpg_key` to a different url if you are behind a firewall or provide a trustworthy mirror.
Usually in combination with changing `docker_yum_repository` as well.

    docker_users:
      - user1
      - user2

A list of system users to be added to the `docker` group (so they can use Docker on the server).

    docker_daemon_options:
      storage-driver: "devicemapper"
      log-opts:
        max-size: "100m"

Custom `dockerd` options can be configured through this dictionary representing the json file `/etc/docker/daemon.json`.

## Use with Ansible (and `docker` Python library)

Many users of this role wish to also use Ansible to then _build_ Docker images and manage Docker containers on the server where Docker is installed. In this case, you can easily add in the `docker` Python library using the `geerlingguy.pip` role:

```yaml
- hosts: all

  vars:
    pip_install_packages:
      - name: docker

  roles:
    - geerlingguy.pip
    - geerlingguy.docker
```

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  roles:
    - geerlingguy.docker
```

## License

MIT / BSD

## Sponsors

* [We Manage](https://we-manage.de): Helping start-ups and grown-ups scaling their infrastructure in a sustainable way.

The above sponsor(s) are supporting Jeff Geerling on [GitHub Sponsors](https://github.com/sponsors/geerlingguy). You can sponsor Jeff's work too, to help him continue improving these Ansible open source projects!

## Author Information

This role was created in 2017 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).
