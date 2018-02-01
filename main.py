#!/usr/bin/env python3
import sys
import argparse
import getpass
import socket
import json
from winrm import Protocol,Session

def inicialize_arguments_parser():
    parser = argparse.ArgumentParser(description='A script to test if the WinRM service is working on target machine')

    parser.add_argument('-t', '--targets', help='Targets windows host', required=True, nargs='+', dest='targets')
    parser.add_argument('-u', '--user', help='Username for the WinRM connection',required=True, dest='user')
    parser.add_argument('-p', '--password', help='Password for the WinRM connection',required=False, dest='password')
    parser.add_argument('-port', help='Change the WinRM connection port',required=False, default="5986", dest='port')
    parser.add_argument('-d', '--debug' , help='Enable debug messages',required=False,action='store_true', dest='debug')
    parser.add_argument('-o,' '--output', help='Output file', required=False, default="output.json", dest='output')
    args = parser.parse_args()
    
    return args

def test_winrm_connection(target, port, user, password):
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
        return {"msg":"Connection succeed.", "error": "", "output_command": std_out, "status_code": status_code}

    except Exception:     
        return {"msg":"Connection failed.", "error": sys.exc_info()[1] , "output_command": "", "status_code": ""}

def main():

    # Extract args from CLI
    args = inicialize_arguments_parser()
    targets = args.targets
    user = args.user
    port = args.port
    password = args.password
    debug = args.debug
    output_file = args.output
    
    if password is None:
        password = getpass.getpass('Enter the Password: ')

    if(len(targets) == 1):
        result = test_winrm_connection(targets[0], port, user, password)
        if(result['msg'] == "Connection succeed."):
            if(debug):
                print(result['status_code'])
                print(result['output_command'])
            sys.stdout.write('0')
            return 0
        else:
            if(debug):
                print(result['error'])                
            sys.stdout.write('1')
            return 1
    else:
        output_dict = {}
        for i, target in enumerate(targets):        
            ip = "Unknown"
            try:            
                ip = socket.gethostbyname(target)
            except Exception:     
                sys.stderr.write("Could not resolve {} host".format(target))
            print("[{index}/{total}] {current_target}\n".format(index=i+1,total=len(targets), current_target=target))
            result = test_winrm_connection(target, port, user, password)
            output_dict[target]= { "ip": ip , "status": str(result["error"]) }
            
            temp_dict = { target: { 
                            "ip": ip ,
                            "status": str(result["error"])
                            }
                        }
            with open("temp-" + output_file, 'a') as file:
                file.write(json.dumps(temp_dict, indent=2, sort_keys=True))    
                file.write("\n")    
        print("Writing output file: {}\n".format(output_file))
        with open(output_file, 'w') as file:
            file.write(json.dumps(output_dict, indent=2, sort_keys=True))        

if __name__ == '__main__':
    main()