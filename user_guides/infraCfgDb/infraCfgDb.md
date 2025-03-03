# Infra Configuration DB

Log into Network Vista, open the menu (top left), and select **infra** then **Databases** and **cfgDb**:

![img.png](imgs/img.png)

The infra configuration DB is similar to any other Network Vista database however, the input parser has been 
custom-built to preserve the tree like structure of a standard configuration file. Whenever a branch or branch of branch 
appears within the configuration file, Network Vista indents the output into the next column. This allows for better searching and slicing of data queries. 

<i>Note: any column that contains no output will be automatically closed</i>

Example, searching **ntp server** under column zero (the root column)

![img_1.png](imgs/img_1.png)

then refining the query to include only **r3**

![img_2.png](imgs/img_2.png)

#### Extracting the Configuration file

To download a copy of a device configuration file, enter the name of the device in the download field found in the main navigation bar

![img_3.png](imgs/img_3.png)

Click ![img_4.png](imgs/img_4.png) and Network Vista will download a copy of the file

![img_5.png](imgs/img_5.png)

![img_6.png](imgs/img_6.png)

To download a copy of the viewable table, click ![img_9.png](imgs/img_9.png)

![img_8.png](imgs/img_8.png)

![img_10.png](imgs/img_10.png)

#### Config Diffs

To access the **config diffs**, click ![img_7.png](imgs/img_7.png), the past Seven days of Diffs will be displayed.

<i>Note: unlikely regular Network Vista Diff tables, it is not possible to select and group diff's. Diff changes are automatically assigned to groupBy values</i>

#### Diff's in action

![img_12.png](imgs/img_12.png)

Example, added new loopback interface

![img_11.png](imgs/img_11.png)

New Loopback interface displayed in **Green**

![img_13.png](imgs/img_13.png)






