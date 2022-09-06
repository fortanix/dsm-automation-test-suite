# DSM Frontend Test Bench

Test bench for DSM frontend using pytest-selenium. It generates reports in allure and HTML.

### *Dependencies*
* [Python3](https://www.python.org/downloads/)
* Browsers - Chrome, Firefox, Edge

### *Running tests in docker container*
The docker image has the browsers and other dependencies installed.
```commandline
docker build . -t dsmqa
docker run -v `pwd`/reports:/app/reports dsmqa -m smoke --URL $URL --EMAIL $EMAIL --PASSWORD $PASSWORD --ACCOUNT_ID $ACCOUNT_ID --BROWSER=$BROWSER
```
Optionally, `–add-host` option can be passed to add host-entries onto /etc/hosts when the container is run.
The execution reports will be stored in reports directory once the execution is completed.

### *Local Environment setup*
```commandline
python3 -m venv dsmenv
source dsmenv/bin/activate
python3 -m pip install -r requirements.txt
```
### *Usage*
```
pytest -m smoke --URL $URL --EMAIL $EMAIL --PASSWORD $PASSWORD --ACCOUNT_ID $ACCOUNT_ID --BROWSER=$BROWSER
```

Test Arguments:

```
-m              Pytest marker to run tests. e.g: smoke, apps, dashboard, groups, security_objects

--URL	        URL endpoint to be used for running tests

--EMAIL         Email ID to be used for logging in

--PASSWORD      Password to be used for logging in

--ACCOUNT_ID    Account ID to be used for test operations

--BROWSER       Optional argument to run tests with different browsers. e.g: Chrome(default), Firefox, Edge

--BROWSER_MODE  Optional argument to run test in head/headless mode.
```

# Contributing

We gratefully accept bug reports and contributions from the community.
By participating in this community, you agree to abide by [Code of Conduct](./CODE_OF_CONDUCT.md).
All contributions are covered under the Developer's Certificate of Origin (DCO).

## Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
have the right to submit it under the open source license
indicated in the file; or

(b) The contribution is based upon previous work that, to the best
of my knowledge, is covered under an appropriate open source
license and I have the right under that license to submit that
work with modifications, whether created in whole or in part
by me, under the same open source license (unless I am
permitted to submit under a different license), as indicated
in the file; or

(c) The contribution was provided directly to me by some other
person who certified (a), (b) or (c) and I have not modified
it.

(d) I understand and agree that this project and the contribution
are public and that a record of the contribution (including all
personal information I submit with it, including my sign-off) is
maintained indefinitely and may be redistributed consistent with
this project or the open source license(s) involved.

# License

This project is primarily distributed under the terms of the Mozilla Public License (MPL) 2.0, see [LICENSE](./LICENSE) for details.