# What is NuBerryPi?

NuBerryPi is a fork of the popular [Peerbox project developed by PeerChemist](https://github.com/peerchemist/Peerbox) tailored to the Nu client
All credit goes to PeerChemist as the hard work is his. This Repo has renamed mentions of Peercoin and Peercoind to Nu and Nud and tailored network references to .

## Intro

Thus, this project's ultimate goal is to provide maximum security platform for minting and running nodes. 
* Security will be enforced by underlying OS, which will be hardened by default to repel most of the attack vectors. 
* Secondary goal of NuBerryPi is to provide plug&play platform for running Peercoin nodes and to allow safe minting as easily as running a wallet software.

## Design

NuBerryPi is designed as extension to Arch Linux, well know Linux distribution which focuses on minimalism and simplicity. An ideal distribution to shape to our needs. What is important, Arch Linux provides very simple solution for building packages, it's PKGBUILD scripts allow anyone to compile the entire OS themselves with ease. Being able to understand internals of every package and to be able to quickly learn how to make one on your own is very important to avoid centralization of knowdlege around one developer or team. Best of all, Arch Linux runs on various hardware, starting from high end servers to simple Raspberry Pi, and everything in between.

NuBerryPi platform uses some of well know security philosophies already used in production servers like “principle of least privilege”, limiting every process to as few right it needs to run along with chrooted environments for essential programs. 
Beside that, system will use Grsecurity patches for Linux kernel. Grsecurity is an extensive security enhancement to the Linux kernel that defends against a wide range of security threats through intelligent access control, memory corruption-based exploit prevention, and mandatory access control (MAC). A major component of Grsecurity is its approach to memory corruption vulnerabilities and their associated exploit vectors, which is extremely important to Peercoin since it is coded in C++, a programming language well know for memory corruption vulnerabilities.

NuBerryPi pules packages from upstream Arch Linux repository and pre-configures them to our needs. With dedicated package and git repository so anyone can inspect and build packages them selves, and contribute if they notice something is wrong or just feel like there is better approach. 
It is very important to have user understand risks and dangers involved with crypto currency. We will try to educate our users and explain what can they do to protect their data and privacy in a world that is becoming increasingly hostile to principles of free speech.

## Vision

NuBerryPi will deliver same experience on all platforms but focus on cheap, energy efficient devices like Raspberry Pi or Beaglebone Black which are compatible to general idea of Peercoin in ecological way. NuBerryPi primary platforms will be those who are cheap and easy to find, as well as recycled computers and parts. NuBerryPi will compliment Peercoin's goal of providing energy efficient cryptocurrency without need for high end components like GPU's or dedicated mining hardware (ASIC's). 
If ASIC is term for dedicated and energy efficient mining, then this is ASIC of PoS.

