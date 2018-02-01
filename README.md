# WinRM Tester

A script to test if the WinRM service is working on target machine

## How to use it

Windows or Unix:

```bash
    python main.py -t 101.103.102.88 -u my_user -p my_password

    or

    # Ommiting the -p will make the CLI ask for the password
    python main.py -t 101.103.102.88 -u my_user
    Enter the Password:
```

Unix bashs style only:

```bash
    chmod +x main.py
    ./main.py -t 101.103.102.88 -u my_user -p my_password

    # Ommiting the -p will make the CLI ask for the password
    ./main.py -t 101.103.102.88 -u my_user
    Enter the Password:
```

The mandatory parameters are:

- `-t` or `--target` , the target machine that will receive the WinRM connection.
- `-u` or `--user` , the username for the user on the WinRm connection.

The optional parameters are:

- `-p` or `--password`, the password for the user on the WinRm connection.
- `-h` or `--help` , shows the help message with the available parameters.
- `-port` , let you choose in which port the WinRM connection will happen.
- `-d` or `--debug`, shows debug messages when running the script.
- `-o` or `--output`, let you choose the name of the output file when running with multiple target hosts. (default=output.json)

## Developing

### Pre-requisites

- Latest Python 3 installed
- Setup a virtual env:
  - From the folder of the project execute: `python -m venv venv`
- Activate the virtual env: 
  - If you are executing Bash on **Linux**, from the folder of the project execute: `source /venv/bin/activate`.
  - If you are executing on **Windows**, from the folder of the project execute: `.\venv\Scripts\activate`.

### How to run

- Install dependencies:
  - `pip install -r requirements.txt`
- Run the script:
    - `python main.py`