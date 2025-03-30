# Definições do oracle

 - Instância: mahideia
 - IP: 150.230.86.233

```sh
# Re-cria swapfile com 4G
sudo rm -rf /.swapfile
sudo dd if=/dev/zero of=/.swapfile bs=1M count=4096
sudo chown root:root /.swapfile
sudo chmod 0600 /.swapfile
sudo mkswap /.swapfile
sudo mount -a

# Instala docker-engine e habilita o serviço
# Os --disablerepo=ol8_oci_included está aí para excluir esse repo que por algum motivo
# está LENTO nesse servidor ae
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum --disablerepo=ol8_oci_included update
sudo yum --disablerepo=ol8_oci_included install docker-ce docker-ce-cli containerd.io
sudo yum --disablerepo=ol8_oci_included install docker-engine -y   
sudo systemctl start docker   
sudo systemctl enable docker

# Lazygit
sudo dnf copr enable atim/lazygit -y
sudo dnf --disablerepo=ol8_oci_included install lazygit

# Criar env
python -m venv venv
python -m pip install -r requirements.txt

```