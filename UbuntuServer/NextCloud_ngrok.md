Install and configure Nextcloud on your Ubuntu 24.04 server, including resolving issues with untrusted domains.

---

# Detailed Documentation for Installing and Configuring Nextcloud on Ubuntu 24.04

## Step 1: Update Your System
First, ensure your system packages are up to date. This is crucial for security and stability.

```bash
# Update the package list to get information on the newest versions of packages and their dependencies
sudo apt update

# Upgrade all the installed packages to their latest versions
sudo apt upgrade -y
```

## Step 2: Install Required Packages
Nextcloud requires a web server, database server, and PHP. We'll use Apache, MariaDB, and PHP.

### Install Apache (Web Server)
Apache will serve the Nextcloud web interface.

```bash
# Install Apache web server
sudo apt install apache2 -y
```

### Install MariaDB (Database Server)
MariaDB will store Nextcloud's data.

```bash
# Install MariaDB database server
sudo apt install mariadb-server -y
```

### Secure MariaDB
Run the MariaDB secure installation script to improve security by setting a root password and disabling insecure defaults.

```bash
# Secure the MariaDB installation
sudo mysql_secure_installation
```
Follow the prompts to set the root password and secure your installation.

### Add the Ondrej PHP PPA
To get the latest PHP versions, add the Ondrej PHP PPA.

```bash
# Install software-properties-common to manage PPAs
sudo apt install software-properties-common -y

# Add the Ondrej PHP PPA
sudo add-apt-repository ppa:ondrej/php -y

# Update the package list to include the new PPA
sudo apt update
```

### Install PHP and Required Modules
Nextcloud requires several PHP modules. We will install PHP 8.1 (or the latest version available).

```bash
# Install PHP and required PHP modules
sudo apt install libapache2-mod-php php8.1 php8.1-gd php8.1-mysql php8.1-curl php8.1-xml php8.1-mbstring php8.1-zip php8.1-intl php8.1-bcmath php8.1-gmp -y
```

## Step 3: Configure MariaDB for Nextcloud
Create a database and user for Nextcloud.

### Log in to the MariaDB shell
```bash
# Log in to the MariaDB shell as root
sudo mysql -u root -p
```
Enter the root password you set during the secure installation.

### Create the Database and User
Inside the MariaDB shell, run the following commands:

```sql
-- Create a database named 'nextcloud'
CREATE DATABASE nextcloud;

-- Create a user 'nextclouduser' with a strong password
CREATE USER 'nextclouduser'@'localhost' IDENTIFIED BY 'your_password';

-- Grant all privileges on the 'nextcloud' database to 'nextclouduser'
GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextclouduser'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

-- Exit the MariaDB shell
EXIT;
```

## Step 4: Download and Extract Nextcloud
Download the latest version of Nextcloud from the official website.

```bash
# Change to the /var/www directory
cd /var/www/

# Download Nextcloud
sudo wget https://download.nextcloud.com/server/releases/nextcloud-24.0.0.zip

# Install unzip if not already installed
sudo apt install unzip -y

# Unzip the downloaded Nextcloud archive
sudo unzip nextcloud-24.0.0.zip

# Change ownership of the Nextcloud files to the Apache user
sudo chown -R www-data:www-data nextcloud

# Set the correct permissions
sudo chmod -R 755 nextcloud
```

## Step 5: Configure Apache for Nextcloud
Create a new configuration file for Nextcloud.

### Create the Configuration File
```bash
# Create and edit the Nextcloud Apache configuration file
sudo nano /etc/apache2/sites-available/nextcloud.conf
```

### Add the Following Content
Replace `your_domain_or_IP` with your server's IP address or domain name.

```apache
<VirtualHost *:80>
    DocumentRoot /var/www/nextcloud/
    ServerName your_domain_or_IP

    <Directory /var/www/nextcloud/>
        Options +FollowSymlinks
        AllowOverride All

        <IfModule mod_dav.c>
            Dav off
        </IfModule>

        SetEnv HOME /var/www/nextcloud
        SetEnv HTTP_HOME /var/www/nextcloud
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/nextcloud_error.log
    CustomLog ${APACHE_LOG_DIR}/nextcloud_access.log combined
</VirtualHost>
```

### Enable the Nextcloud Site and Required Apache Modules
```bash
# Disable the default site to avoid conflicts
sudo a2dissite 000-default.conf

# Enable the Nextcloud site
sudo a2ensite nextcloud.conf

# Enable required Apache modules
sudo a2enmod rewrite headers env dir mime

# Restart Apache to apply the changes
sudo systemctl restart apache2
```

## Step 6: Set the ServerName Globally
Resolve the warning about the server's fully qualified domain name by setting the `ServerName` directive globally.

```bash
# Edit the main Apache configuration file
sudo nano /etc/apache2/apache2.conf
```

Add the following line at the end of the file:

```apache
ServerName localhost
```

Save and exit the file (Ctrl+O, Enter, Ctrl+X), then restart Apache.

```bash
# Restart Apache to apply the changes
sudo systemctl restart apache2
```

## Step 7: Complete the Installation via Web Interface
Open your web browser and navigate to `http://your_domain_or_IP`. Follow the on-screen instructions to complete the installation. Enter the database details as follows:

- **Database user**: `nextclouduser`
- **Database password**: `your_password`
- **Database name**: `nextcloud`
- **Database host**: `localhost`

## Step 8: Troubleshoot Database Connection Issue
If you encounter an error regarding database connection (e.g., "Failed to connect to the database"), ensure that the database user has the correct permissions and that the correct credentials are used during setup.

### Verify Database User Permissions
1. Log in to the MariaDB shell:

```bash
# Log in to the MariaDB shell as root
sudo mysql -u root -p
```

2. In the MariaDB shell, run the following commands:

```sql
-- Check if the user nextclouduser exists
SELECT User, Host FROM mysql.user WHERE User = 'nextclouduser';

-- If nextclouduser exists, grant all privileges
GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextclouduser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Ensure Correct Database Configuration During Nextcloud Setup
During the Nextcloud setup, make sure you are using the correct database credentials. Use the following details:

- **Database user**: `nextclouduser`
- **Database password**: `your_password`
- **Database name**: `nextcloud`
- **Database host**: `localhost`

### Verify Database User Password
Ensure that the password for `nextclouduser` is correct. Reset the password if needed:

1. Log in to MariaDB:

```bash
# Log in to the MariaDB shell as root
sudo mysql -u root -p
```

2. Reset the password:

```sql
-- Reset the password for nextclouduser
ALTER USER 'nextclouduser'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
EXIT;
```

### Remove Old Nextcloud Data (Optional)
If the previous setup attempt created any partial data, clean it up before trying again:

1. Remove the existing Nextcloud data directory:

```bash
# Remove the existing Nextcloud data directory
sudo rm -rf /var/www/nextcloud/data
```

2. Create a new data directory:

```bash
# Create a new Nextcloud data directory
sudo mkdir /var/www/nextcloud/data

# Change ownership to the Apache user
sudo chown -R www-data:www-data /var/www/nextcloud/data

# Set the correct permissions
sudo chmod -R 755 /var/www/nextcloud/data
```

### Restart Apache
Restart Apache to ensure all changes are applied:

```bash
# Restart Apache
sudo systemctl restart apache2
```

### Retry the Installation
Open your web browser and navigate to `http://your_domain_or_IP`. Enter the database details as follows:

- **Database user**: `nextclouduser`
- **Database password**: `your_password`
- **Database name**: `nextcloud`
- **Database host**: `localhost`

Proceed with the installation. If everything is configured correctly, the installation should proceed without any errors.

## Step 9: Accessing Nextcloud Remotely Using Ngrok
If you have a CGNAT internet IP address, you can use Ngrok to access Nextcloud remotely.

### Install Ngrok
```bash
# Download the latest version of Ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz

# Unzip the Ngrok package
tar -xvf ngrok-v3-stable-linux-amd64.tgz

# Move Ngrok to a directory in your PATH
sudo

 mv ngrok /usr/local/bin/ngrok
```

### Set Up Ngrok with Your Authtoken
Set up Ngrok with your authtoken:

```bash
# Set up Ngrok with your authtoken
ngrok authtoken YOUR_AUTHTOKEN
```
Replace `YOUR_AUTHTOKEN` with your actual authtoken.

### Start Ngrok
Start an Ngrok tunnel:

```bash
# Start an Ngrok tunnel to expose port 80
ngrok http 80
```
This will provide you with a public URL that you can use to access your local server from anywhere. For example: `https://XXXXXXXXXXXXXXXXXXXX-free.app`.

## Step 10: Configure Trusted Domains
If you encounter the "Access through untrusted domain" error, add the Ngrok URL to the `trusted_domains` array in Nextcloud's configuration file.

### Edit the `config.php` File
```bash
# Edit the Nextcloud configuration file
sudo nano /var/www/nextcloud/config/config.php
```

### Add the Ngrok URL to `trusted_domains`
Add your Ngrok URL to the `trusted_domains` array:

```php
'trusted_domains' =>
array (
  0 => 'localhost',
  1 => '192.168.1.101',
  2 => 'XXXXXXXXXXXXXXXXXXXX.ngrok-free.app',
),
```

### Save and Exit
Save the changes and exit the editor. If you are using `nano`, you can do this by pressing `Ctrl+O`, then `Enter` to save, and `Ctrl+X` to exit.

### Restart Apache
Restart Apache to apply the changes:

```bash
# Restart Apache
sudo systemctl restart apache2
```

### Access Nextcloud
Open your web browser and navigate to your Ngrok URL: `https://XXXXXXXXXXXXXXXXXXXX.ngrok-free.app`.

---
