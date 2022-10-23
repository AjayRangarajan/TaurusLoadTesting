## Taurus with Jemeter

### Requirements

 - Load testing tool - **Jmeter**
 - Python 3.7 or above
 - Packages
   - cpython
   - bzt

### Installation

```
pip install bzt
```

### Run Taurus test script

```
bzt kouple_backend_test.yml
```

The above command will look for Jmeter binary in the `C:\Users\USERNAME\.bzt` folder and in PATH variable. If not found, it will install Jmeter in the following location and use this for further tests.

While running the test, it will open Python window and show the progress. After completing, the window will be closed.

After completing the test, the test result will be shown in the command line.

It will create an Artifacts directory with all test details and `jmeter.log` file in the current folder.

### Run Taurus test script with GUI

```
bzt kouple_backend_test.yml -gui
```

The above command will open Jmeter