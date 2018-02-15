.PHONY: check-local check-in-vm

IMAGE_NAME := ""
VM_IMAGE := ../Fedora-Cloud-Base-27-1.6.x86_64.qcow2

check-local:
	ansible-playbook -e subject=$(IMAGE_NAME) -v ./tests.yml

check-in-vm: $(VM_IMAGE)
	ansible-playbook -e setup=true -e vm_image=$(VM_IMAGE) ./tests.yml

$(VM_IMAGE):
	curl -o $(VM_IMAGE) -s https://download.fedoraproject.org/fedora/releases/27/CloudImages/x86_64/images/$(VM_IMAGE)

