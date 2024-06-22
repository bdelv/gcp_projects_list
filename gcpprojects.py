# lists all the GCP projects 
# organisation | Project name | ProjectId | LifecycleState | createTime | Owners

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('cloudresourcemanager', 'v1beta1', credentials=credentials)

class Project(object):
    """__init__() functions as the class constructor"""
    def __init__(self):
        self.name = ""
        self.projectNumber = ""
        self.projectId = ""
        self.lifecycleState = ""
        self.organization = ""
        self.owners = ""
        self.createTime = ""
    def __str__(self):
        return "\""+self.organization+'\";\"'+self.name+'\";\"'+self.projectId+'\";\"'+self.lifecycleState+'\";\"'+self.createTime+'\";\"'+self.owners+"\""

orgs = {}
projects = []
# List the orgs
request = service.organizations().list()
while request:
    response = request.execute()
    for org in response.get('organizations', []):
        #(org)
        orgs[org["organizationId"]] = org["displayName"]
    request = service.organizations().list_next(previous_request=request, previous_response=response)
#print(orgs)

# lists the projects
request = service.projects().list()
#print(request)
while request:
    response = request.execute()
    for project in response.get('projects', []):
        #print(project)
        proj = Project()
        proj.name = project["name"]
        proj.projectNumber = project["projectNumber"]
        proj.projectId = project["projectId"]
        proj.lifecycleState = project["lifecycleState"]
        proj.createTime = project["createTime"]
        # searches for the owners
        proj.owners = ""
        get_iam_policy_request_body = {}
        requestPolicy = service.projects().getIamPolicy(resource=proj.projectNumber, body=get_iam_policy_request_body)
        responsePolicy = requestPolicy.execute()
        #print(responsePolicy)
        for policy in responsePolicy.get('bindings', []):
            #print(policy)
            if policy["role"] == "roles/owner":
                for owner in policy.get('members', []):
                    #print(owner)
                    if proj.owners != "":
                        proj.owners += '\n'
                    proj.owners += owner
        #print(proj.owners)
        # searches for the ancestors of the projects
        # print(project["projectId"])
        get_ancestry_request_body = {}
        requestAncestor = service.projects().getAncestry(projectId=project["projectId"], body=get_ancestry_request_body)
        responseAncestor = requestAncestor.execute()
        # print(responseAncestor)
        # searches for the oprganization
        for ancestor in responseAncestor.get('ancestor', []):
            if ancestor["resourceId"]["type"] == 'organization':
                #print(ancestor["resourceId"]['id'])
                proj.organization = orgs[ancestor["resourceId"]['id']]
        print(proj)
        projects.append(proj)
    request = service.projects().list_next(previous_request=request, previous_response=response)

#for proj in projects:
#    print(proj)
