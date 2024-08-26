import sqlite3

dna_list=['aaaaaaabbbbccccccvb',
          'ddddffffdddd',
          'aaadcccdddcccdd']

dna_list=sorted(dna_list)

connection=sqlite3.connect("gene_data.db")
cursor=connection.cursor()

cursor.execute("create table DNA_list (id INTEGER PRIMARY KEY AUTOINCREMENT, dna TEXT)")
for i in range(len(dna_list)):
    cursor.execute("insert into DNA_list (dna) values (?)",[dna_list[i]])
    print("added ", dna_list[i])
print("************")

for row in cursor.execute("select * from DNA_LIST"):
    print(row)

connection.commit()
connection.close()
