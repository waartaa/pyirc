# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "fedora/24-cloud-base"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 9000, host: 9000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"
  if Vagrant.has_plugin?("vagrant-hostmanager")
    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
  end
  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder ".", "/vagrant", type:"rsync"
  config.vm.synced_folder ".", "/vagrant", disable: true
  config.vm.synced_folder ".", "/home/vagrant/devel", type: "rsync"
  # If you want to turn on the sshfs uncomment the following line and comment
  # the above mentioned line
  # config.vm.synced_folder ".", "/home/vagrant/devel", type: "sshfs", sshfs_opts_append: "-o nonempty", reverse: true
  #
  # Comment this line if you would like to disable the automatic update during provisioning
  config.vm.provision "shell", inline: "sudo dnf upgrade -y"
  # bootstrap and run with ansible
  config.vm.provision "shell", inline: "sudo dnf -y install python2-dnf libselinux-python"
  config.vm.provision "ansible" do |ansible|
     ansible.playbook = "ansible/vagrant-playbook.yml"
  end
  config.vm.provision "shell", inline: "cd /home/vagrant/devel && sudo python3 setup.py develop"
  config.vm.provision "shell", inline: "sudo systemctl start redis.service"
  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
config.vm.define "ircb" do |ircb|
     ircb.vm.host_name = "ircb-dev.example.com"

     ircb.vm.provider :libvirt do |domain|
         # Season to taste
         domain.cpus = 4
         domain.graphics_type = "spice"
         domain.memory = 2048
         domain.video_type = "qxl"

         # Uncomment the following line if you would like to enable libvirt's unsafe cache
         # mode. It is called unsafe for a reason, as it causes the virtual host to ignore all
         # fsync() calls from the guest. Only do this if you are comfortable with the possibility of
         # your development guest becoming corrupted (in which case you should only need to do a
         # vagrant destroy and vagrant up to get a new one).
         #
         # domain.volume_cache = "unsafe"
     end
  end
end
