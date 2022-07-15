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

    @staticmethod
    def find_by_name():
        try:
            name = input('Nhap ten : ')
            find_students = list(Student.DATABASE.find({'name': f'{name}'}))

            if find_students:
                for student in find_students:
                    pprint(student)
            else:
                print('Khong tim thay sinh vien co ten da nhap')
        except Exception as err:
            print(f'Error when find student by name: {err}')

    @staticmethod
    def find_greater_score():
        try:
            score = int(input('Nhap diem: '))
            find_student = list(Student.DATABASE.find({'scores.0': {'$gt': score}}))

            if find_student:
                for student in find_student:
                    pprint(student)
            else:
                print('Khong tim thay sinh vien co diem dien kinh cao hon diem nhap')
        except Exception as err:
            print(f'Error when find student greater than socre: {err}')

    @staticmethod
    def find_greater_sum_of_scores():
        try:
            score = int(input('Nhap diem: '))
            find_student = list(Student.DATABASE.aggregate([{ '$project' : {
                        'id_student': '$id_student', 'total_scores': { '$sum': '$scores'}}}]))
            for st in find_student:
                if st['total_scores'] > score:
                    print(st)

        except Exception as err:
            print(f'Error when find student: {err}')


if __name__ == '__main__':
    student = Student()
    while True:
        print("""
            1. Hien thi toan bo sinh vien
            2. Hien thi thong tin cu the
            3. Tao moi sinh vien
            4. Cap nhat sinh vien
            5. Xoa sinh vien
            6. Tim theo ten
            7. Sinh vien co diem lon hon
            8. Tong diem cac mon lon hon
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
            case 6:
                Student.find_by_name()
            case 7:
                Student.find_greater_score()
            case 8:
                Student.find_greater_sum_of_scores()
            case default:
                break
