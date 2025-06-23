### TꓘT modprobed.db repository
This is where we do our `modprobed.db` work for our [TꓘT](https://github.com/The-Kernel-Toolkit/TKT) kernel build system.

Our goal is is a very simple project;

```
Build a simple database from current Linux users, across distros, running generic brand distro based kernels.
With this list we can build a hardware database of the current generic modules in use by current Linux users.
This will help us make our tailored, slimmed down, generic-like build kernels for the TꓘT project.
```

## Contribute Your Kernel Module Data

Help make this project smarter for everyone by contributing your system’s module usage! We're building a generic module list that covers the most common real-world hardware - your input matters.

## Contribute Your Kernel Module Data (via lsmod - the easy method)

Open a terminal shell and run the following command to export your loaded modules into a file that you can submit to us.

```bash
lsmod | awk 'NR>1 {print $1}' | sort -u > ~/Desktop/$(hostname)-TKT-modules-list.txt
```

## Contribute Your Kernel Module Data (via modprobed-db - the preferred method - long game)

### Step 1: Install modprobed-db

Package manager based:

`sudo <your-package-manager install> modprobed-db`

### Step 2: Setup and Enable the Logging Job

Start logging every module that gets used on boot or when you load something manually:

`modprobed-db init`

Enable the systemd service to run on every boot:

`sudo systemctl enable --now modprobed-db.service`

Let it run for a few days or just during your regular use—boot into different environments, use hardware, peripherals, Wi-Fi, audio, USB, etc. The goal is to build a rich database of your system's actual module usage.

### Step 3: Send Us Your Data

Once you've built up some history:

`modprobed-db dump > ~/Desktop/$(hostname)-TKT-modules-list.txt`

Then send us the '.txt' file via a pull request. Add system details if you can (laptop/desktop, CPU/GPU, distro)—that context helps!
