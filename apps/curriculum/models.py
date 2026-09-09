from django.db import models
from django.conf import settings
from django.utils import timezone


class Subject(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200, help_text="Course name e.g. C Programming, Python, Django")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(help_text="Detailed course overview", blank=True, default="")
    short_description = models.CharField(max_length=255, blank=True, default="")
    duration = models.CharField(max_length=50, default="8 Weeks", help_text="e.g. 8 Weeks / 45 Days")
    schedule_type = models.CharField(
        max_length=100,
        default="3 days class + 3 days lab per week",
        help_text="e.g. 3 days class + 3 days lab per week"
    )
    level = models.CharField(max_length=50, default="Beginner to Advanced")
    icon = models.CharField(max_length=50, default="code", help_text="Icon identifier e.g. python, c, code, database")
    banner_image = models.TextField(blank=True, default="")
    instructor_name = models.CharField(max_length=150, default="Lead Trainer")
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Course / Subject"
        verbose_name_plural = "Courses / Subjects"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name) or "subject"
            slug = base_slug
            counter = 1
            while Subject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Module(models.Model):
    objects = models.Manager()
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='modules', null=True, blank=True)
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        prefix = f"[{self.subject.name}] " if self.subject else ""
        return f"{prefix}[{self.level.upper()}] {self.name}"


class Topic(models.Model):
    objects = models.Manager()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    topic_id = models.SlugField(max_length=100, unique=True, blank=True)
    title = models.CharField(max_length=255)
    explain = models.JSONField(default=list, blank=True, help_text="List of explanation points/paragraphs")
    notes_content = models.TextField(blank=True, default="", help_text="Rich markdown/text study notes for the topic")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['module__order', 'order', 'id']

    def save(self, *args, **kwargs):
        if not self.topic_id:
            from django.utils.text import slugify
            base_slug = slugify(self.title) or "topic"
            topic_id = base_slug
            counter = 1
            while Topic.objects.filter(topic_id=topic_id).exclude(pk=self.pk).exists():
                topic_id = f"{base_slug}-{counter}"
                counter += 1
            self.topic_id = topic_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module.subject.name if self.module and self.module.subject else ''} -> {self.title}"


class CodeExample(models.Model):
    objects = models.Manager()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='examples')
    label = models.CharField(max_length=150)
    code = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.topic.title} - {self.label}"


class Problem(models.Model):
    objects = models.Manager()
    LANGUAGE_CHOICES = (
        ('python', 'Python 3'),
        ('c', 'C Programming'),
        ('javascript', 'JavaScript (Node.js)'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('excel', 'MS Excel / Spreadsheet Task'),
        ('word', 'MS Word & Documentation Task'),
        ('tally', 'Tally Prime / Accounting Entry'),
        ('sql', 'SQL & Database Query'),
        ('general', 'General Practical Exercise / Task'),
    )

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Detailed problem statement & instructions")
    language = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default='python')
    expected_output = models.TextField(
        blank=True,
        default="",
        help_text="The exact answer key output string used for automated validation"
    )
    expected_output_hint = models.TextField(blank=True, default="", help_text="Public hint shown to student")
    starter_code = models.TextField(blank=True, default="", help_text="Initial starter template code")
    test_criteria = models.JSONField(default=list, blank=True, help_text="Automated test criteria list")
    expected_keywords = models.JSONField(default=list, blank=True, help_text="Required code/syntax tokens")
    points = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.topic.title} - Lab #{self.order}: {self.title} [{self.language}]"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from apps.assignments.models import ProblemAccess
            ProblemAccess.objects.get_or_create(problem=self)


class Batch(models.Model):
    objects = models.Manager()
    STATUS_CHOICES = (
        ('UPCOMING', 'Upcoming'),
        ('ACTIVE', 'Active / Ongoing'),
        ('COMPLETED', 'Completed'),
        ('PAUSED', 'Paused'),
    )

    name = models.CharField(max_length=150, help_text="e.g. C Programming - Morning Batch A (10:00 AM)")
    course = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='batches',
        help_text="Linked course (supports duplicate course names across separate batches)"
    )
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='assigned_batches',
        help_text="Assigned staff trainers"
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='enrolled_batches',
        help_text="Enrolled students in this batch"
    )
    schedule = models.CharField(max_length=150, default="Mon-Wed-Fri 10:00 AM - 12:00 PM")
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    max_students = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Batch"
        verbose_name_plural = "Batches"

    @property
    def student_count(self):
        return self.students.count()

    def __str__(self):
        return f"{self.name} ({self.course.name}) - [{self.status}]"


class BatchTopicProgress(models.Model):
    objects = models.Manager()
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='batch_progress')
    is_completed = models.BooleanField(default=False, help_text="Independent topic completion flag")
    completed_at = models.DateTimeField(null=True, blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='marked_topic_progress'
    )
    remarks = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ('batch', 'topic')
        ordering = ['topic__order', 'id']

    def __str__(self):
        status = "DONE" if self.is_completed else "PENDING"
        return f"{self.batch.name} - {self.topic.title} [{status}]"


class StaffDailyLog(models.Model):
    objects = models.Manager()
    SESSION_TYPE_CHOICES = (
        ('TOPIC', 'Topic / Theory Class'),
        ('LAB', 'Lab Practice Session'),
        ('DOUBT', 'Doubt Clearing / Review'),
        ('ASSESSMENT', 'Assessment / Test'),
    )

    date = models.DateField(default=timezone.localdate)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='daily_logs')
    course = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='daily_logs')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_task_logs')
    session_type = models.CharField(max_length=30, choices=SESSION_TYPE_CHOICES, default='TOPIC')
    session_title = models.CharField(max_length=200, blank=True, default="", help_text="Topic name covered or 'Lab'")
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.SET_NULL, related_name='daily_logs')
    total_enrolled = models.PositiveIntegerField(default=0)
    students_attended = models.PositiveIntegerField(default=0, help_text="Aggregate attended student count filled by staff")
    remarks = models.TextField(blank=True, default="", help_text="Free text notes/remarks by staff")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} | {self.batch.name} | {self.session_type} ({self.students_attended}/{self.total_enrolled})"


class StudentAttendanceRecord(models.Model):
    objects = models.Manager()
    daily_log = models.ForeignKey(StaffDailyLog, on_delete=models.CASCADE, related_name='student_attendance_records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    is_present = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        unique_together = ('daily_log', 'student')

    def __str__(self):
        p = "Present" if self.is_present else "Absent"
        return f"{self.daily_log.date} - {self.student.username}: {p}"
