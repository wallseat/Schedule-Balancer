from src.schemas import InputScheme, Day, ClassType, Week
from src.types import T_StudentName, T_StudentsSchedule, Dict, List


class HourBalancer:
    input_scheme: InputScheme

    students_hours: Dict[T_StudentName, int]
    students_schedule: T_StudentsSchedule

    _balanced: bool

    def __init__(self, input_scheme: InputScheme) -> None:
        self.input_scheme = input_scheme

        self.students_schedule = {st: {} for st in input_scheme.students}

        self.locations = self._get_locations()
        self.slots = {slot.id_: slot for slot in input_scheme.slots}
        self.courses = {course.id_: course for course in input_scheme.courses}

        self._students_hours = {st: 0 for st in input_scheme.students}
        self._balanced = False

    def _get_locations(self) -> Dict[Week, Dict[Day, str]]:
        out = {week: {day: "" for day in Day} for week in Week}

        for week, days in self.input_scheme.week.items():
            for day, day_scheme in days.items():
                out[week][day] = day_scheme.location

        return out

    def balance(self) -> T_StudentsSchedule:
        """
        Генерирует сбалансированное расписание для каждого студента
        """

        for week_no in range(
            self.input_scheme.start_week, self.input_scheme.end_week + 1
        ):
            week_schedule = (
                self.input_scheme.week[Week.odd]
                if week_no % 2
                else self.input_scheme.week[Week.even]
            )

            for day, classes in week_schedule.items():

                lower_h_students: List[str] = sorted(
                    self.input_scheme.students, key=lambda x: self._students_hours[x]
                )

                students_on_lecture = lower_h_students[
                    : self.input_scheme.min_on_lecture
                ]
                students_on_practice = lower_h_students[
                    : self.input_scheme.min_on_practice
                ]

                for class_ in classes.schedule:
                    if class_.type_ == ClassType.lecture:
                        students_set = students_on_lecture

                    else:
                        students_set = students_on_practice

                    for student in students_set:
                        self._students_hours[student] += 1

                        if week_no not in self.students_schedule[student]:
                            self.students_schedule[student][week_no] = {
                                Day.mon: {},
                                Day.tue: {},
                                Day.wed: {},
                                Day.thu: {},
                                Day.fri: {},
                                Day.sat: {},
                            }

                        self.students_schedule[student][week_no][day][
                            class_.slot_id
                        ] = class_

        self._balanced = True

        return self.students_schedule
