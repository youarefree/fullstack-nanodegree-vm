#THIS IS THE README FILE OF MY IMPLEMENTATION OF THE ITEM CATALOG PROJECT
The project is based on the Python programming language in order to continue and execute it one must first download
and install Python 3 . Here is a link : https://www.python.org/downloads/ . 
I suggest installing python 3.7.1.

Also, you will need to install a vitrual machine where you would isolate where the project/database will run as on a Linux server
Here is a link : https://www.virtualbox.org/

Another thing you should install is vagrant: Here is a link : https://www.vagrantup.com/downloads.html .
There are different types depending on your OS.

*Here are some instructions for the installations:*
Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, here. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com. Install the version for your operating system.

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

vagrant --version

If Vagrant is successfully installed, you will be able to run vagrant --version in your terminal to see the version number. The shell prompt in your terminal may differ. Here, the $ sign is the shell prompt.

Download the VM configuration
Use Github to fork and clone, or download, the repository https://github.com/udacity/fullstack-nanodegree-vm.

You will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory:

vagrant-directory

Navigating to the FSND-Virtual-Machine directory and listing the files in it. This picture was taken on a Mac, but the commands will look the same on Git Bash on Windows.

Instructions
Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

vagrant-up-start

Starting the Ubuntu Linux installation with vagrant up. This screenshot shows just the beginning of many, many pages of output in a lot of colors.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!

linux-vm-login

Logging into the Linux VM with vagrant ssh.

Logged in
If you are now looking at a shell prompt that starts with the word vagrant (as in the above screenshot), congratulations — you've gotten logged into your Linux VM.

If not, take a look at the Troubleshooting section below.

The files for this course
Inside the VM, change directory to /vagrant and look around with ls.

The files you see here are the same as the ones in the vagrant subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM.

Files in the VM's /vagrant directory are shared with the vagrant folder on your computer. But other data inside the VM is not. For instance, the PostgreSQL database itself lives only inside the VM.

*Instructions for running the project it self*
After installing all the prerequisites you need to get hold of the project itself,
you can get it from here: https://github.com/youarefree/fullstack-nanodegree-vm/tree/master/vagrant/catalog
You can fork it so you can make changes on your own device later on.
You need to get it to your machine by downloading or in other words cloning it.
You need to write in your terminal "git clone https://github.com/YOUR-USERNAME/fullstack-nanodegree-vm/tree/master/vagrant/catalog"
YOUR-USERNAME must be substituted with your username :)

Done that, you need to go to your terminal and cd into the foler of the VAGRANTFILE. There you need to run the commands
vagrant up 
vagrant ssh
In order to get your virtual machine up and running.
There is a shared folder to which you need to cd in. It is called /vagrant
There you can find the catalog folder which you also have to cd into. There you can find several python files
which you have to run with the command python.

You have to run them in the correct order with the command python in front.
The first one is the database_setup.py and judging by its name it gives a setup of a database and creates it in the same folder.
The second one is the populateDatabase.py file and also we can find out a bit by its name. It puts some initial data into our database.
And finally, you can run the ItemCatalog.py file in order to get the website up and running on your local machine, port 5000.
After which, if you go to your browser and open http://localhost:5000/ you will see the home page of the website in question.

It is supposed to be an item catalog, but its interface is a bit like an Online Store just for kicks :)
Enjoy.