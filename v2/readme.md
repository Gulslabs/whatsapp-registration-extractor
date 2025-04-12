
### How to Run: 
- Copy Registrations to  `whatsapp_students_registration.txt`[Replace 'Gulam Ahsan' with '+91 9980700122']
- cd `D:\Work\py-ws\whatsapp-registration-extractor\v2` then Run `python .\parse_whatsapp_registrations.py`
- Open `parsed_students.csv` and edit as requird. 
#### Cleaning Values: 
##### 1. **Trimming Extra Spaces**
- **Example:**  `"  Syed Rahman  "` → `"Syed Rahman"`
##### 2. **Mobile Number Cleanup**
- **Applicable Fields:**  `Mobile#`, `Mobile#_2`, `WhatsApp#`. **Example:**  `"+91 90639 13264"` → `"9063913264"`
- **Strips leading country codes:**`+91`, `91` (India),  `+966`, `966` (Saudi Arabia), Case-insensitive and works with or without the `+` symbol. **Examples:** `"91 81234 56789"` → `"8123456789"` `"+966543219876"` → `"543219876"`
##### 3. **Camel Casing**
- **Applicable Fields:**  `Full Name`, `City`, `Area/Locality`, `District`, `State`, `Mandal`, `Profession` 
*(Includes `_2` variants like `City_2`, `Full Name_2`, etc.)*  **Example:**  
  `"mohammed iqbal"` → `"Mohammed Iqbal"`
##### 4. **Uppercasing**  
- **Applicable Fields:** `Student ID#`, `Batch#`. **Example:**   `"tsap-b01"` → `"TSAP-B01"`

##### 5. **Normalized**  
- Field names are **normalized** before checking against formatting rules (e.g., `"mobile"` is treated as `"Mobile#"`).
- The function is **non-destructive** for unlisted fields — no formatting is applied unless the field is explicitly configured.

#### Field Lable Mapping

| All Variants | Final Label |
|-------------|-------------|
| Mobile, Mobile# | Mobile# |
| WhatsApp, WhatsApp# | WhatsApp# |
| Email, Email Address | Email |
| Student ID, Student ID# | Student ID# |
| Batch, Batch# | Batch# |
| Gender | ❌ Remove |


#### Middle East and Gulf Country Calling Codes Removed. 

| Country | Country Code |
|---------|-------------|
| **Gulf Cooperation Council (GCC) Countries** ||
| India | +91 |
| Saudi Arabia | +966 |
| United Arab Emirates | +971 |
| Qatar | +974 |
| Kuwait | +965 |
| Bahrain | +973 |
| Oman | +968 |
| **Other Middle Eastern Countries** ||
| Egypt | +20 |
| Iran | +98 |
| Iraq | +964 |
| Israel | +972 |
| Jordan | +962 |
| Lebanon | +961 |
| Palestine | +970 |
| Syria | +963 |
| Turkey | +90 |
| Yemen | +967 |
