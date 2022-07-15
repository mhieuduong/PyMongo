from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint
from bson.objectid import ObjectId


"""
1. Hien thi danh sach sinh vien
2. Tao moi sinh vien
3. Cap nhat diem sinh vien
4. Xoa sinh vien
5. Kiem tra sinh vien du diem qua mon
"""
"""
Sinh vien
    Ho ten
    Ngay sinh
    MSV
    Diem mon hoc: GDQP, Dien Kinh, Bong Chuyen
    Gioi tinh
"""


def connect_to_mongo():
    try:
        client = MongoClient(
            "mongodb+srv://mhieu:m0ng0Data@cluster0.8dhnaue.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
        client.server_info()
        db = client.school

    except Exception as err:
        err = f'Something wrong when connect to database: {err}'
        return [err, False]
    else:
        print('Connect success to database')
        return [db, True]


def create_collection(db):
    if 'students' not in db.list_collection_names():
        print('There is no students collection. Insert database before use.')
        try:
            db.create_collection('students')
        except Exception as err:
            print(f'Error when create collection: {err}')
            return ''
        else:
            print('Created "students" collection')
    else:
        print('You had students collection')

    students = db.get_collection('students')
    students.create_index('id_student', unique=True)
    return students


def show_collection(stu_collect):
    for student in stu_collect.find():
        pprint(student)

    print('Total students is : ' + str(stu_collect.count_documents({}))
          + '\n'
            + '===============')

    return 'Show collection is done'


def create_new_student(stu_collect):
    _id = ObjectId()
    name = input('Nhap ho ten: ')
    year = input('Nhap nam sinh: ')
    gender = input('Nhap gioi tinh [male/female]: ')
    id_student = input('Nhap ma sinh vien: ')
    scores = list(map(int, input("""
    Nhap diem GDPG, Dien kinh, Bong chuyen: 
        """).split()))

    try:
        add_student = stu_collect.insert_one({
            '_id': _id,
            'name': name,
            'year': year,
            'scores': scores,
            'gender': gender,
            'id_student': id_student
        })
        print('student object id:', add_student)
    except Exception as err:
        print(f'Error when create new student: {err}')
    return 'Create process is done'


def find_a_student(stu_collect):
    try:
        id_student = input('Nhap MSV: ')
        find_student = stu_collect.find_one({'id_student': f'{id_student}'})
        if find_student:
            pprint(find_student)
        else:
            print('Khong tim thay thong tin voi MSV da nhap')
    except Exception as err:
        return(f'Error when find a student: {err}')

    return ('=======\n' + 'Find process is done')


def update_scores(stu_collect):
    # id_student = input('Nhap MSV: ')
    id_student = '69dctm400'
    update_student = stu_collect.find_one({'id_student': id_student})
    pprint(update_student)

    print('Bo trong o diem neu khong muon cap nhat')
    gdqp = input('Nhap diem GDQP: ')
    dien_kinh = input('Nhap diem Dien kinh: ')
    bong_chuyen = input('Nhap diem Bong chuyen: ')

    gdqp = int(gdqp) if gdqp else update_student['scores'][0]
    dien_kinh = int(dien_kinh) if dien_kinh else update_student['scores'][1]
    bong_chuyen = int(
        bong_chuyen) if bong_chuyen else update_student['scores'][2]

    stu_collect.update_one(
        {'id_student': id_student},
        {"$set": {'scores': [gdqp, dien_kinh, bong_chuyen]}}
    )

    print(gdqp, dien_kinh, bong_chuyen)

    return 'Update process is done'


def delete_a_student(stu_collect):
    id_student = input('Nhap MSV muon xoa: ')
    try:
        delete_student = stu_collect.delete_one({'id_student': id_student})
        if delete_student.deleted_count:
            print('Xoa thanh cong')
        else:
            print('Sinh vien co MSV khong ton tai trong he thong')

    except Exception as err:
        return (f'Error when delete student: {err}')

    return 'Delete process is done'


def check_certificate(stu_collect):
    """
    (1) GDQP > 5
    (2) (Bong chuyen + Dien Kinh) / 2 > 5.5
    (1) va (2) thoa man -> Dat
    """
    id_student = input('Nhap MSV: ')
    try:
        student = stu_collect.find_one({'id_student': id_student})
        if stu_collect is not None:
            check = stu_collect.find_one(
                {"$expr": {"$and": [{"id_student": id_student},
                                    {"$gt": ["$array.0", 5]}]}})
            pprint("check: ", check)
        else:
            print('Sinh vien co MSV khong ton tai trong he thong')

    except Exception as err:
        return (f'Error when check certificate: {err}')

    return 'Check process is done'


if __name__ == '__main__':
    connect = connect_to_mongo()
    if connect[1] == True:
        students_collection = create_collection(connect[0])
        print('students_collection: ' + students_collection.name)
    else:
        exit()

    try:
        while True:
            print("""
                1. Danh sach sinh vien
                2. Tao moi sinh vien
                3. Cap nhat diem cho sinh vien
                4. Xoa sinh vien
                5. Kiem tra chung chi sinh vien
                6. Tim kiem sinh vien
                0. Thoat chuong trinh
                """)
            choose = int(input('Nhap lua chon ban muon: '))
            match choose:
                case 0:
                    break
                case 1:
                    print(show_collection(students_collection))
                case 2:
                    print(create_new_student(students_collection))
                case 3:
                    print(update_scores(students_collection))
                case 4:
                    print(delete_a_student(students_collection))
                case 5:
                    print(check_certificate(students_collection))
                case 6:
                    print(find_a_student(students_collection))
                case default:
                    break
    except Exception as err:
        print(f'Something wrong when process: {err}')
