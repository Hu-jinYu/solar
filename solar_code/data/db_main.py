import db_table as d
if __name__=="__main__":
    create_table1=d.Chat()
    create_table2=d.UserInfoManager()
    create_table3=d.ReminderManager()
    create_table4=d.PersonaManager()

    # create_table1._create_table()
    # create_table2._create_table()
    # create_table3._create_table()
    # create_table4._create_table()

    # create_table1.create_chat("123","user","2025,一战成名!")
    # create_table2.create_user("李华","男","2002-09-12")
    # create_table3.create_reminder("爬山","周末和家人一起去黄山看光明顶","单次","2025-01-21","未完成")
    # create_table4.create_persona("魅魔","妖娆,色诱,不吸干你血不罢休！！！")

    text1=create_table1.get_all_sessions()
    # text2=create_table2.get_all_users()
    # text3=create_table3.get_all_reminders()
    # text4=create_table4.get_all_personas()
    print(text1)
    # print(text2)
    # print(text3)
    # print(text4)

    # create_table1.update_chat("3508c7c7-fced-11ef-9c56-f077c346fabd",role='assistant')
    # create_table2.update_user("707d1896-214b-4941-89b5-a8049c0e2f79",name='小名',gender='女')

    # create_table1.delete_chat("3508c7c7-fced-11ef-9c56-f077c346fabd")

    create_table1.close()
    create_table2.close()
    create_table3.close()
    create_table4.close()