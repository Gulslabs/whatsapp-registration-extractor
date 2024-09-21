# WhatsApp to CSV Generator 
- All registrations are pushed to a Whatsapp group.
- All message of registration follow a particular format(`sample below`).
- *Problem Statement*: Extract registration messages; then extract all the fields from every such message and push it as rows on a csv file(`sample below`)
### Prerequisite:
- Step 0: Installations    
    - Virtual Environment for Python in VSCode https://code.visualstudio.com/docs/python/environments
    - Install pandas `pip install pandas`
      
### How to Run:
- Step 1: Download the chats
    -Select the class registration group you want to export messages from; tap three dots(...) on top right corner; go to more and "Export Chat". Choose *Not to include media*
- Step 2: Replace
    - In the downloaded file
        - Replace all `——————————————` with `------------------------------`; this will ensure UTF-8 encoding gets applied correctly.
        - Replace all `———` with `---` and `__` with `--`
        - Replace all `Email Address`, `EmailAddress` with `Email`
        - Replace all `REFFERRED` with `REFERRED`
- Step 3: Execution
    - Run `python.exe WhtAppTxt-To-RegFrm-Extractor.py`. Update the source file reference as required. This will generate `KARMH-B02_Registrations.txt`. Replace all `*KARMH-B02 STUDENT DETAILS*` with `KARMH-B02 STUDENT DETAILS`
    - Run `python.exe RegFrm-To-Csv-Convertor.py`. Update the source file reference as required. This will generate `KARMH-B02_Registrations.csv`. The generated csv file will have some analomolies. 
    - Finally run `python.exe RegFrm-Csv-Cleansing.py`; this will cleans empty rows, remove phone number and other anamolies
### Formats:

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
```
Full Name,Mobile#,WhatsApp#,Gender,HOMETOWN DETAILS - Area/Locality,HOMETOWN DETAILS - City,HOMETOWN DETAILS - District,HOMETOWN DETAILS - State,CURRENT RESIDENCE - Area/Locality,CURRENT RESIDENCE - City,CURRENT RESIDENCE - District,CURRENT RESIDENCE - State,OTHER DETAILS - Age,OTHER DETAILS - Qualification,OTHER DETAILS - Profession,OTHER DETAILS - Email,REFERRED By - Full Name,REFERRED By - Mobile#,REFERRED By - Student ID#,REFERRED By - Batch#,REFERRED By - Mobile,REFERRED By - Student ID,REFERRED By - Batch
Syed Thaseemuddin,1234567890,1234567890,M,Kirmani Colony,Bidar,Bidar,Karnataka,HSR Layout,Bengaluru,Bengaluru,Karnataka,42,"M.S,  B.E",Engineering Manager,st@gmail.com,GA,1234567890,259_Ahsan,NB-02
```
