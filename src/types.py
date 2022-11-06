from typing import Dict, List, Tuple

from src.schemas import Day, ClassScheme

T_StudentName = str
T_WeekNo = int
T_SlotId = int
T_CourseId = int
T_Location = str

T_StudentsSchedule = Dict[
    T_StudentName,
    Dict[
        T_WeekNo,
        Dict[
            Day,
            Dict[T_SlotId, ClassScheme],
        ],
    ],
]
