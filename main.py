#!/usr/bin/env python3
import sys
import argparse
import getpass
from winrm import Protocol,Session

def inicialize_arguments_parser():
    parser = argparse.ArgumentParser(description='A script to test if the WinRM service is working on target machine')

    parser.add_argument('-t', '--target', help='Target windows host', required=True, dest='target')
    parser.add_argument('-u', '--user', help='Username for the WinRM connection',required=True, dest='user')
    parser.add_argument('-p', '--password', help='Password for the WinRM connection',required=False, dest='password')
    parser.add_argument('-port', help='Change the WinRM connection port',required=False, default="5986", dest='port')
    parser.add_argument('-d', '--debug' , help='Enable debug messages',required=False, default=False, dest='debug')
    args = parser.parse_args()
    
    return args

def main():

    # Extract args from CLI
    args = inicialize_arguments_parser()
    target = args.target
    user = args.user
    port = args.port
    password = args.password
    debug = args.debug

    if password is None:
        password = getpass.getpass('Digite com o Password: ')
    protocol = Protocol(
    endpoint='https://{target}:{port}/wsman'.format(target=target, port=port),
    transport='ntlm',
    username=user,
    password=password,
    server_cert_validation='ignore')
    try:
        shell_id = protocol.open_shell()
        command_id = protocol.run_command(shell_id, 'whoami')
        std_out, std_err, status_code = protocol.get_command_output(shell_id, command_id)
        protocol.cleanup_command(shell_id, command_id)
        protocol.close_shell(shell_id)
        if(debug):        
            print(std_out)
            print(status_code)
        return 0

    except Exception:     
        if(debug):                   
            print("Error while trying to connect via WinRM")
            print(sys.exc_info()[1])
        return 1


if __name__ == '__main__':
    main()