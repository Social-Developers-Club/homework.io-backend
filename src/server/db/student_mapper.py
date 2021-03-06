from server.bo.student import Student
from server.db.mapper import Mapper


class StudentMapper(Mapper):

    def __init__(self):
        super().__init__()

    def find_all(self):
        result = []
        cursor = self._cnx.cursor()
        cursor.execute("SELECT * from student")
        tuples = cursor.fetchall()

        for (id, first_name, surname, school_id) in tuples:
            student = self.__create_student(id, first_name, surname)
            result.append(student)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_surname(self, name):
        result = []
        cursor = self._cnx.cursor()
        command = "SELECT id, first_name, surname FROM student WHERE surname LIKE '{}' ORDER BY surname".format(name)
        cursor.execute(command)
        tuples = cursor.fetchall()

        for (id, first_name, surname) in tuples:
            student = self.__create_student(id, first_name, surname)
            result.append(student)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_class(self, class_id):
        result = []
        cursor = self._cnx.cursor()
        command = "SELECT id, first_name, surname FROM student WHERE class_id='{}' ORDER BY surname".format(class_id)
        cursor.execute(command)
        tuples = cursor.fetchall()

        for (id, first_name, surname, school_id) in tuples:
            student = self.__create_student(id, first_name, surname)
            result.append(student)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_school(self, school):
        result = []
        cursor = self._cnx.cursor()
        command = "SELECT id, first_name, surname FROM student WHERE school_id='{}' ORDER BY surname".format(school)
        cursor.execute(command)
        tuples = cursor.fetchall()

        for (id, first_name, surname, school_id) in tuples:
            student = self.__create_student(id, first_name, surname)
            result.append(student)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_key(self, key):
        result = None

        cursor = self._cnx.cursor()
        command = "SELECT id, first_name, surname FROM student WHERE id={}".format(key)
        cursor.execute(command)
        tuples = cursor.fetchall()

        try:
            (id, first_name, surname) = tuples[0]
            student = self.__create_student(id, first_name, surname)
            result = student
        except IndexError:
            """tritt auf, wenn kein Tupel zurückgeliefert wurde"""
            result = None

        self._cnx.commit()
        cursor.close()

        return result

    def insert(self, student):
        cursor = self._cnx.cursor()
        cursor.execute("SELECT MAX(id) AS maxid FROM student ")
        tuples = cursor.fetchall()

        for (maxid) in tuples:
            student.set_id(maxid[0]+1)

        command = "INSERT INTO student (id, first_name, surname, school_id) VALUES (%s,%s,%s,%s)"
        # School_ID ist aktuell immer 0, daher hier statisch gecodet
        data = (student.get_id(), student.get_first_name(), student.get_surname(), 0)
        cursor.execute(command, data)

        self._cnx.commit()
        cursor.close()

        return student

    def update(self, student):
        cursor = self._cnx.cursor()

        command = "UPDATE student " + "SET first_name=%s, surname=%s WHERE id=%s"
        data = (student.get_first_name(), student.get_surname(), student.get_id())
        cursor.execute(command, data)

        self._cnx.commit()
        cursor.close()

    def delete(self, student):
        cursor = self._cnx.cursor()

        command = "DELETE FROM student WHERE id={}".format(student.get_id())
        cursor.execute(command)

        self._cnx.commit()
        cursor.close()

    def __create_student(self, id, first_name, surname):
        student = Student()
        student.set_id(id)
        student.set_first_name(first_name)
        student.set_surname(surname)
        return student


if __name__ == "__main__":
    with StudentMapper() as mapper:
        result = mapper.find_all()
        for p in result:
            print(p)