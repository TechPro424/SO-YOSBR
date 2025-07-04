import requests, os, shutil, json, sys
from zipfile import ZipFile
useragent = {'user-agent': 'TechPro424/SO_YOSBR'}
latest = (requests.get(url = 'https://api.modrinth.com/v2/project/BYfVnHa7/version', headers=useragent).json())[0]
latest_id = latest.get('id')

#"check if there is a corresponding version in my project"
latest_mypack_changelog = (requests.get(url='https://api.modrinth.com/v2/project/Uq3JO1Dp/version', headers=useragent).json())[0].get('changelog')
if latest_mypack_changelog.startswith(latest_id): 
    print('Already exists')
    sys.exit()



'''download SO zip file'''
so_file_content = requests.get(url=latest.get('files')[0].get('url'), stream=True, headers=useragent)
with open('SO.zip', 'wb') as so_file:
    for chunk in so_file_content.iter_content(chunk_size=1024):
        if chunk: so_file.write(chunk)

'''extract zip file'''
os.makedirs('.\\SO', exist_ok=True)

with ZipFile('SO.zip', 'r') as zip:
    zip.extractall(path='.\\SO')
    zip.close()

mc_version = latest.get('game_versions')[0]

yosbr_req = requests.get(url=('https://api.modrinth.com/v2/project/WwbubTsV/version?game_versions=["' + mc_version + '"]'), headers=useragent)
if not (yosbr_req.json()): yosbr_req = requests.get(url=('https://api.modrinth.com/v2/project/WwbubTsV/version'), headers=useragent)


yosbr_file_content = requests.get(url=yosbr_req.json()[0].get('files')[0].get('url'), stream=True, headers=useragent)
os.makedirs('.\\SO\\overrides\\mods', exist_ok=True)
with open('.\\SO\\overrides\\mods\\yosbr.jar', 'wb') as yosbr_file:
    for chunk in yosbr_file_content.iter_content(chunk_size=1024):
        if chunk: yosbr_file.write(chunk)

os.makedirs( '.\\SO\\overrides\\config\\yosbr\\', exist_ok=True)
shutil.move('.\\SO\\overrides\\options.txt', '.\\SO\\overrides\\config\\yosbr\\')

os.remove('SO.zip')
shutil.make_archive('SO', 'zip', 'SO')
os.rename('SO.zip', 'SO.mrpack')
shutil.rmtree('.\\SO\\')


files = {'file': open('SO.mrpack', 'rb')}

data = {
        'name': latest.get('name'), 
        'version_number': latest.get('version_number'),
        'changelog': latest_id + '\n\n\n' + latest.get('changelog') + '\n\n\n',
        'dependencies': latest.get('dependencies'),
        'game_versions': latest.get('game_versions'),
        'version_type': latest.get('version_type'),
        'loaders': latest.get('loaders'),
        'featured': latest.get('featured'),
        'status': latest.get('status'),
        'requested_status': latest.get('requested_status'),
        'project_id': 'Uq3JO1Dp',
        'file_parts': ['file'],
        'primary_file': 'file'}

'''
data = {
        'name': '1.21.7-2.1', 
        'version_number': '1.21.7-2.1',
        'changelog': 'latest_id' + '\n' + 'test' + '\n',
        'dependencies': [],
        'game_versions': ['1.21.7'],
        'version_type': 'release',
        'loaders': ['fabric'],
        'featured': False,
        'status': 'listed',
        'requested_status': 'listed',
        'project_id': 'Uq3JO1Dp',
        'file_parts': ['file'],
        'primary_file': 'file'}
        '''
payload = {'data': json.dumps(data)}
token = os.environ.get('TOKEN')
useragent.update({'Authorization': token})
upload = requests.post('https://api.modrinth.com/v2/version', files=files, headers=useragent, data=payload)





