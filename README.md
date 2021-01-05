# Analysis of Building Permits For Vaughan

Authors: [Freda Xin](www.linkedin.com/in/freda-xin/), [Wayne Chan](https://www.linkedin.com/in/waynechan-cma/)

---
## Library Contents

1. [Data Cleaning Part
I](https://github.com/FredaXin/project_vaughan/blob/main/data_cleaning.py)  
2. [Data Cleaning Part
II](https://github.com/FredaXin/project_vaughan/blob/main/data_cleaning_1.py)  
3. [Data Cleaning Part
III](https://github.com/FredaXin/project_vaughan/blob/main/data_cleaning_2.py) 
4. [Web-scraping code for StatCan](https://github.com/FredaXin/project_vaughan/blob/main/scraper_statcan.py)
5. [EDA and Feature Engineering
   code](https://github.com/FredaXin/project_vaughan/blob/main/eda.ipynb)  



---
## Objective
Our client, the City of Vaughan, provided us with the
Building Permits data in Canada from 2000 to 2019. The goal of this project is
to synthesize and interpret the data, and to identify any trends showcasing
Vaughan’s growth for marketing purposes and to attract investments.  

The most challenging and time-consuming part of this process is data cleaning. To solve challenges and to
automate the data cleaning process, we built a custom Python library. 

The following sections of the README will focus on the mechanism of the custom
Python library. For key findings of this project, please see  the PPT in the
[link](https://docs.google.com/presentation/d/1zjLx8IJUHk1ILf2BKMBMqEbVAtviD5W3aG89NV7ENkI/edit?usp=sharing). 


---
## Background

### Issues of the Source Data:  

#### Issue 1: 
Complex and overly formatted data in Excel: the source data was formatted in hierarchical structures that needs to be flattened and transformed into tubular
structures.

#### Issue 2:
Format inconsistency between years: the formats and structures of the source data varies between years. 

#### Issue 3:
Naming issues for geographical divisions (names are not unique). For example:  
• Hamilton, Windsor, Victoria exist in multiple provinces  
• Toronto could refer to the CD or the CSD  
• The same city could appear on multiple rows due to municipality designation changing (eg. Markham)  

### Our goal:
• To turn the source data into flattened structure (i.e. tabular structure) so
that other platforms, such as Tableau or Pandas, can process it.  
• To automate this process so that the result is reliable and reproducible.

---
## Mechanism
1. [Data Cleaning Part
I](https://github.com/FredaXin/project_vaughan/blob/main/data_cleaning.py)  
• Address [Issue 1](#Issue-1)   
• Use the Python Standard Library   
• Search the source data for the CSDs of interests    
• Reconstruct the selected CSD into tabular structure

2. [Data Cleaning Part
II](https://github.com/FredaXin/project_vaughan/blob/main/data_cleaning_1.py)  
Fine tune the data cleaning process and 
3. Combine the Building Permits data with Census data 
4. Feature engineering to add calculated fields 



---
## References

• [2016 and 2011 censuses](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/hlt-fst/pd-pl/Table.cfm?Lang=Eng&T=307&SR=1&S=3&O=D&RPP=9999&PR=0)

• [2011 and 2006 censuses](https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/Table-Tableau.cfm?LANG=Eng&T=307&SR=1&S=11&O=A&RPP=9999&PR=0&CMA=0)

• [2006 and 2001 censuses](https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/hlt/97-550/Index.cfm?TPL=P1C&Page=RETR&LANG=Eng&T=307&S=3&O=D&RPP=699)

• [StatCan Example of Analysis of Building Permits](https://www150.statcan.gc.ca/n1/daily-quotidien/201001/dq201001a-eng.htm)