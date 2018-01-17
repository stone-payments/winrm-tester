import sys
import argparse
from winrm import Protocol,Session

def inicialize_arguments_parser():
    parser = argparse.ArgumentParser(description='A script to test if the WinRM service is working on target machine')

    parser.add_argument('-t', '--target', help='Target windows host', required=True, dest='target')
    parser.add_argument('-u', '--user', help='Username for the WinRM connection',required=True, dest='user')
    parser.add_argument('-p', '--password', help='Password for the WinRM connectio',required=True, dest='password')
    args = parser.parse_args()
    
    return args

def main():

    # Extract args from CLI
    args = inicialize_arguments_parser()
    target = args.target
    user = args.user
    password = args.password

    protocol = Protocol(
    endpoint='https://{}:5986/wsman'.format(target),
    transport='ssl',
    username=user,
    password=password,
    server_cert_validation='ignore')
    try:
        shell_id = protocol.open_shell()
        command_id = protocol.run_command(shell_id, 'whoami')
        std_out, std_err, status_code = protocol.get_command_output(shell_id, command_id)
        protocol.cleanup_command(shell_id, command_id)
        protocol.close_shell(shell_id)        
        print(std_out)
        print(status_code)
        return 0

    except Exception:                
        print("Error while trying to connect via WinRM")
        print(sys.exc_info()[1])
        return 1


if __name__ == '__main__':
    main()