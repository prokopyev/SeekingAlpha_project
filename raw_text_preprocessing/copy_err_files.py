from shutil import copyfile

with open('live_stream.txt', 'r') as file:
    t = file.readlines()

for i in range(len(t)):
    copyfile(t[i][:-1],
             'data/err_files/{}'.format('copy_' + t[i][:-1].replace('/', '*')))














