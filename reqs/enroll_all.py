import pdb

import requests

username = "student1"
password = "testpass123"

url = "http://localhost:8000/api/courses/"
r = requests.get(url)
courses = r.json()
available_courses = ", ".join([course["title"] for course in courses])
print(f"Available courses: {available_courses}")


for course in courses:
    course_id, course_title = course["id"], course["title"]

    url = f"http://localhost:8000/api/courses/{course_id}/enroll/"
    r = requests.post(url, auth=(username, password))
    if r.status_code == 200:
        print(f"Sucessfully enrolled in course: {course_title}.")
