from shutil import copyfile

with open('err.txt', 'r') as file:
    t = file.readlines()

for i in range(len(t)):
    copyfile(t[i][:-1],
             'data/err_files/{}'.format('copy_' + t[i][:-1].replace('/', '*')))














