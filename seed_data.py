import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalari_backend.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta, date
from apps.users.models import User
from apps.curriculum.models import (
    Subject, Module, Topic, Problem, CodeExample,
    Batch, BatchTopicProgress, StaffDailyLog, StudentAttendanceRecord
)
from apps.assignments.models import Submission, ProblemAccess


def seed():
    print("[+] Seeding SkillStack Tutor Management Platform data...")

    # 1. Users
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Deepan',
            'last_name': 'Tutor Admin',
            'email': 'admin@skillstack.com',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True,
            'is_admin_role': True,
            'mobile_number': '9999900000',
            'pin_code': '0912'
        }
    )
    admin.email = 'admin@skillstack.com'
    admin.pin_code = '0912'
    admin.set_password('0912')
    admin.save()
    print(f"[OK] Master Admin user: admin@skillstack.com / 0912")

    trainer1, _ = User.objects.get_or_create(
        username='trainer1',
        defaults={
            'first_name': 'Karthik',
            'last_name': 'Ramasamy',
            'email': 'karthik@skillstack.com',
            'role': 'STAFF',
            'is_staff': True,
            'mobile_number': '9888811111',
            'pin_code': '1111',
            'bio': 'Senior C & Python Trainer with 7+ years of coaching experience.'
        }
    )
    trainer1.set_password('trainer123')
    trainer1.save()

    trainer2, _ = User.objects.get_or_create(
        username='trainer2',
        defaults={
            'first_name': 'Ananya',
            'last_name': 'Suresh',
            'email': 'ananya@skillstack.com',
            'role': 'STAFF',
            'is_staff': True,
            'mobile_number': '9888822222',
            'pin_code': '2222',
            'bio': 'Full Stack Web & Python Specialist.'
        }
    )
    trainer2.set_password('trainer123')
    trainer2.save()
    print(f"[OK] Staff trainers created (trainer1, trainer2 / trainer123)")

    student1, _ = User.objects.get_or_create(
        username='9876543210',
        defaults={
            'first_name': 'Praveen',
            'last_name': 'Kumar',
            'email': 'praveen@gmail.com',
            'role': 'STUDENT',
            'mobile_number': '9876543210',
            'pin_code': '1234',
            'batch_name': 'C Programming - Morning Batch A'
        }
    )
    student1.set_password('1234')
    student1.save()

    student2, _ = User.objects.get_or_create(
        username='9876543211',
        defaults={
            'first_name': 'Sneha',
            'last_name': 'Murugan',
            'email': 'sneha@gmail.com',
            'role': 'STUDENT',
            'mobile_number': '9876543211',
            'pin_code': '1234',
            'batch_name': 'C Programming - Morning Batch A'
        }
    )
    student2.set_password('1234')
    student2.save()

    student3, _ = User.objects.get_or_create(
        username='9876543212',
        defaults={
            'first_name': 'Vignesh',
            'last_name': 'Rajan',
            'email': 'vignesh@gmail.com',
            'role': 'STUDENT',
            'mobile_number': '9876543212',
            'pin_code': '1234',
            'batch_name': 'C Programming - Evening Batch B'
        }
    )
    student3.set_password('1234')
    student3.save()
    print(f"[OK] Students created (student mobile login: 9876543210 / 1234)")

    # 2. Courses
    c_course, _ = Subject.objects.get_or_create(
        slug='c-programming',
        defaults={
            'name': 'C Programming',
            'description': 'Master core programming fundamentals, memory management, pointers, and problem solving in C.',
            'short_description': 'Foundational programming concepts with structured memory mastery.',
            'duration': '6 Weeks',
            'schedule_type': '3 days class + 3 days lab per week',
            'level': 'Beginner',
            'icon': 'c',
            'order': 1
        }
    )

    py_course, _ = Subject.objects.get_or_create(
        slug='python-programming',
        defaults={
            'name': 'Python Programming',
            'description': 'Complete Python from fundamentals to OOP, data structures, and script automation.',
            'short_description': 'Modern Python programming with algorithmic problem solving.',
            'duration': '8 Weeks',
            'schedule_type': '3 days class + 3 days lab per week',
            'level': 'Beginner to Intermediate',
            'icon': 'python',
            'order': 2
        }
    )

    django_course, _ = Subject.objects.get_or_create(
        slug='django-fullstack',
        defaults={
            'name': 'Django Full Stack',
            'description': 'End-to-end backend engineering, REST APIs, authentication, and PostgreSQL.',
            'short_description': 'Enterprise web backend with Django REST Framework.',
            'duration': '10 Weeks',
            'schedule_type': '4 days class + 2 days lab per week',
            'level': 'Intermediate to Advanced',
            'icon': 'django',
            'order': 3
        }
    )

    excel_course, _ = Subject.objects.get_or_create(
        slug='advanced-ms-excel',
        defaults={
            'name': 'Advanced MS Excel & Data Analytics',
            'description': 'Master formulas (VLOOKUP, XLOOKUP, INDEX-MATCH), Pivot Tables, Conditional Formatting, Data Visualization, and Dashboards.',
            'short_description': 'Industry-standard spreadsheet mastery, business formulas & data automation.',
            'duration': '4 Weeks',
            'schedule_type': 'Mon to Fri Daily Practical Labs',
            'level': 'Beginner to Advanced',
            'icon': 'excel',
            'order': 4
        }
    )

    word_course, _ = Subject.objects.get_or_create(
        slug='ms-word-office',
        defaults={
            'name': 'MS Word & Professional Office Documentation',
            'description': 'Official document formatting, mail merge, tables, typography styles, cover letters, invoices, and executive reports.',
            'short_description': 'Essential workplace documentation, formatting and official publishing.',
            'duration': '3 Weeks',
            'schedule_type': '3 days class + 2 days lab per week',
            'level': 'Beginner to Intermediate',
            'icon': 'word',
            'order': 5
        }
    )

    tally_course, _ = Subject.objects.get_or_create(
        slug='tally-prime-accounting',
        defaults={
            'name': 'Tally Prime & GST Accounting',
            'description': 'Computerized accounting, voucher entry, inventory management, GST computation, balance sheets, and audit reports.',
            'short_description': 'Complete business accounting & computerized GST tax compliance.',
            'duration': '6 Weeks',
            'schedule_type': 'Mon, Wed, Fri - 10:00 AM to 12:00 PM',
            'level': 'Beginner to Advanced',
            'icon': 'tally',
            'order': 6
        }
    )
    print("[OK] Courses created (C, Python, Django, Advanced Excel, MS Word, Tally Prime)")

    # 3. Modules, Topics & Practice Programs for C Programming
    mod_c1, _ = Module.objects.get_or_create(
        subject=c_course,
        name='Module 1: Syntax, Variables & Formatting',
        defaults={'level': 'beginner', 'order': 1}
    )

    top_c1, _ = Topic.objects.get_or_create(
        module=mod_c1,
        topic_id='c-intro-variables',
        defaults={
            'title': 'Variables, Data Types & Formatted I/O',
            'explain': [
                'Understanding primitive data types (int, float, char) and format specifiers.',
                'Printing structured output using printf with alignment and precision.',
                'Best practices for variable declaration and memory allocation.'
            ],
            'notes_content': """# Formatted Output in C

In C programming, the `printf()` function defined in `<stdio.h>` outputs formatted characters to the standard output console.

### Format Specifiers:
- `%d` or `%i`: Signed decimal integer
- `%f`: Floating-point decimal
- `%c`: Single character
- `%s`: Character string

### Example:
```c
#include <stdio.h>

int main() {
    char name[] = "Alex";
    int score = 95;
    printf("=== Student Profile ===\\n");
    printf("Name: %s\\n", name);
    printf("Score: %d\\n", score);
    printf("Grade: A+\\n");
    return 0;
}
```
""",
            'order': 1
        }
    )

    prob_c1, _ = Problem.objects.get_or_create(
        topic=top_c1,
        title='Program 1: Student Profile Card Formatter',
        defaults={
            'description': 'Write a C program that outputs a 4-line formatted profile card. The output must match the exact lines specified.',
            'language': 'c',
            'expected_output': "=== Student Profile ===\nName: Alex\nScore: 95\nGrade: A+",
            'expected_output_hint': 'Print 4 lines: header, Name: Alex, Score: 95, Grade: A+',
            'starter_code': """#include <stdio.h>

int main() {
    // Write your code here
    
    return 0;
}
""",
            'points': 10,
            'order': 1
        }
    )

    prob_c2, _ = Problem.objects.get_or_create(
        topic=top_c1,
        title='Program 2: Circle Area & Perimeter Calculator',
        defaults={
            'description': 'Given radius = 7, print the circle Radius, Area (formula: 3.14159 * r * r with 2 decimal places), and Circumference (2 * 3.14159 * r with 2 decimal places).',
            'language': 'c',
            'expected_output': "Radius: 7\nArea: 153.94\nCircumference: 43.98",
            'expected_output_hint': 'Area: 153.94, Circumference: 43.98',
            'starter_code': """#include <stdio.h>

int main() {
    int r = 7;
    // Calculate and print
    
    return 0;
}
""",
            'points': 10,
            'order': 2
        }
    )

    # 4. Modules & Topics for Python
    mod_py1, _ = Module.objects.get_or_create(
        subject=py_course,
        name='Module 1: Control Flow & Lists',
        defaults={'level': 'beginner', 'order': 1}
    )

    top_py1, _ = Topic.objects.get_or_create(
        module=mod_py1,
        topic_id='py-loops-lists',
        defaults={
            'title': 'Fibonacci Series & List Aggregations',
            'explain': [
                'Generating mathematical sequences using while and for loops.',
                'Accumulator variables and sum aggregations over integer lists.'
            ],
            'notes_content': """# Fibonacci Numbers in Python

The Fibonacci sequence begins with 0 and 1, where each subsequent number is the sum of the two preceding ones:
`0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...`

```python
fib = [0, 1]
for _ in range(8):
    fib.append(fib[-1] + fib[-2])
print(fib)
print(f"Sum: {sum(fib)}")
```
""",
            'order': 1
        }
    )

    prob_py1, _ = Problem.objects.get_or_create(
        topic=top_py1,
        title='Program 1: Generate First 10 Fibonacci Numbers & Sum',
        defaults={
            'description': 'Generate a Python list containing the first 10 Fibonacci numbers (starting at 0), print the list, and on the next line print "Sum: <total>".',
            'language': 'python',
            'expected_output': "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\nSum: 88",
            'expected_output_hint': 'Output format: [0, 1, ...] newline Sum: 88',
            'starter_code': """# Generate first 10 fibonacci numbers
fib = [0, 1]
while len(fib) < 10:
    fib.append(fib[-1] + fib[-2])

print(fib)
print(f"Sum: {sum(fib)}")
""",
            'points': 10,
            'order': 1
        }
    )

    prob_py2, _ = Problem.objects.get_or_create(
        topic=top_py1,
        title='Program 2: Filter Even Squares',
        defaults={
            'description': 'For numbers from 1 to 10 inclusive, compute the square of each even number and print the result list.',
            'language': 'python',
            'expected_output': "[4, 16, 36, 64, 100]",
            'expected_output_hint': 'List of squares of even numbers from 1 to 10',
            'starter_code': """# Write a list comprehension to square even numbers 1..10
res = [x**2 for x in range(1, 11) if x % 2 == 0]
print(res)
""",
            'points': 10,
            'order': 2
        }
    )

    # 4b. Modules & Practical Labs for Advanced MS Excel
    mod_xl1, _ = Module.objects.get_or_create(
        subject=excel_course,
        name='Module 1: Advanced Formulas & Lookup Functions',
        defaults={'level': 'intermediate', 'order': 1}
    )

    top_xl1, _ = Topic.objects.get_or_create(
        module=mod_xl1,
        topic_id='excel-vlookup-xlookup',
        defaults={
            'title': 'VLOOKUP, XLOOKUP & Dynamic Data Search',
            'explain': [
                'Syntax of VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]).',
                'Using modern XLOOKUP for two-way lookups with exact and approximate matching.',
                'Handling #N/A errors with IFERROR and IFNA functions.'
            ],
            'notes_content': """# Advanced Excel Lookups: VLOOKUP & XLOOKUP

Lookup functions search for a specific value in a dataset table and return a corresponding value from another column.

### 1. VLOOKUP Formula Syntax:
```excel
=VLOOKUP(lookup_value, table_range, column_index, FALSE)
```
- `lookup_value`: Cell value to search (e.g., Employee ID `E104`)
- `table_range`: Selected reference data table (e.g., `A2:D50`)
- `column_index`: Number of the column from which to fetch data (e.g., `3` for Salary)
- `FALSE`: Exact match requirement

### 2. XLOOKUP Modern Formula:
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])
```
*Example:* `=XLOOKUP(G2, A2:A100, D2:D100, "Employee Not Found")`
""",
            'order': 1
        }
    )

    prob_xl1, _ = Problem.objects.get_or_create(
        topic=top_xl1,
        title='Lab Task 1: Salary & Department Lookup Matrix',
        defaults={
            'description': 'Construct an automated VLOOKUP formula to retrieve employee designation and monthly CTC from the master payroll table. Expected result output must verify formula integrity.',
            'language': 'excel',
            'expected_output': "LOOKUP_RESULT: Designation=Senior Data Analyst | CTC=₹85,000 | Status=VERIFIED",
            'expected_output_hint': 'Use =VLOOKUP(E2, A2:D20, 3, FALSE)',
            'starter_code': '=VLOOKUP(E2, A2:D20, 3, FALSE)',
            'points': 10,
            'order': 1
        }
    )

    # 4c. Modules & Practical Labs for MS Word & Documentation
    mod_wd1, _ = Module.objects.get_or_create(
        subject=word_course,
        name='Module 1: Mail Merge & Executive Templates',
        defaults={'level': 'beginner', 'order': 1}
    )

    top_wd1, _ = Topic.objects.get_or_create(
        module=mod_wd1,
        topic_id='word-mail-merge',
        defaults={
            'title': 'Mail Merge Automation & Bulk Certificate Generation',
            'explain': [
                'Connecting Excel data source list to Word document.',
                'Inserting merge fields: <<First_Name>>, <<Course_Name>>, <<Grade>>.',
                'Generating individual PDF letters and print batches.'
            ],
            'notes_content': """# MS Word Mail Merge Masterclass

Mail Merge allows generating personalized documents (appointment letters, certificates, invoices) in bulk by linking a master Word document to an Excel database.

### Step-by-Step Workflow:
1. Open Word -> Go to **Mailings** Tab -> **Start Mail Merge** -> Select **Letters / Envelopes**.
2. Click **Select Recipients** -> **Use an Existing List** -> Choose your `students_list.xlsx` sheet.
3. Click **Insert Merge Field** to place dynamic tokens: `<<Student_Name>>`, `<<Batch_Name>>`, `<<Issue_Date>>`.
4. Preview results and click **Finish & Merge** -> **Edit Individual Documents**.
""",
            'order': 1
        }
    )

    prob_wd1, _ = Problem.objects.get_or_create(
        topic=top_wd1,
        title='Lab Task 1: Official Course Completion Certificate Template',
        defaults={
            'description': 'Configure a Word Mail Merge template with <<Student_Name>>, <<Course>>, and <<Completion_Date>> tokens linked to the candidate Excel data sheet.',
            'language': 'word',
            'expected_output': "MAIL_MERGE_STATUS: Fields=<<Student_Name>>,<<Course>>,<<Date>> | Records_Merged=30 | Status=PASSED",
            'expected_output_hint': 'Insert merge fields into the certificate template',
            'starter_code': '<<Student_Name>> has successfully completed <<Course>> on <<Date>>.',
            'points': 10,
            'order': 1
        }
    )

    # 5. Batches (including Duplicate Course Name running in parallel!)
    batch_c_a, _ = Batch.objects.get_or_create(
        name='C Programming - Morning Batch A (10:00 AM)',
        defaults={
            'course': c_course,
            'schedule': 'Mon, Wed, Fri - 10:00 AM to 12:00 PM',
            'start_date': date.today() - timedelta(days=14),
            'status': 'ACTIVE',
            'max_students': 25
        }
    )
    batch_c_a.staff.add(trainer1)
    batch_c_a.students.add(student1, student2)

    batch_c_b, _ = Batch.objects.get_or_create(
        name='C Programming - Evening Batch B (03:00 PM)',
        defaults={
            'course': c_course,
            'schedule': 'Tue, Thu, Sat - 03:00 PM to 05:00 PM',
            'start_date': date.today() - timedelta(days=7),
            'status': 'ACTIVE',
            'max_students': 25
        }
    )
    batch_c_b.staff.add(trainer2)
    batch_c_b.students.add(student3)

    batch_py, _ = Batch.objects.get_or_create(
        name='Python Full Stack - Regular Batch (11:30 AM)',
        defaults={
            'course': py_course,
            'schedule': 'Mon, Wed, Fri - 11:30 AM to 01:30 PM',
            'start_date': date.today() - timedelta(days=10),
            'status': 'ACTIVE',
            'max_students': 30
        }
    )
    batch_py.staff.add(trainer1)
    batch_py.students.add(student1, student3)
    print("[OK] Batches created with duplicate course support and student enrollments")

    # 6. Initialize Topic Progress for Batches
    for b in [batch_c_a, batch_c_b, batch_py]:
        course_topics = Topic.objects.filter(module__subject=b.course)
        for idx, t in enumerate(course_topics):
            # Mark first topic as completed for batch A
            is_done = (b == batch_c_a and idx == 0)
            BatchTopicProgress.objects.get_or_create(
                batch=b,
                topic=t,
                defaults={
                    'is_completed': is_done,
                    'completed_at': timezone.now() if is_done else None,
                    'marked_by': trainer1 if is_done else None,
                    'remarks': 'Covered syntax & completed lab 1 successfully' if is_done else ''
                }
            )
    print("[OK] Batch topic progress initialized")

    # 7. Seed Staff Daily Task Logs (Today & Past Days for reports)
    today = date.today()
    log1, _ = StaffDailyLog.objects.get_or_create(
        date=today,
        batch=batch_c_a,
        course=c_course,
        staff=trainer1,
        defaults={
            'session_type': 'TOPIC',
            'session_title': 'Variables & Formatted Output',
            'topic': top_c1,
            'total_enrolled': 2,
            'students_attended': 2,
            'remarks': 'All students present. Completed practice program 1 in lab.'
        }
    )

    log2, _ = StaffDailyLog.objects.get_or_create(
        date=today,
        batch=batch_c_b,
        course=c_course,
        staff=trainer2,
        defaults={
            'session_type': 'LAB',
            'session_title': 'Lab Practice Session - Formatters',
            'topic': top_c1,
            'total_enrolled': 1,
            'students_attended': 1,
            'remarks': 'Assisted with C compiler syntax errors and printf formatting.'
        }
    )

    # Past dates for monthly/yearly reports
    for days_ago in [2, 5, 8, 12, 18, 25]:
        past_date = today - timedelta(days=days_ago)
        StaffDailyLog.objects.get_or_create(
            date=past_date,
            batch=batch_c_a,
            course=c_course,
            staff=trainer1,
            defaults={
                'session_type': 'TOPIC' if days_ago % 2 == 0 else 'LAB',
                'session_title': 'Session ' + str(days_ago),
                'topic': top_c1,
                'total_enrolled': 2,
                'students_attended': 2 if days_ago % 4 != 0 else 1,
                'remarks': 'Regular batch session conducted on schedule.'
            }
        )
    print("[OK] Staff daily task logs created across dates for multi-dimensional reporting")

    # 8. Sample Submissions with Real Telemetry
    sub1, _ = Submission.objects.get_or_create(
        student=student1,
        problem=prob_c1,
        defaults={
            'batch': batch_c_a,
            'language': 'c',
            'submitted_code': """#include <stdio.h>

int main() {
    printf("=== Student Profile ===\\n");
    printf("Name: Alex\\n");
    printf("Score: 95\\n");
    printf("Grade: A+\\n");
    return 0;
}
""",
            'actual_output': "=== Student Profile ===\nName: Alex\nScore: 95\nGrade: A+",
            'expected_output': prob_c1.expected_output,
            'is_passed': True,
            'status': 'PASSED',
            'execution_time_ms': 14.2,
            'attempt_number': 1,
            'score': 10,
            'staff_feedback': 'Clean solution! Correct output formatting.'
        }
    )

    sub2, _ = Submission.objects.get_or_create(
        student=student1,
        problem=prob_py1,
        defaults={
            'batch': batch_py,
            'language': 'python',
            'submitted_code': """fib = [0, 1]
while len(fib) < 10:
    fib.append(fib[-1] + fib[-2])

print(fib)
print(f"Sum: {sum(fib)}")
""",
            'actual_output': "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\nSum: 88",
            'expected_output': prob_py1.expected_output,
            'is_passed': True,
            'status': 'PASSED',
            'execution_time_ms': 28.5,
            'attempt_number': 1,
            'score': 10,
            'staff_feedback': 'Great logic.'
        }
    )
    print("[OK] Sample student submissions seeded")
    print("[SUCCESS] Seed complete!")


if __name__ == '__main__':
    seed()
