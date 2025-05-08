import requests
import json
import sys
from logjuicer import LogJuicer
import time


class OLSClient:
    """Python client for OpenShift Lightspeed service"""

    def __init__(self, url, auth_token=None):
        self.endpoint = f"{url}/v1/query"
        self.auth_token = auth_token
        self.connect()

    def connect(self):
        print("Waiting for Lightspeed Service status")
        if requests.get(self.endpoint).status_code == 200:
            print("Service Authenticated")
            return True
        return False

    def query(self, query, model="llama3.1:latest", provider="ollama"):
        payload = {
            "query": query
        }
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        try:
            response = requests.post(self.endpoint, json=payload,
                                     headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to query Lightspeed service: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_data = e.response.json()
                error_msg += f", Error: {error_data.get('error', 'Unknown')}"
            raise Exception(error_msg)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage help:\n\
        python agent.py ask <query>\n\
        python agent.py analyze <logfile>")
        sys.exit(1)
    client = OLSClient("http://192.168.1.180:8080")
    if client:
        print("Connected to Lightspeed Service")
    match sys.argv[1]:
        case 'ask':
            query = " ".join(sys.argv[2:])
            print("Asking Openshift Lightspeed Service")
            try:
                response = client.query(query)
                print("Response:", json.dumps(response, indent=2))
                print('------------------------------------------->\n'
                      + response.get("response"))
            except Exception as e:
                print(f"Error: {e}")
        case 'analyze':
            filename = sys.argv[2]
            print("Analyzing logfile", filename)
            juicer = LogJuicer(filename)
            logdiff = juicer.juice()
            if logdiff is None:
                print("Error during logjuicer execution")
                sys.exit(1)
            print("Diff generated from baseline for logtype\n",
                  juicer.logtype, logdiff)
            print("Analyzing generated logdiff with Lightspeed Service")
            prompt = """This is a log diff of a failure in an OS latency,\
            network latency or other performance related test,\
            analyze this log, write a traige summary describing failure and \
            give the exact path to relevant must-gather log files\n\
                """
            query = prompt+logdiff

            try:
                response = client.query(query)
                # print("Response:", json.dumps(response, indent=2))
                print('------------------------------------------->\n'
                      + response.get("response"))
            except Exception as e:
                print(f"Error: {e}")
        case _:
            print("unknown option")
