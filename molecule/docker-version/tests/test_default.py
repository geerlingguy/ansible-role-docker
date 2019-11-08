import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


@pytest.mark.parametrize('pkg', [
    'docker-ce',
    'docker-ce-cli',
    'containerd.io'
])
def test_packages_are_installed(host, pkg):
    package = host.package(pkg)
    assert package.is_installed


def test_srv(host):
    service = host.service("docker")

    assert service.is_running
    assert service.is_enabled


def test_docker_version(host):
    docker_version = os.environ.get("DOCKER_VERSION_CI")
    if not docker_version:
        docker_version = "18.09.2"

    # docker_cli = host.check_output('docker -v')
    # assert docker_cli.find(docker_version) != -1

    docker_daemon = host.check_output('docker info|grep Version')
    assert docker_daemon.find(docker_version) != -1


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
