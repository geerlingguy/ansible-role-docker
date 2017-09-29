# Ansible Role: Docker

[![Build Status](https://travis-ci.org/geerlingguy/ansible-role-docker.svg?branch=master)](https://travis-ci.org/geerlingguy/ansible-role-docker)

An Ansible Role that installs [Docker](https://www.docker.com) on Linux.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    # Edition can be one of: 'ce' (Community Edition) or 'ee' (Enterprise Edition).
    docker_edition: 'ce'
    docker_package: "docker-{{ docker_edition }}"
    docker_package_state: present

The `docker_edition` should be either `ce` (Community Edition) or `ee` (Enterprise Edition). You can also specify a specific version of Docker to install using a format like `docker-{{ docker_edition }}-<VERSION>`. And you can control whether the package is installed, uninstalled, or at the latest version by setting `docker_package_state` to `present`, `absent`, or `latest`, respectively.

    docker_install_compose: true
    docker_compose_version: "1.15.0"
    docker_compose_path: /usr/local/bin/docker-compose

Docker Compose installation options.

    docker_apt_release_channel: stable
    docker_apt_repository: "deb https://download.docker.com/linux/{{ ansible_distribution|lower }} {{ ansible_distribution_release }} {{ docker_apt_release_channel }}"

(Used only for Debian/Ubuntu.) You can switch the channel to `edge` if you want to use the Edge release.

    docker_yum_repo_url: https://download.docker.com/linux/centos/docker-{{ docker_edition }}.repo
    docker_yum_repo_enable_edge: 0
    docker_yum_repo_enable_test: 0

(Used only for RedHat/CentOS.) You can enable the Edge or Test repo by setting the respective vars to `1`.

### devicemapper

Out of the box this role deploys docker with the overlay driver, but the only
officially supported configuration of Docker on RedHat/CentOS is to use device
mapper as the storage driver (Not to be confused with `docker volume`). Docker
can configure the lvm thin provisioning when provided a raw block device (such
as a second disk). To deploy this configuration, set the following variables in
your deploy:

    docker_devicemapper_raw_device: /dev/sdb # Or /dev/vdb or ...
    docker_configure_daemon: true

For more information, see the [device mapper driver][devicemapper] documentation.

### Docker daemon configuration

To configure devicemapper as the storage driver, this role has to configure the
docker daemon via `daemon.json`, but you can also use this to configure the
daemon as you wish by overriding `docker_daemon_config`. This yaml hash is then
converted to json. Making changes to `daemon.json` then require a restart of the
service, but this role does not default to restarting the service. To trigger a
restart when reconfiguring the daemon, set `docker_restart` to `true`.

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

## Author Information

This role was created in 2017 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).

[devicemapper]: https://docs.docker.com/engine/userguide/storagedriver/device-mapper-driver/
