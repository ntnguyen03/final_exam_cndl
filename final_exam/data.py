from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Kết nối đến MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']

# Tạo các collection
db.departments.drop()
db.employees.drop()
db.performance_evaluations.drop()
db.training_programs.drop()
db.employee_training.drop()

# Thêm dữ liệu vào collection departments
departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations']
department_ids = []

for dept in departments:
    result = db.departments.insert_one({'name': dept})
    department_ids.append(result.inserted_id)

print(f"Đã thêm {len(departments)} phòng ban.")

# Thêm dữ liệu vào collection employees
first_names = ['Nguyen', 'Tran', 'Le', 'Pham', 'Hoang', 'Vu', 'Do', 'Bui', 'Dang', 'Dinh']
last_names = ['An', 'Binh', 'Cuong', 'Dung', 'Em', 'Giang', 'Hoa', 'Khanh', 'Linh', 'Minh']

for _ in range(100):  # Tạo 100 nhân viên
    employee = {
        'first_name': random.choice(first_names),
        'last_name': random.choice(last_names),
        'birth_date': datetime.now() - timedelta(days=random.randint(8000, 20000)),
        'hire_date': datetime.now() - timedelta(days=random.randint(0, 3650)),
        'department_id': random.choice(department_ids)
    }
    result = db.employees.insert_one(employee)
    
    # Thêm đánh giá hiệu suất cho nhân viên
    for _ in range(random.randint(1, 5)):  # 1-5 đánh giá cho mỗi nhân viên
        evaluation = {
            'employee_id': result.inserted_id,
            'evaluation_date': datetime.now() - timedelta(days=random.randint(0, 1000)),
            'score': round(random.uniform(1, 5), 2)
        }
        db.performance_evaluations.insert_one(evaluation)

print(f"Đã thêm {db.employees.count_documents({})} nhân viên và {db.performance_evaluations.count_documents({})} đánh giá hiệu suất.")

# Thêm dữ liệu vào collection training_programs
training_programs = ['Leadership Skills', 'Technical Skills', 'Communication Skills', 'Project Management', 'Customer Service']

for program in training_programs:
    start_date = datetime.now() - timedelta(days=random.randint(0, 365))
    db.training_programs.insert_one({
        'name': program,
        'start_date': start_date,
        'end_date': start_date + timedelta(days=random.randint(1, 30))
    })

print(f"Đã thêm {len(training_programs)} chương trình đào tạo.")

# Thêm dữ liệu vào collection employee_training
employees = list(db.employees.find())
programs = list(db.training_programs.find())

for _ in range(200):  # Tạo 200 bản ghi đào tạo
    employee = random.choice(employees)
    program = random.choice(programs)
    db.employee_training.insert_one({
        'employee_id': employee['_id'],
        'program_id': program['_id'],
        'completion_date': program['end_date'] + timedelta(days=random.randint(0, 30)),
        'performance_score': round(random.uniform(1, 5), 2)
    })

print(f"Đã thêm {db.employee_training.count_documents({})} bản ghi đào tạo nhân viên.")

print("Hoàn thành việc khởi tạo dữ liệu.")