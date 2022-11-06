from src.core import HourBalancer
from src.render import HtmlRenderer
from src.schemas import InputScheme


def main():
    import sys

    args = sys.argv

    if len(args) < 2:
        print(f"No input file specified, use: {args[0].split('/')[-1]} INPUT_JSON")
        exit(1)

    import json

    with open(args[1], "r") as f:
        json_data = json.load(f)

    input_scheme = InputScheme.parse_obj(json_data)

    hour_balancer = HourBalancer(input_scheme)
    students_schedule = hour_balancer.balance()

    html_renderer = HtmlRenderer(
        students_schedule,
        courses=hour_balancer.courses,
        slots=hour_balancer.slots,
        locations=hour_balancer.locations,
    )
    html_renderer.render()
