import requests

URL = "https://api.mg-rast.org/metadata/export/mgp385"

class Data_pull:
    
    def __init__(self):
        self.response = None
        self.pulled_data = None
        self.human_project_id_list = []
        self.human_project_name_list = []

    def pull_data(self, url):
        self.url = url
        try:
            with requests.session() as ses:
                try:
                    self.response = ses.get(self.url, timeout=120)
                except requests.exceptions.Timeout as e:
                    print(f"TimeoutError: The connection timed out \n {e} \n")
                    raise
        
            if self.response.status_code == requests.codes.ok:
                print(f"Good request for url: {self.url}.\n")
        
            try:
                self.response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"HTTPError: {self.response.text} \n {e} \n")
                raise
    
            try:
                self.pulled_data = self.response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(f"JSONDecodeError: The file must be JSON. \n {e} \n")
                raise
        
   
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError: Connection refused, try it again later. \n {e} \n")
            raise

        return self.pulled_data
    
    def get_human_wgs_projects(self, json_dic):
        for item in json_dic['data']:
            if item['sequence_type'] == 'WGS' and item['project_id'] not in self.human_project_id_list:
                self.human_project_id_list.append(item['project_id'])
                self.human_project_name_list.append

data_pull = Data_pull() 

meta_data_human_skin = data_pull.pull_data("https://api.mg-rast.org/search?limit=1000&env_package=human-skin&sequence_type=WGS")
meta_data_human_associated = data_pull.pull_data("https://api.mg-rast.org/search?limit=1000&env_package=human-associated&sequence_type=WGS")
meta_data_human_gut = data_pull.pull_data("https://api.mg-rast.org/search?limit=1000&env_package=human-gut&sequence_type=WGS")
meta_data_human_oral = data_pull.pull_data("https://api.mg-rast.org/search?limit=1000&env_package=human-oral&sequence_type=WGS")

data_pull.get_human_wgs_projects(meta_data_human_skin)
data_pull.get_human_wgs_projects(meta_data_human_associated)
data_pull.get_human_wgs_projects(meta_data_human_gut)
data_pull.get_human_wgs_projects(meta_data_human_oral)

print(data_pull.human_project_id_list)
print(len(data_pull.human_project_id_list))
