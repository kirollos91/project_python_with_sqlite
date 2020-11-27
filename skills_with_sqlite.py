# استدعاء الدالة
import sqlite3
# الاتصال بقاعدة البيانات
db = sqlite3.connect("app.db")
# استخدام دالة المؤشر 
cr = db.cursor()
# رقم المستخدم الافتراضى
uid = 0
# انشاء متغير يحتوى رسالة الاختيارات التى سوف تظهر فى بداية البرنامج
input_massage = """
what do you want to do?
"s" => show all skills,
"a" => add new skill,
"d" => delete skill,
"u" => update skill progress,
"q" => Quit the app.
choose option:
"""
# انشاء متغير ليحتوى على ماسوف يقوم بة المستخدم من الاختيار
user_input = input(input_massage).strip().lower()
# انشاء فائمة لوضع الاختيارات بداخلها 
commands_list = ["s","a","d","u","q"]
# التاكد من ان اختيار المستخدم من ضمن هذة القائمة او لا
# كتابة الدوال
# دالة حفظ البيانات و اغلاق قواعد البيانات
def commit_and_close():
    """commit changes and close connection to database"""
    # حفظ البيانات
    db.commit()
    # اغلاق قواعد البيانات
    db.close()
    # رسالة تظهر عند اغلاق قواعد البيانات
    print("Connection to database is closed")
# دالة اظهار البيانات
def show_skills():
    # كود الاستعلام عن البيانات
    cr.execute(f"select * from skills where user_id={uid}")
    # ارجاع جميع البيانات المستعلم عنها
    results = cr.fetchall()
    # طباعة رسالة بعدد المهارات للمستخدم
    print(f"you have {len(results)} skills.")
    # التاكيد على ان هذا المستخدم يملك على الاقل مهارة واحدة
    if len(results) > 0:
        # طباعة رسالة اظهار المهارات و النسبة لكل منهم
        print("showing skills with progress: ")
        # استخدام دالة التكرار لاظهار كل المهارات و النسب الخاصة بيهم لكل واحدة 
        for row in results:
            # الطباعة
            print(f"skill => {row[0]}",end=", ")
            print(f"progress => {row[1]}%")
    # استدعاء دالة الحفظ و اغلاق قواعد البيانات
    commit_and_close()

# دالة اضافة البيانات
def add_skill():
    # استقبال المهارة الجديدة من المستخدم
    sk = input("write skill name: ").strip().capitalize()
    # كود الاستعلام عن البيانات
    cr.execute(f"select name from skills where name = '{sk}' and user_id={uid}")
    # ارجاع جميع البيانات المستعلم عنها
    results = cr.fetchone()
    if results is not None:
        # طباعة رسالة بوجود هذة المهارة سابقا
        print(f"you have skill {results[0]} before")
    else:    
        # ستقبال النسبة المئوية من المستخدم
        prog = input("write skill progress: ").strip()
        # كود ادخال البيانات داخل قواعد البيانات جدول المهارات
        cr.execute(f"insert into skills(name,progress,user_id) values ('{sk}','{prog}',{uid})")
        # استدعاء دالة الحفظ و اغلاق قواعد البيانات
    commit_and_close()

# دالة خذف البيانات
def delete_skill():
    # استقبال المهارة التى يريد المستخدم حذفها
    sk = input("write skill name: ").strip().capitalize()
    # كود حذف المهارة من قواعد البيانات
    cr.execute(f"delete from skills where name = '{sk}' and user_id = {uid}")
    # استدعاء دالة الحفظ و اغلاق قواعد البيانات    
    commit_and_close()    

# دالة تعديل البيانات
def update_skill():
    # استقبال المهارة المراد تغيرها
    sk = input("write skill name: ").strip().capitalize()
    # كود الاستعلام عن البيانات
    cr.execute(f"select name from skills where name = '{sk}' and user_id={uid}")
    # ارجاع جميع البيانات المستعلم عنها
    results = cr.fetchone()
    # التاكد من ان هذة المهارة موجودة
    if results is not None:
        # استقبال القيمة الجديدة من النسبة المؤية
        prog = input("write the new skill progress: ").strip()
        # كود تعديل قيمة النسبة المؤية
        cr.execute(f"update skills set progress='{prog}' where name = '{sk}' and user_id= {uid}")
        # استدعاء دالة الحفظ و اغلاق قواعد البيانات
        commit_and_close()
    else:
        # استقبال من المستخدم اذا كان يريد اضافة هذة المهارة الجديدة
        if input("do you want to add this new skill? y/n: ").strip()[0] == "y":
            # استدعاء دالة اضافة المهارة
            add_skill()    
        else:
            # استدعاء دالة الخروج
            quit_app()

# دالة الخروج من البرنامج
def quit_app():
    # استدعاء دالة الحفظ و اغلاق قواعد البيانات
    commit_and_close()
    print("App is closed.")
    
# التحقق من وجود الاختيار فى القائمة
if user_input in commands_list:
    # رسالة ترجع ماقام المستخدم من اختيارة
    print(f"your choose is {user_input}")
    # استقبال رقم المستخدم
    uid = input("please enter user ID: ")
    # اذا كان الاختيار اظهر البيانات
    if user_input == "s":
        show_skills()
     # اذا كان الاختيار اضافة البيانات    
    elif user_input == "a":
        add_skill()
     # اذا كان الاختيار حذف البيانات
    elif user_input == "d":
        delete_skill()
     # اذا كان الاختيار تعديل البيانات
    elif user_input == "u":
        update_skill()        
     # اذا كان الاختيار الخروج من البرنامج
    else:
        quit_app()
 # اذا كان الاختيار غير صحيح
else:
    # رسالة للمستخدم تقول ان اختيارة لم يكن صحيحا
    print(f"your choosed {user_input} not fond in that chooses")    