import requests
import json
import sys
from logjuicer import LogJuicer


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


def check_jira_config():

    """Check if Jira configuration is available."""
    # Since Jira is configured in olsconfig.yaml, we don't need to check environment variables
    # The MCP server will handle the configuration
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage help:\n\
        python agent.py ask <query>\n\
        python agent.py analyze <logfile> [project_key]\n\
        python agent.py analyze-with-jira <logfile> <project_key>")
        sys.exit(1)
    
    client = OLSClient("http://0.0.0.0:8080")
    if client:
        print("Connected to Lightspeed Service")
    
    # Check Jira configuration
    jira_enabled = check_jira_config()
    
    match sys.argv[1]:
        case 'ask':
            query = " ".join(sys.argv[2:])
            print("Asking Openshift Lightspeed Service")
            try:
                response = client.query(query)
                print("Response:", json.dumps(response, indent=2))
                
                # Display the main response
                main_response = response.get("response", "")
                if main_response:
                    print('------------------------------------------->\n' 
                          + main_response)
                
                # Display tool results if available
                tool_results = response.get("tool_results", [])
                if tool_results:
                    print("\n" + "="*50)
                    print("TOOL RESULTS:")
                    print("="*50)
                    for tool_result in tool_results:
                        if tool_result.get("status") == "success":
                            content = tool_result.get("content", "")
                            if content:
                                print(f"\n{tool_result.get('name', 'Tool')} "
                                      f"Result:")
                                print("-" * 30)
                                print(content)
                                print("-" * 30)
                
            except Exception as e:
                print(f"Error: {e}")
        
        case 'analyze':
            filename = sys.argv[2]
            project_key = sys.argv[3] if len(sys.argv) > 3 else None
            
            print("Analyzing logfile", filename)
            juicer = LogJuicer(filename)
            logdiff = juicer.juice()
            if logdiff is None:
                print("Error during logjuicer execution")
                sys.exit(1)
            print("Diff generated from baseline for logtype\n",
                  juicer.logtype, logdiff)
            
            prompt = """This is a log diff of a failure in an OS latency,\
            network latency or other performance related test,\
            analyze this log, write a triage summary describing failure and \
            give the exact path to relevant must-gather log files\n\
                """
            
            if project_key and jira_enabled:
                prompt += f"\n\nAdditionally, search for related Jira issues in project '{project_key}' that might be related to this failure."
            
            query = prompt + logdiff

            try:
                response = client.query(query)
                
                # Display the main response
                main_response = response.get("response", "")
                if main_response:
                    print('------------------------------------------->\n' 
                          + main_response)
                
                # Display tool results if available
                tool_results = response.get("tool_results", [])
                if tool_results:
                    print("\n" + "="*50)
                    print("TOOL RESULTS:")
                    print("="*50)
                    for tool_result in tool_results:
                        if tool_result.get("status") == "success":
                            content = tool_result.get("content", "")
                            if content:
                                print(f"\n{tool_result.get('name', 'Tool')} "
                                      f"Result:")
                                print("-" * 30)
                                print(content)
                                print("-" * 30)
                
            except Exception as e:
                print(f"Error: {e}")
        
        case 'analyze-with-jira':
            if len(sys.argv) < 4:
                print("Usage: python agent.py analyze-with-jira <logfile> <project_key>")
                sys.exit(1)
            
            filename = sys.argv[2]
            project_key = sys.argv[3]
            
            print(f"Analyzing logfile {filename} with Jira integration for project {project_key}")
            juicer = LogJuicer(filename)
            logdiff = juicer.juice()
            if logdiff is None:
                print("Error during logjuicer execution")
                sys.exit(1)
            print("Diff generated from baseline for logtype\n",
                  juicer.logtype, logdiff)
            
            prompt = f"""This is a log diff of a failure in an OS latency,\
            network latency or other performance related test.\
            
            Please:
            1. Analyze this log and write a triage summary describing the 
               failure
            2. Give the exact path to relevant must-gather log files based 
               on the log content (do not use oc_logs tool)
            3. Use the search_jira_issues tool to find related Jira issues 
               in project '{project_key}' that might be related to this failure
            4. Present the Jira search results separately from your analysis
            
            Important: Do not use the oc_logs tool as it requires cluster 
            access. Focus on analyzing the provided log content and using 
            the search_jira_issues tool for Jira integration.
            
            Log diff:
            """
            
            query = prompt + logdiff

            try:
                response = client.query(query)
                
                # Debug: Print the full response structure for analyze-with-jira
                print("DEBUG: Full response structure:")
                print(f"Response keys: {list(response.keys())}")
                print(f"Has tool_results: {'tool_results' in response}")
                if 'tool_results' in response:
                    print(f"Tool results count: {len(response['tool_results'])}")
                
                # Display the main response
                main_response = response.get("response", "")
                if main_response:
                    print('------------------------------------------->\n' 
                          + main_response)
                
                # Display tool results if available
                tool_results = response.get("tool_results", [])
                if tool_results:
                    print("\n" + "="*50)
                    print("TOOL RESULTS:")
                    print("="*50)
                    for i, tool_result in enumerate(tool_results):
                        print(f"\nTool Result {i+1}:")
                        print(f"Status: {tool_result.get('status')}")
                        print(f"Name: {tool_result.get('name', 'Unknown')}")
                        print(f"Content: {tool_result.get('content', 'No content')}")
                        print(f"Type: {tool_result.get('type', 'Unknown')}")
                        if tool_result.get("status") == "success":
                            content = tool_result.get("content", "")
                            if content:
                                print(f"\n{tool_result.get('name', 'Tool')} "
                                      f"Result:")
                                print("-" * 30)
                                print(content)
                                print("-" * 30)
                else:
                    print("\nNo tool results found in response")
                
            except Exception as e:
                print(f"Error: {e}")
        
        case _:
            print("unknown option")
