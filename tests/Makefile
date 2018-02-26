.PHONY: check-local check-in-vm

IMAGE_NAME := ""
VM_IMAGE_NAME := Fedora-Cloud-Base-27-1.6.x86_64.qcow2
VM_IMAGE_PATH = ../$(VM_IMAGE_NAME)
INVENTORY := /usr/share/ansible/inventory/standard-inventory-qcow2
ANSIBLE_EXTRA_ARGS ?=

check-local:
	ansible-playbook $(ANSIBLE_EXTRA_ARGS) -e subject=$(IMAGE_NAME) ./local.yml

check-in-vm: $(VM_IMAGE_PATH)
	TEST_SUBJECTS=$(VM_IMAGE_PATH) ansible-playbook $(ANSIBLE_EXTRA_ARGS) -e ansible_python_interpreter=/usr/bin/python3 -e subject=$(IMAGE_NAME) -i $(INVENTORY) -e setup=true -e vm_image=$(VM_IMAGE) ./in-vm.yml

$(VM_IMAGE_PATH):
	curl -o $(VM_IMAGE_PATH) -s https://download.fedoraproject.org/fedora/releases/27/CloudImages/x86_64/images/$(VM_IMAGE_NAME)

