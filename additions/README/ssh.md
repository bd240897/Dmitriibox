## SSH

### Create SSH-key (Win 10)
https://www.youtube.com/watch?v=fCQ8ogMHSoo&t=1517s
https://cloud.yandex.ru/docs/compute/operations/vm-connect/ssh

    ssh-keygen -t rsa -b 2048
    // C:\Game\ssh\game-master
    // saySmth
    // open dmitrii_box.pub
    ssh -i C:\ssh\game-master amid@51.250.84.74

### Send file be ssh
    scp -i C:\Games\ssh\game-master Python-3.8.3.tgz amid@84.201.187.44:/home/amid/temp
    ssh -i game-master amid@178.154.207.25