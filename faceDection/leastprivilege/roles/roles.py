import random
import os
import re


import google.auth
from googleapiclient import discovery
from google.cloud import storage
from google.cloud import datastore

from core.framework import levels
from core.framework.cloudhelpers import deployments, iam, cloudfunctions



LEVEL_PATH = 'leastprivilege/roles'

FUNCTION_LOCATION = 'us-central1'

LEVEL_NAMES = {'pd5': 'PredefinedRole-Vision'}
FARS = {        
         'pd5':['roles/datastore.user','roles/storage.admin']
        }

#entires created in cloud function
F_KINDS =['pd5']


def create(second_deploy=True):

    # Create randomized bucket name to avoid namespace conflict
    nonce = str(random.randint(100000000000, 999999999999))
    nonce_file =  f'core/levels/{LEVEL_PATH}/nonce.txt'
    #write key file in function directory
    with open(nonce_file, 'w') as f:
        f.write(nonce)
    os.chmod(nonce_file, 0o700)
    print(f'Nonce {nonce} has been written to {nonce_file}')
    

    # Set role of default cloud function account
    credentials, project_id = google.auth.default()

   
    
    print("Level initialization finished for: " + LEVEL_PATH)
    # Insert deployment
    config_template_args = {'nonce': nonce}

    template_files = [
        'core/framework/templates/service_account.jinja',
        'core/framework/templates/iam_policy.jinja',
        'core/framework/templates/bucket_acl.jinja',
        'core/framework/templates/ubuntu_vm.jinja',
        'core/framework/templates/cloud_function.jinja']


    print("Level setup started for: " + LEVEL_PATH)
    
    start_message = ' Use function entrypoints below to access levels \n\n'
    
    for RESOURCE_PREFIX in LEVEL_NAMES:

        LEVEL_NAME = LEVEL_NAMES[RESOURCE_PREFIX]
        fvar = FARS[RESOURCE_PREFIX]

        
        
        func_patha = f'core/levels/{LEVEL_PATH}/{RESOURCE_PREFIX}/functionaccess'
       
        
        #Generate function urls
        
        func_upload_urla = cloudfunctions.upload_cloud_function(func_patha, FUNCTION_LOCATION)
       
       
        #Update deployment with functions
        config_template_args_patch = {f'funca_upload_url_{RESOURCE_PREFIX}':func_upload_urla, 
                                       
                                        f'level_name_{RESOURCE_PREFIX}': LEVEL_NAME, f'resource_prefix_{RESOURCE_PREFIX}':RESOURCE_PREFIX }
        config_template_args.update(config_template_args_patch)

        msg= f'https://{FUNCTION_LOCATION}-{project_id}.cloudfunctions.net/{RESOURCE_PREFIX}-f-access-{nonce}    {LEVEL_NAMES[RESOURCE_PREFIX]}'
        start_message += msg+'\n'

   

    if second_deploy:
        deployments.insert(LEVEL_PATH, template_files=template_files, config_template_args=config_template_args, second_deploy=True)
    else:
        deployments.insert(LEVEL_PATH, template_files=template_files, config_template_args=config_template_args)

    try:
        
        

       
         # Create service account key file
        sa_key = iam.generate_service_account_key(f'{RESOURCE_PREFIX}-access')
        levels.write_start_info(LEVEL_PATH, start_message, file_name=f'{RESOURCE_PREFIX}-access.json', file_content=sa_key)
        
    except Exception as e: 
        exit()

def read_nonce():
    nonce_file =  f'core/levels/{LEVEL_PATH}/nonce.txt'
    level_nonce = ''
    try:
        f = open(nonce_file, "r")
        level_nonce = f.read()
    except Exception as e: 
        print(str(e))
    return level_nonce

def delete_nonce_file():
    try:
        print(f'Deleting nonce file')
        nonce_file =  f'core/levels/{LEVEL_PATH}/nonce.txt'
        if os.path.exists(nonce_file):
            os.remove(nonce_file)
    except Exception as e: 
        print(str(e))

    

def delete_custom_roles(credentials, project_id):
    service = discovery.build('iam','v1', credentials=credentials)
    parent = f'projects/{project_id}'
    try:
        response = service.projects().roles().list(parent= parent, showDeleted = False).execute()
        if 'roles' in response:
            roles = response['roles']
            if len(roles)!=0:
                print(f'Deleting custom roles ')
                NONCE = read_nonce()
                pattern = f'projects/{project_id}/roles/ct'
                for role in roles:
                    if re.search(rf"{pattern}[0-9]*_access_role_{NONCE}", role['name'], re.IGNORECASE):
                        print(role['name'])
                        try:
                            service.projects().roles().delete(name= role['name']).execute()
                        except Exception as e:
                            print('Delete error: '+str(e))
                
    except Exception as e: 
        print('Error: '+str(e))

def  delete_entities(project_id):
    print('Deleting entities')
    nonce = read_nonce()
    all_kinds = []
    all_kinds.extend(F_KINDS)
    try:
        client = datastore.Client()
        for k in all_kinds:
            kind =f'{k}-{nonce}-{project_id}'
            query = client.query(kind=kind)
            entities = query.fetch()
            for entity in entities:
                client.delete(entity.key)
    except Exception as e: 
        print(str(e))

def destroy():

    credentials, project_id = google.auth.default()
    #Delete datastore entity
    delete_entities(project_id)

    # Delete starting files
    levels.delete_start_files()

    # Delete deployment
    deployments.delete()

    delete_custom_roles(credentials, project_id)
    
    delete_nonce_file()
