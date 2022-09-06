import json
import traceback
import uuid

import requests
from requests.auth import HTTPBasicAuth

from utils.logger_util import get_logger

logger = get_logger(__name__)

HEADERS = {"Authorization": "", "Content-Type": "application/json"}


class API:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        url = self.host + "sys/v1/session/auth"
        response = requests.post(url, auth=HTTPBasicAuth(username, password), verify=False)
        logger.debug(f"authenticate user response: {response.text}")
        self.data = response.json()
        self.user_id = self.data["entity_id"]
        self.access_token = self.data["access_token"]
        self.token_type = self.data["token_type"]
        self.auth_token = "Bearer " + self.access_token

    def get_all_accounts(self):
        url = self.host + "sys/v1/accounts"
        headers = {"Authorization": self.auth_token}
        response = requests.request("GET", url, headers=headers, verify=False)
        acct_ids = [i.get("acct_id") for i in response.json() if i.get("name") != "System Administration"]
        logger.debug(f"Number of accounts: {len(acct_ids)}")
        return acct_ids

    def select_account(self, account_id):
        url = self.host + "sys/v1/session/select_account"
        payload = '{\n  "acct_id": "' + account_id + '"\n}'
        headers = {"Authorization": self.auth_token}
        requests.request("POST", url, data=payload, headers=headers, verify=False)
        logger.debug(f"Account {account_id} is selected.")

    def get_account_details(self, account_id):
        url = self.host + f"sys/v1/accounts/{account_id}"
        headers = {"Authorization": self.auth_token}
        data = requests.get(url, headers=headers, verify=False)
        logger.debug(f"Account data: {data.text}")
        return data

    def get_user(self, user_id):
        url = self.host + f"sys/v1/users/{user_id}"
        headers = {"Authorization": self.auth_token}
        data = requests.get(url, headers=headers, verify=False)
        logger.debug(f"user details: {data.text}")
        return data

    def update_user_first_last_name(self, user_id, first_name, last_name):
        url = self.host + f"sys/v1/users/{user_id}"
        headers = {"Authorization": self.auth_token}
        payload = json.dumps({"user_id": user_id, "first_name": first_name, "last_name": last_name})
        data = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
        logger.info(f"updated user details: {data.text}")
        return data

    def invite_user(self, user, account_id):
        url = self.host + "sys/v1/users/invite"
        headers = {"Authorization": self.auth_token}
        invite_user = requests.post(url, headers=headers, json=user, verify=False)
        logger.debug("user " + invite_user.json()["user_id"] + " invited to account " + account_id)

        process_invite_url = self.host + "sys/v1/users/process_invite"
        process_invite = requests.post(
            process_invite_url,
            headers=user["headers"],
            json={"accepts": [account_id]},
            verify=False,
        )
        logger.debug(
            "invite user " + str(user["Email"]) + " to account " + account_id + "response:" + process_invite.text
        )

    def get_all_groups(self):
        url = self.host + "sys/v1/groups"
        headers = {"Authorization": self.auth_token}
        response = requests.request("GET", url, headers=headers, verify=False).json()
        group_ids = [i.get("group_id") for i in response]
        logger.debug(f"List of All GroupIDs: {group_ids}")
        return group_ids

    def approve_all_pending_requests(self, account_id):
        logger.debug(f"Select account: {account_id}")
        self.select_account(account_id)
        approval_requests = self.host + "/sys/v1/approval_requests?status=PENDING"
        headers = {"Authorization": self.auth_token}
        res = requests.get(approval_requests, headers=headers, data={}, verify=False)
        total_reqs_num = len(res.json())
        logger.debug(f"Num of approve requests for account {account_id}: {total_reqs_num}")
        for index, data in enumerate(res.json()):
            quorum_request_id = data["request_id"]
            logger.debug(f"[{index}/{total_reqs_num}] Approve request id: {data['request_id']}")
            url = self.host + "sys/v1/approval_requests/" + quorum_request_id + "/approve"
            out = requests.request("POST", url, headers=headers, data={}, verify=False)
            logger.debug(
                f"[{index}/{total_reqs_num}] Approved request {quorum_request_id} for account {account_id}: {out.text}"
            )

    def remove_groups_policy_quorum_kup_hsm(self, group_id):
        url = self.host + "sys/v1/groups/" + group_id
        headers = {"Authorization": self.auth_token}
        grp_response = requests.request("GET", url, headers=headers, data={}, verify=False).json()
        logger.debug(f"grp_response: {grp_response}")

        # Delete Quorum Policy
        if "approval_policy" in grp_response:
            url = self.host + "sys/v1/approval_requests"
            payload = json.dumps(
                {
                    "method": "PATCH",
                    "operation": f"/sys/v1/groups/{group_id}",
                    "body": {"approval_policy": {}},
                }
            )
            delete_quorum_request = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
            delete_quorum_request_id = delete_quorum_request["request_id"]

            # Approve delete quorum policy
            url = self.host + "sys/v1/approval_requests/" + delete_quorum_request_id + "/approve"
            requests.request("POST", url, headers=headers, data={}, verify=False)
            logger.debug(f"Delete quorum policy request ID: {delete_quorum_request_id}")

        # Delete Key Undo Policy
        if "key_history_policy" in grp_response:
            url = self.host + "sys/v1/groups/" + group_id
            payload = json.dumps({"group_id": group_id, "key_history_policy": "remove"})
            requests.request("PATCH", url, headers=headers, data=payload, verify=False)

        # Delete HSM from Group
        if "hmg" in grp_response:
            hmg_id = list(grp_response["hmg"].keys())[0]
            logger.debug(hmg_id)
            logger.debug(type(hmg_id))
            url = self.host + "sys/v1/groups/" + group_id
            payload = json.dumps({"group_id": group_id, "del_hmg": [hmg_id]})
            requests.request("PATCH", url, headers=headers, data=payload, verify=False)
            logger.debug(requests.status_codes)

    def get_all_security_objects(self):
        url = self.host + "crypto/v1/keys?show_destroyed=true&show_deleted=true&show_value=false&limit=1000&offset=0"
        headers = {"Authorization": self.auth_token}
        response = requests.request("GET", url, headers=headers, data={}, verify=False).json()
        kids = [i.get("kid") for i in response]
        logger.debug(f"List of All Kids: {kids}")
        for kid in kids:
            history_ids = []
            for i in response:
                if i.get("kid") == kid and "history" in i:
                    for his_id in i.get("history"):
                        history_ids.append(str(his_id.get("id")))
            logger.debug("history_id: " + str(history_ids))
            url = self.host + f"crypto/v1/keys/{kid}/revert"
            payload = json.dumps({"ids": history_ids})
            requests.put(url, headers=headers, data=payload, verify=False)
        return kids

    def delete_key(self, kid):
        # Delete Destroyed Keys
        url = self.host + "crypto/v1/keys/" + kid
        headers = {"authorization": self.auth_token}
        response = requests.request("DELETE", url, headers=headers, verify=False)
        logger.debug(f"Delete key api response: {response.text}")
        logger.debug(f"Key Deleted: {kid}")

    def get_all_plugins(self):
        url = self.host + "sys/v1/plugins"
        headers = {"authorization": self.auth_token}
        response = requests.request("GET", url, headers=headers, verify=False).json()
        plugin_ids = [i.get("plugin_id") for i in response]
        logger.debug(f"List of Plugins {plugin_ids}")
        return plugin_ids

    def delete_plugin(self, plugin_id):
        url = self.host + "sys/v1/plugins/" + plugin_id
        headers = {"authorization": self.auth_token}
        response = requests.request("DELETE", url, headers=headers, verify=False)
        logger.debug(response.text)
        logger.debug(f"Plugin deleted {plugin_id}")

    def get_all_apps(self):
        url = self.host + "sys/v1/apps/"
        headers = {"authorization": self.auth_token}
        url1 = self.host + "sys/v1/apps"
        querystring = {"role": "admin"}
        normal_apps_response = requests.request("GET", url, headers=headers, verify=False).json()
        admin_apps_response = requests.request("GET", url1, params=querystring, headers=headers, verify=False).json()
        normal_app_ids = [i.get("app_id") for i in normal_apps_response]
        admin_app_ids = [i.get("app_id") for i in admin_apps_response]
        app_ids = normal_app_ids + admin_app_ids
        logger.debug(f"List of apps: {app_ids}")
        return app_ids

    def delete_app(self, app_id):
        url = self.host + "sys/v1/apps/" + app_id
        headers = {"authorization": self.auth_token}
        response = requests.request("DELETE", url, headers=headers, verify=False)
        logger.debug(response.text)
        logger.debug(f"App Deleted: {app_id}")

    def delete_group(self, grp_id):
        url = self.host + f"sys/v1/groups/{grp_id}"
        headers = {"authorization": self.auth_token}
        requests.delete(url=url, headers=headers, verify=False)
        logger.debug(f"Group Deleted: {grp_id}")

    def get_kek_group_ids(self, group_ids):
        url = self.host + "sys/v1/groups/"
        headers = {"authorization": self.auth_token}
        kek_grp_ids = []
        for index, grp_id in enumerate(group_ids):
            response = requests.get(url + grp_id, headers=headers, verify=False)
            logger.debug(f"{index}, {response.json().get('group_id')}, {response.json().get('wrapping_key_name')}")
            if response.json().get("wrapping_key_name"):
                kek_grp_ids.append(response.json()["group_id"])
        logger.debug(f"kek_grp_ids: {kek_grp_ids}")
        return kek_grp_ids

    def remove_kek_from_group(self, kek_grp_id):
        url = self.host + "sys/v1/groups/"
        headers = {"authorization": self.auth_token}
        response = requests.get(url + kek_grp_id, headers=headers, verify=False)
        logger.debug(f"{response.json().get('group_id')}, {response.json().get('wrapping_key_name')}")
        logger.debug(f"wrapping_key_name BEFORE: {response.json().get('wrapping_key_name')}")
        payload = {"group_id": kek_grp_id, "wrapping_key_name": None}
        response = requests.patch(url + kek_grp_id, headers=headers, json=payload, verify=False)
        data = response.json()
        logger.debug(f"wrapping_key_name AFTER: {data.get('wrapping_key_name')}")

    def remove_objects_from_account(self, account_id):
        try:
            logger.debug(f"Remove account with id: {account_id}")
            self.select_account(account_id)

            # Remove groups policy quorum kup hsm
            group_ids = self.get_all_groups()
            for group_id in group_ids:
                self.remove_groups_policy_quorum_kup_hsm(group_id)

            # Remove KEK from group
            kek_group_ids = self.get_kek_group_ids(group_ids)
            for kek_group_id in kek_group_ids:
                self.remove_kek_from_group(kek_group_id)

            # Delete Security Objects
            kids = self.get_all_security_objects()
            for kid in kids:
                self.delete_key(kid)

            # Delete Plugins
            plugins = self.get_all_plugins()
            for plugin in plugins:
                self.delete_plugin(plugin)

            # Delete Apps
            app_ids = self.get_all_apps()
            for app_id in app_ids:
                self.delete_app(app_id)

            # Delete Groups
            for group_id in group_ids:
                self.delete_group(group_id)
        except Exception as e:
            logger.debug(f"Failed to remove objects from account id {account_id}")
            logger.debug(traceback.print_exc())
