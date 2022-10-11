# doctors-search-beep

This repository is for educational purposes only.

This repository contains an example script that could help you to find free
slots for doctor apointment in Lithuania.

This script periodically fetches data from website and notifies if apointment
entries are found

Initially it is intended to run on [AML-S805X-AC (La Frite)](https://libre.computer/products/s805x/)
to not waste electricity but can be easily modified to run on any HW

## Prerequisites

* Python3
* Python virtualenv module (optional)
* Linux OS/systemd (optional)

## Usage

The following information describes how to run this script as systemd service,
on Linux operating system. Please search how to perform same steps on other
operating systems by yourself

* create virtual environment (it not created already)
```bash
virtualenv .env
```

* activate virtualenv
```bash
source .env/bin/activate
```

* install python dependencies
```bash
pip install -r requirements.txt
```

* prepare systemd service
```bash
python generate_systemd.py
```

## Known limitations

* Code structure is not separating GPIO libs properly

## Contributing

You are welcome to update this script.

### Git commit message convention:
```bash                                                                                                                 
<type>: <subject>                                                                                                 
```  
"type" must be one of the following mentioned below: 
* build: Build related changes (eg: npm related/ adding external dependencies)
* chore: A code change that external user won't see (eg: change to .gitignore file or .prettierrc file)
* feat: A new feature
* fix: A bug fix
* docs: Documentation related changes
* refactor: A code that neither fix bug nor adds a feature. (eg: You can use this when there is semantic changes like renaming a variable/ function name)
* perf: A code that improves performance
* style: A code that is related to styling
* test: Adding new test or making changes to existing test

"subject":
* use imperative, present tense (eg: use "add" instead of "added" or "adds")
* don't use dot(.) at end
* don't capitalize first letter

