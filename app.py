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


class DataBase(object):
    URI = "mongodb+srv://mhieu:m0ng0Data@cluster0.8dhnaue.mongodb.net/" \
          "?retryWrites=true&w=majority",
    DATABASE = None

    @staticmethod
    def initialize():
        client = MongoClient(DataBase.URI, server_api=ServerApi('1'))
        DataBase.DATABASE = client['school']

    @classmethod
    def connect(cls, collection):
        return DataBase.DATABASE[collection]


class Student(DataBase):
    DATABASE = None

    @staticmethod
    def __init__():
        DataBase.initialize()
        Student.DATABASE = DataBase.connect('students')

    @staticmethod
    def find_all():
        for student in Student.DATABASE.find():
            pprint(student)
        print('Total students is : ' + str(Student.DATABASE.count_documents({}))
              + '\n'
              + '===============')

    @staticmethod
    def find_one():
        try:
            id_student = input('Nhap MSV: ')
            find_student = Student.DATABASE.find_one({'id_student': f'{id_student}'})
            if find_student:
                pprint(find_student)
            else:
                print('Khong tim thay thong tin voi MSV da nhap')
        except Exception as err:
            return f'Error when find a student: {err}'

    @staticmethod
    def update():
        id_student = input('Nhap MSV: ')
        update_student = Student.DATABASE.find_one({'id_student': id_student})
        pprint(update_student)

        print('Bo trong o diem neu khong muon cap nhat')
        gdqp = input('Nhap diem GDQP: ')
        dien_kinh = input('Nhap diem Dien kinh: ')
        bong_chuyen = input('Nhap diem Bong chuyen: ')

        gdqp = int(gdqp) if gdqp else update_student['scores'][0]
        dien_kinh = int(dien_kinh) if dien_kinh else update_student['scores'][1]
        bong_chuyen = int(
            bong_chuyen) if bong_chuyen else update_student['scores'][2]

        Student.DATABASE.update_one(
            {'id_student': id_student},
            {"$set": {'scores': [gdqp, dien_kinh, bong_chuyen]}}
        )

        print(gdqp, dien_kinh, bong_chuyen)

    @staticmethod
    def create():
        _id = ObjectId()
        name = input('Nhap ho ten: ')
        year = input('Nhap nam sinh: ')
        gender = input('Nhap gioi tinh [male/female]: ')
        id_student = input('Nhap ma sinh vien: ')
        scores = list(map(int, input("""
        Nhap diem GDPG, Dien kinh, Bong chuyen: 
            """).split()))

        try:
            add_student = Student.DATABASE.insert_one({
                '_id': _id,
                'name': name,
                'year': year,
                'scores': scores,
                'gender': gender,
                'id_student': id_student
            })
        except Exception as err:
            print(f'Error when create new student: {err}')
        return 'Create process is done'

    @staticmethod
    def delete():
        id_student = input('Nhap MSV muon xoa: ')
        try:
            delete_student = Student.DATABASE.delete_one({'id_student': id_student})
            if delete_student.deleted_count:
                print('Xoa thanh cong')
            else:
                print('Sinh vien co MSV khong ton tai trong he thong')
        except Exception as err:
            return f'Error when delete student: {err}'


if __name__ == '__main__':
    student = Student()
    while True:
        print("""
            1. Hien thi toan bo sinh vien
            2. Hien thi thong tin cu the
            3. Tao moi sinh vien
            4. Cap nhat sinh vien
            5. Xoa sinh vien
            0. Thoat khoi chuong trinh
            """)
        choose = int(input('Nhap lua chon: '))
        match choose:
            case 1:
                Student.find_all()
            case 2:
                Student.find_one()
            case 3:
                Student.create()
            case 4:
                Student.update()
            case 5:
                Student.delete()
            case default:
                break