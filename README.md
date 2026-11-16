# Ansible Role: Docker

[![CI](https://github.com/geerlingguy/ansible-role-docker/actions/workflows/ci.yml/badge.svg)](https://github.com/geerlingguy/ansible-role-docker/actions/workflows/ci.yml)

An Ansible Role that installs [Docker](https://www.docker.com) on Linux.

## Requirements

The `community.general` collection is required when using rootless Docker support.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# Edition can be one of: 'ce' (Community Edition) or 'ee' (Enterprise Edition).
docker_edition: 'ce'
docker_packages:
  - "docker-{{ docker_edition }}"
  - "docker-{{ docker_edition }}-cli"
  - "docker-{{ docker_edition }}-rootless-extras"
  - "containerd.io"
  - docker-buildx-plugin
docker_packages_state: present
```

The `docker_edition` should be either `ce` (Community Edition) or `ee` (Enterprise Edition). 
You can also specify a specific version of Docker to install using the distribution-specific format: 
Red Hat/CentOS: `docker-{{ docker_edition }}-<VERSION>` (Note: you have to add this to all packages);
Debian/Ubuntu: `docker-{{ docker_edition }}=<VERSION>` (Note: you have to add this to all packages).

You can control whether the package is installed, uninstalled, or at the latest version by setting `docker_packages_state` to `present`, `absent`, or `latest`, respectively. Note that the Docker daemon will be automatically restarted if the Docker package is updated. This is a side effect of flushing all handlers (running any of the handlers that have been notified by this and any other role up to this point in the play).

```yaml
docker_obsolete_packages:
  - docker
  - docker.io
  - docker-engine
  - docker-doc
  - docker-compose
  - docker-compose-v2
  - podman-docker
  - containerd
  - runc
```

`docker_obsolete_packages` for different os-family:

- [`RedHat.yaml`](./vars/RedHat.yml)
- [`Debian.yaml`](./vars/Debian.yml)
- [`Suse.yaml`](./vars/Suse.yml)

A list of packages to be uninstalled prior to running this role. See [Docker's installation instructions](https://docs.docker.com/engine/install/debian/#uninstall-old-versions) for an up-to-date list of old packages that should be removed.

```yaml
docker_service_manage: true
docker_service_state: started
docker_service_enabled: true
docker_service_start_command: ""
docker_restart_handler_state: restarted
```

Variables to control the state of the `docker` service, and whether it should start on boot. If you're installing Docker inside a Docker container without systemd or sysvinit, you should set `docker_service_manage` to `false`.

```yaml
docker_install_compose_plugin: true
docker_compose_package: docker-compose-plugin
docker_compose_package_state: present
```

Docker Compose Plugin installation options. These differ from the below in that docker-compose is installed as a docker plugin (and used with `docker compose`) instead of a standalone binary.

```yaml
docker_install_compose: false
docker_compose_version: "v2.32.1"
docker_compose_arch: "{{ ansible_facts.architecture }}"
docker_compose_url: "https://github.com/docker/compose/releases/download/{{ docker_compose_version }}/docker-compose-linux-{{ docker_compose_arch }}"
docker_compose_path: /usr/local/bin/docker-compose
```

Docker Compose installation options.

```yaml
docker_add_repo: true
```

Controls whether this role will add the official Docker repository. Set to `false` if you want to use the default docker packages for your system or manage the package repository on your own.

```yaml
docker_repo_url: https://download.docker.com/linux
```

The main Docker repo URL, common between Debian and RHEL systems.

```yaml
docker_apt_release_channel: stable
docker_apt_ansible_distribution: "{{ 'ubuntu' if ansible_facts.distribution in ['Pop!_OS', 'Linux Mint'] else ansible_facts.distribution }}"
docker_apt_repo_url: "{{ docker_repo_url }}/{{ docker_apt_ansible_distribution | lower }}"
docker_apt_gpg_key: "{{ docker_repo_url }}/{{ docker_apt_ansible_distribution | lower }}/gpg"
docker_apt_filename: "docker"
```

(Used only for Debian/Ubuntu.) You can switch the channel to `nightly` if you want to use the Nightly release.

`docker_apt_ansible_distribution` is a workaround for Ubuntu variants which can't be identified as such by Ansible, and is only necessary until Docker officially supports them.

You can change `docker_apt_repo_url` if you need to point Debian or Ubuntu systems at an internal mirror or cache.
You can change `docker_apt_gpg_key` to a different url if you are behind a firewall or provide a trustworthy mirror.
`docker_apt_filename` controls the name of the source list file created in `sources.list.d`. If you are upgrading from an older (<7.0.0) version of this role, you should change this to the name of the existing file (e.g. `download_docker_com_linux_debian` on Debian) to avoid conflicting lists.

```yaml
docker_yum_repo_url: "{{ docker_repo_url }}/{{ 'fedora' if ansible_facts.distribution == 'Fedora' else 'rhel' if ansible_facts.distribution == 'RedHat' else 'centos' }}/docker-{{ docker_edition }}.repo"
docker_yum_repo_enable_test: '0'
docker_yum_gpg_key: "{{ docker_repo_url }}/{{ 'fedora' if ansible_facts.distribution == 'Fedora' else 'rhel' if ansible_facts.distribution == 'RedHat' else 'centos' }}/gpg"
```

(Used only for RedHat/CentOS.) You can enable the Test repo by setting the respective vars to `1`.

You can change `docker_yum_gpg_key` to a different url if you are behind a firewall or provide a trustworthy mirror.
Usually in combination with changing `docker_yum_repository` as well.

```yaml
docker_users: []
```

A list of system users to be added to the `docker` group (so they can use Docker on the server). Example:

```yaml
docker_users:
  - user1
  - user2
```

```yaml
docker_daemon_options: {}
```

Custom `dockerd` options can be configured through this dictionary representing the json file `/etc/docker/daemon.json` (or `~/.config/docker/daemon.json` when running in rootless mode). Example:

```yaml
docker_daemon_options:
  storage-driver: "overlay2"
  log-opts:
    max-size: "100m"
```

### Rootless Docker Mode

Rootless Docker allows running the Docker daemon and containers as a non-root user to mitigate potential container breakout vulnerabilities. This role provides native, opt-in support for rootless mode.

```yaml
docker_rootless: false
docker_rootless_user: ""
docker_rootless_subid_start: ""
docker_rootless_subid_count: 65536
docker_rootless_network_driver: ""
docker_rootless_environment: {}
docker_rootless_expose_privileged_ports: false
```

- **`docker_rootless`**: Controls whether to configure Docker in rootless mode. Default is `false` (existing rootful behavior). When `true`:
  - The system-level `docker.service` and `docker.socket` are masked, stopped, and disabled.
  - The Docker daemon runs as a user systemd service (`systemctl --user`) under `docker_rootless_user`.
  - Systemd linger is enabled via `loginctl enable-linger` to keep the user daemon running without an active user session.
- **`docker_rootless_user`**: The unprivileged system user account under which rootless Docker runs. Required when `docker_rootless: true`. Rootless Docker cannot run as `root` (UID 0). If the account does not exist on the target host, the role automatically creates it. If the account already exists, the role discovers its home directory, UID, and GID from the system passwd database, and reconciles that home directory's ownership (`<user>:<primary gid>`) and mode (`0750`).
- **`docker_rootless_subid_start`**: Optional starting ID for subordinate UID and GID allocations in `/etc/subuid` and `/etc/subgid`. If omitted, the role dynamically calculates a safe, collision-free offset from current host allocations (starting from `100000`). Existing allocations with count > 0 are preserved.
- **`docker_rootless_subid_count`**: Number of subordinate UIDs and GIDs allocated in `/etc/subuid` and `/etc/subgid` when creating a new allocation (default: `65536`). Existing allocations with count > 0 are preserved.
- **`docker_rootless_network_driver`**: RootlessKit network driver to select (`""`, `"slirp4netns"`, `"pasta"`, or `"gvisor-tap-vsock"`). When empty (`""`, default), the role does not set `DOCKERD_ROOTLESS_ROOTLESSKIT_NET` itself, allowing Moby to use its automatic network driver selection. When an explicit driver is configured, the role sets `DOCKERD_ROOTLESS_ROOTLESSKIT_NET=<driver>` in the systemd service unit and installs the driver's required packages (e.g. `slirp4netns` or `passt`).
- **`docker_rootless_environment`**: Key-value dictionary of environment variables passed to the rootless systemd service unit. For example:
  ```yaml
  docker_rootless_environment:
    HTTP_PROXY: "http://proxy.example.com:8080"
    NO_PROXY: "localhost,127.0.0.1"
  ```
- **`docker_rootless_expose_privileged_ports`**: When `true`, applies `cap_net_bind_service=ep` capability to the `rootlesskit` executable to allow publishing privileged ports (< 1024) without globally modifying sysctl `net.ipv4.ip_unprivileged_port_start`. Reconciled and removed when set to `false`. Capability tooling (`libcap2-bin`, `libcap`, or `libcap-progs`) is installed only when this feature is enabled.

#### Supported Platforms for Rootless Mode

Rootless Docker requires `systemd` user sessions (`systemctl --user`, `loginctl enable-linger`) and Docker's rootless extras package.
- **Supported OS Families**: `Debian` family (Debian, Ubuntu), `RedHat` family (RHEL, CentOS Stream, Fedora, Rocky Linux, AlmaLinux), and `Suse` family (openSUSE, SLES). Automated CI exercises rootless mode against `ubuntu2404`, `fedora43`, and `opensuseleap15`.
- **Unsupported**: Alpine Linux (uses OpenRC instead of systemd) and Arch Linux (rootless extras are not packaged in official pacman repositories). On these distributions, enabling `docker_rootless: true` fails fast with an explicit error, while standard rootful mode (`docker_rootless: false`) remains fully supported.

#### Prerequisites & Feature-Dependent Packaging

Prerequisites are kept strictly minimal:
- **Core packages**: Only the minimal package providing `newuidmap` and `newgidmap` (`uidmap` on Debian/Ubuntu, `shadow-utils` on RedHat, `shadow` on SUSE) is installed unconditionally for rootless mode.
- **Networking packages**: By default (`docker_rootless_network_driver: ""`), RootlessKit uses Moby's automatic driver selection (which defaults to built-in `gvisor-tap-vsock` requiring no external packages). When an explicit network driver is set, its prerequisite package (`slirp4netns` or `passt` for `pasta`) is installed automatically.
- **Capability packages**: Capability tooling packages (`libcap2-bin` / `libcap` / `libcap-progs`) are only installed when `docker_rootless_expose_privileged_ports: true`.

#### Service Lifecycle & Handlers

In rootless mode:
- The daemon service is controlled via the existing `docker_service_manage`, `docker_service_state`, and `docker_service_enabled` variables, targeting the user-level systemd service `~/.config/systemd/user/docker.service`.
- The `restart docker` handler automatically directs restarts to the user systemd service when `docker_rootless: true` and to the system daemon when `docker_rootless: false`.

#### Daemon Configuration

When `docker_rootless: true`, daemon options configured via `docker_daemon_options` are rendered into the user's configuration file at `~/.config/docker/daemon.json` (owned by `docker_rootless_user`) rather than the rootful `/etc/docker/daemon.json`.

#### Socket Contract and Usage

In rootless mode, the daemon listens on a per-user UNIX domain socket:
```
unix:///run/user/<uid>/docker.sock
```
The role exposes the following fact for subsequent tasks, playbooks, or tools:
- `docker_rootless_socket`: `unix:///run/user/<uid>/docker.sock`

To interact with the rootless daemon from the CLI:
```bash
export DOCKER_HOST="unix:///run/user/$(id -u)/docker.sock"
docker info
```
Or specify the host flag:
```bash
docker -H unix:///run/user/<uid>/docker.sock info
```

### cAdvisor Support

[cAdvisor](https://github.com/google/cadvisor) (Container Advisor) provides container users an understanding of the resource usage and performance characteristics of their running containers. This role optionally installs cAdvisor as a native, root-owned `systemd` system service from official upstream static release binaries with checksum verification.

cAdvisor is compatible with both standard rootful Docker and rootless Docker deployments.

```yaml
# cAdvisor options service options.
docker_install_cadvisor: false
docker_cadvisor_service_manage: true
docker_cadvisor_state: started
docker_cadvisor_service_enabled: true
docker_cadvisor_restart_handler_state: restarted
docker_cadvisor_listen_ip: "127.0.0.1"
docker_cadvisor_port: 8080
docker_cadvisor_extra_args: []

# cAdvisor Package Options
docker_cadvisor_version: "latest"
docker_cadvisor_arch: "{{ 'amd64' if ansible_facts.architecture in ['x86_64', 'amd64'] else 'arm64' if ansible_facts.architecture in ['aarch64', 'arm64'] else ansible_facts.architecture }}"
```

- **`docker_install_cadvisor`**: Enables installation and service management for cAdvisor. Default is `false`.
- **`docker_cadvisor_service_manage`**: Whether to manage the cAdvisor systemd service. Default is `true`.
- **`docker_cadvisor_state`**: Desired state of the systemd service (`started`, `stopped`). Default is `started`.
- **`docker_cadvisor_service_enabled`**: Whether cAdvisor should be enabled at boot (default: `true`).
- **`docker_cadvisor_restart_handler_state`**: State for the cAdvisor restart handler (`restarted`).
- **`docker_cadvisor_listen_ip`**: IP address to bind the web server and Prometheus metrics endpoint. Default is `127.0.0.1`.
- **`docker_cadvisor_port`**: Port on which cAdvisor listens (default: `8080`).
- **`docker_cadvisor_extra_args`**: List of additional command-line flags passed directly to the cAdvisor executable (e.g. `["-docker_only=true"]`).
- **`docker_cadvisor_version`**: Upstream cAdvisor release tag (e.g. `v0.60.5`) or `latest` (default: `latest`).
- **`docker_cadvisor_arch`**: Architecture identifier for binary downloads (`amd64` or `arm64`).


#### Service Lifecycle & Handlers

cAdvisor is managed as a native root-owned system systemd service (`/etc/systemd/system/cadvisor.service`), regardless of whether Docker is running in rootful or rootless mode.

- The `restart cadvisor` handler independently handles cAdvisor restarts when its binary or unit template is updated, without restarting or interrupting the Docker daemon.
- cAdvisor is ordered after the respective Docker service (`docker.service` in rootful mode, or `user@<uid>.service` in rootless mode) and enforces an `ExecStartPre` Docker API readiness probe (`docker info`) against the effective socket. This prevents cAdvisor from permanently missing container runtime registration if it starts before dockerd is ready. In rootless mode, it connects to the unprivileged user's Docker and containerd sockets while leaving system Docker masked and inactive.

#### Exposed Metrics Contract

Upon completion of the cAdvisor tasks, the role exposes the following facts:
- `docker_cadvisor_effective_listen_ip`: Effective IP address (e.g. `127.0.0.1`).
- `docker_cadvisor_effective_port`: Effective port (e.g. `8080`).
- `docker_cadvisor_effective_metrics_path`: Metrics path (e.g. `/metrics`).
- `docker_cadvisor_effective_metrics_url`: Full metrics URL (e.g. `http://127.0.0.1:8080/metrics`).
- `docker_cadvisor_effective_docker_endpoint`: Effective Docker socket URL.

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
