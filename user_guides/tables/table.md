# Table Data

Once Network Vista has collected and structured the data, it is placed into tables and made available through the UI or API.
The number of displayed rows is 20, however, this can be adjusted by using the row selector. 

### Query

To query, simply enter a value which you are searching for. In this example, I am looking for all OSPF neigbors on host r3

![img.png](imgs/img.png)

Click the filter button ![img_14.png](imgs/img_14.png) found on the right side of each column

![img_1.png](imgs/img_1.png)

To further refine a search, continue to add by filtering values in each of the column fields. I enter 180.3.3.3 and click the filter button.

![img_2.png](imgs/img_2.png)

By default, the standard query method uses a lookup of value "contains". Querying data is case-sensitive. 
To change the behaviour from value contains to either starts with or ends with, use the following regex characters:

* ^ for starts with
* $ for ends with

![img_15.png](imgs/img_15.png)

![img_16.png](imgs/img_16.png)

### Hiding columns
To temporarily hide a column, select the column menu button 
![img_3.png](imgs/img_3.png). The icon will display red when enabled![img_4.png](imgs/img_4.png), then select the ![img_5.png](imgs/img_5.png) icon. 

The column will remain hidden until you leave the page.

![img_6.png](imgs/img_6.png)

Remove all filters to see the full table. 

![img_7.png](imgs/img_7.png)

click ![img_8.png](imgs/img_8.png), the column will reappear.

### Changing column order & columns selection

By default, all table columns are displayed. For some tables, this could result in over 20 columns of data being displayed. 

To filter out unwanted columns, click on the top main menu filter button ![img_9.png](imgs/img_9.png)

A table column selector page will be displayed

![img_10.png](imgs/img_10.png)

Simply move the column name from Selected -> Selectable to hide the column. 

![img_11.png](imgs/img_11.png)

Alternately, move columns from Selectable -> Selected to make visable again.

To change the order of the table, highlight the column name in the Selected column and use the arrows to adjsut the position

![img_12.png](imgs/img_12.png)

Once ready, click Save. The table will update then click Close. 

![img_13.png](imgs/img_13.png)






