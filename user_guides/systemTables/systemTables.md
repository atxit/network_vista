# Network Vista System Tables

There are a number of Network Vista System tables which provide system level outputs such as collection results and logs. 

Log into Network Vista, open the menu (top left), select Root/Admin 

<i>techTip: Scheduler is only visible as root, admin and sudo admin user</i>

* Job Status: Realtime view of all the Network Vista jobs and processes

![img.png](imgs/img.png)

* Logs: Realtime view of all the Network Vista logs

![img_1.png](imgs/img_1.png)

* Collection Error: SSH collection results

Log into Network Vista, open the menu (top left), select Infra -> Collection Errors

![img_2.png](imgs/img_2.png)

* importTime: time of collection.
* importState: ok = ssh was successful, failed = SSH timed out.
* parsed: collected output is in the correct structure to be imported into the database.
* importStateFailed: SSH failure.
* noOutput; No output was detected from the show command.
* vrfNotFound: when using the dynamic vrf feature, no vrf found is displayed if no VRF where found (IOS only)
* string: Normal condition when found under **show running-config** or **show startup-config**

* DB Import Status: Database import results

Log into Network Vista, open the menu (top left), select Infra -> DB Import Status

![img_3.png](imgs/img_3.png)

Each column displays the total number of rows which were imported (per device, per show output).


