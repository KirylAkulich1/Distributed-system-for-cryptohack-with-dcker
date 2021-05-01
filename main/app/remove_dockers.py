import subprocess
for i in range(10):
    subprocess.check_output([f'docker rm -f hacker{i}'], shell=True)