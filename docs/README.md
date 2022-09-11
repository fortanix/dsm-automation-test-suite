# Local Environment setup

The automation tests can be executed locally on the linux machine. 

### *Dependencies*
* [Python3](https://www.python.org/downloads/) - v3.8 and above
* Browsers - Chrome, Firefox, Edge

**Browser installation on linux:**
```commandline
apt-get update
apt-get upgrade -y

# Firefox
apt-get install -y firefox

# Chrome
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Edge
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add
add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
apt-get update
apt-get install -y microsoft-edge-dev
```

**Setup virtual environment and install dependencies**
```commandline
python3 -m venv dsmenv
source dsmenv/bin/activate
python3 -m pip install -r requirements.txt
```
### *Usage*
```
pytest -m smoke --URL $URL --EMAIL $EMAIL --PASSWORD $PASSWORD --ACCOUNT_ID $ACCOUNT_ID --BROWSER=$BROWSER --CLEANUP
```
**NOTE**: On passing option `--CLEANUP`, the existing account data will be deleted and test will begin with a clean account. All the previous security objects, groups, apps, plugins would be removed.

**Test Arguments:**

```
-m              Pytest marker to run tests. e.g: smoke, apps, dashboard, groups, security_objects

--URL	        URL endpoint to be used for running tests. e.g: https://amer.smartkey.io/

--EMAIL         Email ID to be used for logging in

--PASSWORD      Password to be used for logging in

--ACCOUNT_ID    Account ID to be used for test operations. Account ID can be copied from DSM UI > Select account > Settings > Click Copy account id icon.

--BROWSER       Optional argument to run tests with different browsers. e.g: Chrome(default), Firefox, Edge

--BROWSER_MODE  Optional argument to run test in head/headless mode. e.g: headless(only runs headless in docker, default), headless

--CLEANUP       Pass the option to clean up the previous data in the account.  
```