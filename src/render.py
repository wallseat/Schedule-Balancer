import os

from jinja2 import Environment, FileSystemLoader

from src import MODULE_PATH
from src.types import (
    T_StudentsSchedule,
    T_StudentName,
    List,
    T_SlotId,
    Dict,
    T_Location,
    T_CourseId,
)
from src.schemas import SlotScheme, CourseScheme, Week, Day

env = Environment(loader=FileSystemLoader(MODULE_PATH + "/templates"))


class HtmlRenderer:
    def __init__(
        self,
        students_schedule: T_StudentsSchedule,
        slots: Dict[T_SlotId, SlotScheme],
        courses: Dict[T_CourseId, CourseScheme],
        locations: Dict[Week, Dict[Day, T_Location]],
        *,
        template_name: str = "template.html",
    ):
        self.template = env.get_template(template_name)

        self.locations = locations
        self.courses = courses
        self.slots = slots
        self.students_schedule = students_schedule

    def render(
        self,
        *,
        output_folder: str = "./schedules",
        exclude_list: List[T_StudentName] = None,
        only_list: List[T_StudentName] = None,
    ) -> None:
        if exclude_list and only_list:
            raise AssertionError("exclude_list and only_list are mutually exclusive")

        os.path.exists(f"{output_folder}") or os.mkdir(f"{output_folder}")

        for student, schedule in self.students_schedule.items():
            start_week = min(schedule.keys())
            end_week = max(schedule.keys())

            for week_no, days in schedule.items():
                week_type = Week.odd if week_no % 2 else Week.even

                output_html = self.template.render(
                    student_name=student,
                    slots=self.slots,
                    courses=self.courses,
                    locations=self.locations,
                    week_no=week_no,
                    week_type=week_type,
                    days=days,
                    start_week=start_week,
                    end_week=end_week,
                )

                os.path.exists(f"{output_folder}/{student}") or os.mkdir(
                    f"{output_folder}/{student}"
                )

                with open(f"schedules/{student}/week_{week_no}.html", "w") as f:
                    f.write(output_html)
