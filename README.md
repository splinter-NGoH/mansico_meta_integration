## Mansico Meta Integration
![logo](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/4080cbd5-6f5f-48fe-877d-e28e5e795bf8)

This project is about syncing Facebook leads with ERPnext, When Clients fill Facebook ads instant forms app automatic fetch new created leads and create lead automatic in Lead doctype. Also on changing the Lead Status the new status sent to meta Pixel.


---

### How to Install

#### Frappe Cloud:

One-click installing available if you are hosting on FC from [here](https://frappecloud.com/marketplace/apps/mansico_meta_integration)

#### Self Hosting:

1. `bench get-app https://github.com/splinter-NGoH/mansico_meta_integration.git`
2. `bench --site [your.site.name] install-app mansico_meta_integration`
3. `bench --site [your.site.name] migrate`

---

## Facebook Requirements:

- Meta Business Account
  you have to create if not already having meta business account use this [link](https://www.facebook.com/business/help/1710077379203657?id=180505742745347) for help
- App Create Meta Business Settings
  to continue this tutorial u must create meta app following these steps:
![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/70138d92-07c2-4e05-8a6b-a408854a3900)

---

![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/9fd7cf1d-dbf1-42f1-8195-804a6c1038d8)

---

![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/3cb79346-2df9-468f-aeb9-fd86f4aa53d9)

---

![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/0019f6b9-83c5-48a7-bf55-ff66b5c6e405)


---

after creating your app go through Marketing Api Set up

![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/7b81826e-1ffe-46e7-9954-b7b38d522f8e)

---

- Access Tocken of admin System User
  after creating the app go back Meta settings > Users > System users > add

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/4b4bafec-78ad-4893-b365-1c2ced25f555)

  after user created u will be prompet to choose permissions make sure to check all check boxes also dont forget to include the app
  we created moment before and also allow all check boxes
  now there is a access token generated for you make sure to copy the token and past it in access token field in your system in Meta Facebook Settings

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/273d3c1b-766e-4bab-9b2e-fca3213b916b)

  if you already have admin System user just Generate new token and paste it in your System like image above.
  
---

- Pixel ID
- Pixel Access Token
  to get your pixel id and access token got to Events Manger

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/ab602583-2c5c-4682-b85d-5a1dc49c0c58)

  ---

  from left menu choose
  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/1d43af36-24fa-4f58-b960-5cfe93e76393)

  now create and connect your crm

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/0ce3ad11-4b76-4024-a37a-4d64eb8d7884)

  NOW continue setup your pixel CRM

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/0a5dec15-c93f-4f3c-bd93-4b430f6d279a)

  from menu choose Learn how

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/80308a38-81e8-4376-a381-d03b7d0ad71a)

  in Create endpoint section
  Generate  Access Token

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/8dd287ee-4903-4285-9ba4-2808a7827aa9)

  then paste it in your system

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/eeab771d-f32e-4cc4-9f41-fd44311d2114)

  also get the pixel id and paste it in system

  ![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/ca090b9a-1cb7-4037-a221-de733f571b54)


---

Now you almost Ready 

now fill the api url and graph api version like img below 

![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/d802a857-7807-4cd6-ae4e-cef10466816a)


---

now go to Page ID doctype and add you page name and id 

![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/164bbb69-9539-4579-a7bf-568d91c74bcc)


now go too  New Read By 

and add 
![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/ed73238f-a54b-4c67-a515-f3d0d23f9072)


`All Leads` as img above make sure you spell it right

---

Finally got to sync new add 

and create new sync

![image](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/4cbc636a-181b-483d-9e25-7bc15cf9c5dd)

after saving and submit it will fetch all current available forms and make schedule job depends on the Event Frequency you choose to fetch and create new leads for every interval you choos 

![datad](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/15e25a56-9c67-4df3-ac51-c10d58424912)

---

Now your job is queued 

![datad](https://github.com/splinter-NGoH/mansico_meta_integration/assets/73743592/f822733d-4c45-49b6-8ad9-fd8bbe30d09e)

---

### Dependencies:

- [Frappe](https://github.com/frappe/frappe)
- [Erpnext](https://github.com/frappe/erpnext)

---

### License

MIT

---

### Very Important Note

This app will be having new updates as soon as possible also dont forget to star the repo
Pull requests from Developers are very Welcome
Hope you guys have another day of solving bugs 
Cheers from Mansy!
