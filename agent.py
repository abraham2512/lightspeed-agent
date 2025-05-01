import requests
import json
import sys


class OLSClient:
    """Python client for OpenShift Lightspeed service"""

    def __init__(self, url, auth_token=None):
        self.endpoint = f"{url}/v1/query"
        self.auth_token = auth_token

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
        print("Usage help:\npython agent.py ask <query>\n\
              python agent.py analyze <logfile>")
        sys.exit(1)
    client = OLSClient("http://192.168.1.180:8080")
    match sys.argv[1]:
        case 'ask':
            query = " ".join(sys.argv[2:])
            try:
                response = client.query(query)
                print("Response:", json.dumps(response, indent=2))
            except Exception as e:
                print(f"Error: {e}")
        case 'analyze':
            print("Analyzing logdiff with OLS")
            filename = sys.argv[2]
            prompt = """This is a log diff of a failure in an OS latency,\
            network latency or other performance related test,\
            analyze this log, write a short summary and \
            print the relevant log file paths in must-gather\n\
                """
            with open(filename) as file:
                contents = file.read()
                query = prompt+contents
                try:
                    response = client.query(query)
                    print("Response:", json.dumps(response, indent=2))
                except Exception as e:
                    print(f"Error: {e}")
