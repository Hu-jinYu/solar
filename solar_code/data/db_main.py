import solar.solar_code.data.db_table as d
if __name__=="__main__":
    create_table1=d.Chat()
    create_table2=d.UserInfoManager()
    create_table3=d.ReminderManager()
    create_table4=d.PersonaManager()

    create_table1._create_table()
    create_table2._create_table()
    create_table3._create_table()
    create_table4._create_table()

    create_table1.close()
    create_table2.close()
    create_table3.close()
    create_table4.close()