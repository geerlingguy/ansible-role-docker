import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_is_docker_installed(host):
    package_docker = host.package('docker-ce')

    assert package_docker.is_installed


def test_is_docker_servive_enabled(host):
    assert host.service("docker").is_running is True
    assert host.service("docker").is_enabled is True


def test_pull_hello_world_image(host):
    pull = host.run("sudo docker pull hello-world")
    assert 'Status: Downloaded newer image for hello-world:latest' in pull.stdout


def test_run_hello_world_container_successfully(host):
    hello_world_ran = host.run(
        "sudo docker run hello-world")
    assert hello_world_ran.stderr is ''
    assert 'Hello from Docker!' in hello_world_ran.stdout
