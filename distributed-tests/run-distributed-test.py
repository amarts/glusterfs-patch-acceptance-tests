#!/usr/bin/env python
import subprocess
import argparse
import sys
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager


def get_ansible_host_ip():
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources='hosts')
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    hostnames = []
    for host in inventory.get_hosts():
        hostnames.append(variable_manager.get_vars(host=host))
    ip = ' '.join([str(i['ansible_host']) for i in hostnames])
    return str(ip)


def main():
    parser = argparse.ArgumentParser(description="Run distributed test")
    parser.add_argument("--n", help="Maximum number of machines to use")
    args = parser.parse_args()
    ip = get_ansible_host_ip()
    failed_tests = subprocess.call(['/opt/qa/distributed-tests/distributed-test.sh',
                                    '--hosts', '%s' % ip, '--id-rsa', 'key', '-n',
                                    '%s' % args.n, '-v'])
    sys.exit(failed_tests)


if __name__ == '__main__':
    main()
