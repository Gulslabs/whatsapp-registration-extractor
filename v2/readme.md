
### How to Run: 
- Copy Registrations to  `whatsapp_students_registration.txt`[Replace `Gulam Ahsan` with `+91 9980700122`]
- cd `D:\Work\py-ws\whatsapp-registration-extractor\v2` then Run `python .\parse_whatsapp_registrations.py`
- Open `parsed_students.csv` and edit as requird. 
#### Cleaning Values: 
##### 1. **Trimming Extra Spaces**
- **Example:**  `"  Syed Rahman  "` → `"Syed Rahman"`
##### 2. **Mobile Number Cleanup**
- **Applicable Fields:**  `Mobile#`, `Mobile#_2`, `WhatsApp#`. **Example:**  `"+91 90639 13264"` → `"9063913264"`
- **Strips leading country codes:**`+91`, `91` (India),  `+966`, `966` (Saudi Arabia), `+1`, `1`(USA) Case-insensitive and works with or without the `+` symbol. **Examples:** `"91 81234 56789"` → `"8123456789"` `"+966543219876"` → `"543219876"`
##### 3. **Camel Casing**
- **Applicable Fields:**  `Full Name`, `City`, `Area/Locality`, `District`, `State`, `Mandal`, `Profession` 
*(Includes `_2` variants like `City_2`, `Full Name_2`, etc.)*  **Example:**  
  `"mohammed iqbal"` → `"Mohammed Iqbal"`
##### 4. **Uppercasing**  
- **Applicable Fields:** `Student ID#`, `Batch#`. **Example:**   `"tsap-b01"` → `"TSAP-B01"`

##### 5. **Normalized**  
- Field names are **normalized** before checking against formatting rules (e.g., `"mobile"` is treated as `"Mobile#"`).

#### Field Lable Mapping

| All Variants | Final Label |
|-------------|-------------|
| Mobile, Mobile# | Mobile# |
| WhatsApp, WhatsApp# | WhatsApp# |
| Email, Email Address | Email |
| Student ID, Student ID# | Student ID# |
| Batch, Batch# | Batch# |
| Gender | ❌ Remove |
