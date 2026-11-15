SARAH STORE WEBSITE STARTER
==========================

អ្វីដែលមានក្នុងឯកសារនេះ
- គេហទំព័រ Flask សាកល្បង ជាភាសាខ្មែរ
- ទំព័រដើម និងហ្គេម ៤ ប្រភេទ
- ជ្រើសរើសកញ្ចប់ និងបញ្ចូលព័ត៌មានគណនី
- រក្សាទុកការបញ្ជាទិញក្នុង SQLite
- ទំព័រមើលការបញ្ជាទិញ និងផ្ទាំង Admin សាកល្បង

សំខាន់៖ នេះមិនទាន់ជាប្រព័ន្ធលក់ពិតប្រាកដទេ។
- មិនទាន់ភ្ជាប់ ABA PayWay / KHQR
- មិនទាន់មានការផ្ទៀងផ្ទាត់ការបង់ប្រាក់
- មិនទាន់ភ្ជាប់ Reseller API ឬការបញ្ចូលហ្គេមស្វ័យប្រវត្តិ
- Account lookup មិនទាន់ភ្ជាប់ API
- /admin មិនទាន់មាន Login និងមិនត្រូវបើកជាសាធារណៈ

របៀបដំណើរការលើ Windows
1. ដំឡើង Python 3.11 ឬថ្មីជាងនេះ។
2. Extract ZIP ទៅ Desktop។
3. បើក Folder នេះក្នុង VS Code។
4. បើក Terminal នៅក្នុង VS Code ហើយដំណើរការ៖

   py -m venv .venv
   .venv\Scripts\activate
   py -m pip install -r requirements.txt
   py app.py

5. បើក Browser ទៅ៖ http://127.0.0.1:5000

កែតម្លៃ
- បើក app.py
- រក GAMES នៅខាងលើ
- កែ packages និងតម្លៃតាមផលិតផលពិតរបស់អ្នក

មុនដាក់ Online
- បន្ថែម Admin login និងការពារសុវត្ថិភាព
- កំណត់ FLASK_SECRET_KEY ថ្មី
- ភ្ជាប់ ABA PayWay តាមឯកសារផ្លូវការ និងតេស្ត callback/signature
- ភ្ជាប់ Reseller API តាមឯកសាររបស់អ្នកផ្គត់ផ្គង់
- បន្ថែម account lookup តាម API ដែលអនុញ្ញាត
- កុំដាក់ API key ឬ secret នៅក្នុង frontend ឬ GitHub

Contact placeholder: @sarah168hd
