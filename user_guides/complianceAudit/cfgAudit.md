# Network Vista Compliance Audit

Log into Network Vista, open the menu (top left), select infra then Compliance Audit

<i>techTip: Some feature within the audit module are restricted root, admin and sudo admin users</i>


Before starting, please confirm that Network Vista is **Collect Configuration Db** enabled. 

![img.png](imgs/img.png)

Once confirmed and the Network Vista collection process has completed, following these steps

##### Menu Icons

![img_1.png](imgs/img_1.png) DashBoard Summary Page

![img_2.png](imgs/img_2.png) Table Results Page

![img_3.png](imgs/img_3.png) Device Level Results Page

![img_4.png](imgs/img_4.png) Input Device Variables

![img_5.png](imgs/img_5.png) Audit Template builder

![img_6.png](imgs/img_6.png) Template and Variable assignment


#### Audit Template builder

The Audit template build is where we create test templates which will be used to audit the configuration files.

![img_7.png](imgs/img_7.png)

In this example, I will be creating a test that will confirm that my NTP servers are set up correctly.

In this example, my template name is **ntpAudit**, and I am validating that **ntp server 1.1.1.1** is present across all devices. 
![img_8.png](imgs/img_8.png)

Once ready, click the save button ![img_10.png](imgs/img_10.png)

![img_9.png](imgs/img_9.png)

Next, click on Template and Variable assignment ![img_6.png](imgs/img_6.png)

![img_11.png](imgs/img_11.png)

Select the devices which should use this audit test template. In this example, all devices will be enabled.

<i>techTip: Click the filter button ![img_12.png](imgs/img_12.png) in the column to enable or disable all items within the column,
then to disable the filter, click ![img_13.png](imgs/img_13.png)</i>

![img_14.png](imgs/img_14.png)

If needed, this table can reverted back to the last save, click ** restore ** ![img_15.png](imgs/img_15.png)

![img_16.png](imgs/img_16.png)

Last step is to navigate to the Table Results Page ![img_2.png](imgs/img_2.png) and push the start arrow button ![img_17.png](imgs/img_17.png)

![img_18.png](imgs/img_18.png)

Results will be display once processing completes. 

Reading the result, 50% of the devices failed. This is due to these devices using a different NTP source **2.2.2.2**.
I could place another test under **ntpAudit** however, this would still result in a 50% failure. 

![img_19.png](imgs/img_19.png)

As expected

![img_20.png](imgs/img_20.png)

To resolve this, we must use regional vars. Regional Vars (or variables) are values which are swapped out depending on device locations. 

navigate to Input Device Variables ![img_4.png](imgs/img_4.png)

![img_21.png](imgs/img_21.png)

Start by unlocking the table ![img_22.png](imgs/img_22.png)

* varKey: a key (or name) which is used within the test audit template, **ntpOne**
* varRegion: the region in which the varKey resides, **emea**
* varValue: the value that will replace the varKey, **1.1.1.1**

To add another row, click ![img_23.png](imgs/img_23.png). To remove a row, click ![img_24.png](imgs/img_24.png) then the trash button on the row that needs to be removed ![img_25.png](imgs/img_25.png)

![img_26.png](imgs/img_26.png)

Once ready, click ![img_27.png](imgs/img_27.png) and Save ![img_28.png](imgs/img_28.png). Nagiavte back to the Audit Template builder ![img_5.png](imgs/img_5.png)

Remove the two existing tests by click the trash icon.

Instead of enter **ntp server 1.1.1.1**, this time I enter **ntp server {ntpOne}**. The top right information box will display errors. 

![img_30.png](imgs/img_30.png)

Click Save

![img_31.png](imgs/img_31.png)

Navigate back to the Template and Variable assignment ![img_6.png](imgs/img_6.png). 

NOTE: Since I removed the two existing audit tests <i>before</i> I added the new regional var rule, all devices were unassigned. 
To maintain assessment, it is best to add <i>then</i> remove audit tests. 

* emea will contain: r1,r2 & r3
* apac will contain: esw1, esw2 & esw3
* all devices will be assigned to the ntpAudit template

<i>techTip: devices can only be assigned to one region at a time but can belong to one or more audit templates</i>

![img_32.png](imgs/img_32.png)

Navigate back to the Table Results Page ![img_2.png](imgs/img_2.png) and restart the test.

everything is passing

![img_33.png](imgs/img_33.png)

Navigate back to the Device Level Results Page ![img_3.png](imgs/img_3.png)

![img_34.png](imgs/img_34.png)

We can see that the keyVar has been replaced with the keyValue.

Another useful feature of the compliance audit tool is if/when condition:

* if: strict match, must be present
* when: test condition one, if matched, then test condition two and/or three (if used)

Whenever a **when** statement is used, the logic that Network Vista will apply is, if the condition is not met, skip conditions two and three (if provided).

This does not affect the overall audit score of a device.

In this example, any device which has OSPF enabled must log adjacency changes (log-adjacency-changes)

![img_35.png](imgs/img_35.png)

![img_36.png](imgs/img_36.png)

Navigate back to the Table Results Page ![img_2.png](imgs/img_2.png) and restart the test.

![img_37.png](imgs/img_37.png)

Five Skips and One Pass, as expected

Click on the results icon ![img_39.png](imgs/img_39.png) to see device level results 

#### Summary View

Navigate back to the DashBoard Summary Page ![img_1.png](imgs/img_1.png)

![img_38.png](imgs/img_38.png)

<i>techTip: Each device summary ring is hyperlinked, click on the device to see a detail view of the audit results</i>



















