from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint


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
        db = client.students

    except Exception as err:
        err = f'Something wrong when connect to database: {err}'
        return [err, False]
    else:
        print('Connect success to database')
        return [db, True]


def create_collection(db):
    print(type(db))
    print(db.list_collection_names())
    if 'students' not in db.list_collection_names():
        print('There is no students collection. Insert database before use.')
    pass


def show_collection():
    pass


def create_new_student():
    pass


def update_scores():
    pass


def delete_a_student():
    pass


def calculate_score():
    pass


if __name__ == '__main__':
    connect = connect_to_mongo()
    if connect[1] == True:
        create_collection(connect[0])
    print("""
        1. Danh sach sinh vien
        2. Tao moi sinh vien
        3. Cap nhat diem cho sinh vien
        4. Xoa sinh vien
        5. Kiem tra diem sinh vien
        0. Thoat chuong trinh
        """)
    try:
        while True:
            choose = int(input('Nhap lua chon ban muon: '))
            match choose:
                case 0:
                    break
                case 1:
                    print(show_collection())
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case default:
                    break
    except Exception as err:
        print(f'Something wrong when process: {err}')
