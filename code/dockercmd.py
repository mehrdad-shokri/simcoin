import config
import bitcoindcmd
import tccmd


def run_node(node, cmd):
    return ('docker run'
            ' --cap-add=NET_ADMIN'  # for `tc`
            ' --detach=true'
            ' --net=isolated_network'
            ' --ip=' + str(node.ip) +
            ' --name=' + config.prefix + node.name +  # container name
            ' --hostname=' + config.prefix + node.name +
            ' --volume $PWD/' + config.host_dir(node) + ':' + bitcoindcmd.guest_dir +
            ' ' + config.node_image +  # image name # src: https://hub.docker.com/r/abrkn/bitcoind/
            ' bash -c "' + cmd + '" ')


def run_selfish_proxy(node, cmd):
        return (
                'docker run'
                ' --cap-add=NET_ADMIN'  # for `tc`
                ' --detach=true'
                ' --net=isolated_network'
                ' --ip=' + str(node.ip) +
                ' --name=' + config.prefix + node.name +
                ' --hostname=' + config.prefix + node.name +
                ' --rm'
                ' ' + config.selfish_node_image +
                ' bash -c "' + cmd + '"; ')


def exec_cmd(node, command):
        return ('docker exec '
                + config.prefix + node + ' '
                + command)


def create_network(ip_range):
        return ('docker network create'
                ' --subnet=' + ip_range +
                ' --driver bridge isolated_network')


def rm_network():
        return 'docker network rm isolated_network'


def fix_data_dirs_permissions():
        return ('docker run '
                ' --rm --volume $PWD/' + config.root_dir + ':/mnt' + ' ' + config.node_image + ' chmod a+rwx --recursive /mnt')


def rm_container(name):
        return 'docker rm --force ' + config.prefix + name


def ps_containers():
        return 'docker ps -a -q -f "name={}*"'.format(config.prefix)


def remove_all_containers():
        return 'docker rm -f $({})'.format(ps_containers())
