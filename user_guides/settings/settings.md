# Settings

*techTip: Settings is only visible to root, admin, and sudo admin users*

Log into Network Vista, open the menu (top left), and select **Settings**:

![img.png](imgs/img.png)

#### System Administrator

In addition to the Network Vista root account, there is also an admin account. To enable the admin user account, 
add a password with a minimum length of eight characters. Once set, click **Save**.

![img_1.png](imgs/img_1.png)

#### Sudo Administrators

Sudo Admin Users are standard users with elevated rights. Network Vista employs Role-Based Access Control (RBAC) for certain functions, such as making changes. 
To grant access, add the user’s ID to one of the three input fields and click **Save**

![img_2.png](imgs/img_2.png)

#### Static Users

Static users are accounts that can be created to access Network Vista. By default, static users are standard users unless elevated to Sudo Administrators.
Enter the user ID in the field and select **Save**. 

![img_3.png](imgs/img_3.png)

<i>techTip: Network Vista supports LDAP integration, in addition to static users</i>

![img_4.png](imgs/img_4.png)

Please provide the 'registrationId' to the user and have then following the new user guide. Once registered, the 'registrationStatus' will change from 'unregistered' to 'registrationComplete' (the registrationCode will disappear) 

![img_5.png](imgs/img_5.png)

To remove a user, click the remove (trash) icon. 

#### Static Device Management

There are two methods to import devices into Network Vista: 

1) through the API, or;
2) upload using a .csv file

For a lab or a demo environment, using the static method would be the easiest approach.

To add a device or set of devices, click on the 'choose file' button. 

<i>techTip: The .csv file must contain the following columns:</i>

![img_6.png](imgs/img_6.png)

Once ready, click upload

![img_7.png](imgs/img_7.png)

To remove all static devices, click 'remove table'. 

To view the imported device table, navigate to the infra/device tab (once the infra menu has been activated)

![img.png](imgs/img_20.png)

#### Infrastructure SSH Access

To enable the SSH collection process, a username and password is required. The SSH password is encrypted by the vault seed password found in the system.yml file.  

Once ready, click 'Save Credentials'. 

<i>techTip: Read Only Password is recommended.</i>

<i>techTip: Once a SSH username and password has been saved, the infra menu will be activated.</i>

#### Concurrent VTY & SSH Sessions

Network Vista has been designed for rapid data collection. Use the 'Concurrent 
VTY Sessions' and 'Concurrent SSH Sessions' selection inputs to adjust the following options:

Concurrent VTY Sessions: 

number of active session PER Device

* One Vty Sessions
* Three Vty Sessions
* Five Vty Sessions

Concurrent SSH Sessions: 

the total number of concurrent collections

* 30 Device Sessions
* 60 Device Sessions
* 90 Device Sessions

#### Network Vista Managed Databases

Network Vista has a small number of purpose built databases which can be enabled or disabled within the settings module.

* To enable the collection of the configuration DBs, select the 'Collect Configuration Db' option
* To enable Network Vista to compare the running configuration file against the startup, select the 'Running CFG vs StartUp CFG' option
* To enable Network Vista to collect and enrich inventory data, select the 'Collect Inventory Db' option

<i>techTip: Running CFG vs StartUp CFG requires Collect Configuration Db</i>

#### Network Vista API Keys

To enable the Network Vista API interface, please following the following steps. 

To generate a readWrite API key, click the 'Request Read Write' button
To generate a readOnly API key, click the 'Request Read Only' button

Warning: Any stored keys will be replaced. 

![img_23.png](imgs/img_23.png)

Click 'Yes' to proceed or 'No'

![img_21.png](imgs/img_21.png)

The new API key will appear for 15 seconds. Click on the API key, this will save it to the clipboard. Save the API key in a 
secure location as it can never to viewed again.

![img_24.png](imgs/img_24.png)

#### Meraki API Key

To enable the Meraki collection process, please enter a valid Meraki key. Just like the SSH password, read only is recommended. 

Once ready, click **'Test and Save'**. If successful, the Meraki menu will be activated. 
<i>techTip: If there is a Meraki organisation that should not be included, enter the organisation Id (numbers only)</i>

![img_8.png](imgs/img_8.png)

#### LDAP

To enable LDAP integration, please enter the following information:

* LDAP IP or DNS Name: The LDAP server or VIP.
* Match on Attr: The attribute to match on (e.g., ou).
* Bind DN: The location of the user search (e.g., uid=username,ou=users,dc=example,dc=org).
* Group User Membership: Access to Network Vista is granted when one or more groups are matched.
* LDAP Admin Group: When matched, the user is granted admin access.
* Test Username and Test Password: Runs a test using the provided information. 


If successful, LDAP is enabled across the platform.

Click **'Test & Save'**

![img_9.png](imgs/img_9.png)

#### Data Retention Policy

Defines the amount of time before stored logs messages will be removed. 

Diff Log Retention: 

* One Month
* Three Months
* Five Months

System Log Retention:

* One Month
* Two Months
* Three Months
* Four Months
* Five Months

![img_10.png](imgs/img_10.png)






