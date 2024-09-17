# WhatsApp to CSV Generator 
We have a whatsapp group for class registration. All message for registration follow a particular format(`sample below`). We need to extract all the fields from every such message and push them as rows on a final csv file(`sample below`)
### Prerequisite:
- Step 0: Installations
    - Install pandas `pip install pandas`
    - Virtual Environment for Python in VSCode https://code.visualstudio.com/docs/python/environments
### How to Run:
- Step 1: Download the chats
    -Select the class registration group you want to export messages from; tap three dots(...) on top right corner; go to more and "Export Chat". Choose *Not to include media*
- Step 2: Replace
    - In the downloaded file Replace all `——————————————` with `------------------------------`; this will ensure UTF-8 encoding gets applied correctly. And replace all `———` with `---` and `__` with `--`
    - Replace all `Email Address`, `EmailAddress` with `Email`
    - Replace all `REFFERRED` with `REFERRED`
- Step 3: Execution
    -Run `python.exe WhtAppTxt-To-RegFrm-Extractor.py`. Update the source file reference as required. This will generate `KARMH-B02_Registrations.txt`. Replace all `*KARMH-B02 STUDENT DETAILS*` with `KARMH-B02 STUDENT DETAILS`
    - Run `python.exe RegFrm-To-Csv-Convertor.py`. Update the source file reference as required. This will generate `KARMH-B02_Registrations.csv`. The generated csv file will have some analomolies. 
    - Finally run `python.exe RegFrm-Csv-Cleansing.py`; this will cleans empty rows, remove phone number and other anamolies
### Format:

```
=====================
KARMH-B02 STUDENT DETAILS
=====================
Full Name : 
Mobile# : 
WhatsApp# : 
Gender : 
——————————————	
HOMETOWN DETAILS
Area/Locality : 
City : 
District : 
State : 
——————————————	
CURRENT RESIDENCE
Area/Locality : 
City : 
District : 
State : 
——————————————	
OTHER DETAILS
Age : 
Qualification : 
Profession : 
Email Address : 
——————————————	
REFERRED By
Full Name : 
Mobile# : 
Student ID# : 
Batch# : 
=====================
```
