from django.db import models
from django.conf import settings
from django.utils import timezone

SUPABASE_URL = "https://ystzefjfudtqgrzlcgmb.supabase.co"
SUPABASE_STORAGE_BUCKET = "topic-images"


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
            base_slug = str(slugify(self.name)) or "subject"
            slug = base_slug
            counter = 1
            while Subject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


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

    def __str__(self) -> str:
        prefix = f"[{self.subject.name}] " if self.subject else ""
        return f"{prefix}[{str(self.level).upper()}] {str(self.name)}"


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
            base_slug = str(slugify(self.title)) or "topic"
            topic_id = base_slug
            counter = 1
            while Topic.objects.filter(topic_id=topic_id).exclude(pk=self.pk).exists():
                topic_id = f"{base_slug}-{counter}"
                counter += 1
            self.topic_id = topic_id
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{str(self.module.subject.name) if self.module and self.module.subject else ''} -> {str(self.title)}"


class CodeExample(models.Model):
    objects = models.Manager()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='examples')
    label = models.CharField(max_length=150)
    code = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:
        return f"{str(self.topic.title)} - {str(self.label)}"


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

    def __str__(self) -> str:
        return f"{str(self.topic.title)} - Lab #{self.order}: {str(self.title)} [{str(self.language)}]"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from apps.assignments.models import ProblemAccess
            ProblemAccess.objects.get_or_create(problem=self)


class TopicImage(models.Model):
    objects = models.Manager()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='images')
    image_url = models.TextField(help_text="Public Supabase Storage URL of the uploaded image")
    caption = models.CharField(max_length=300, blank=True, default="", help_text="Optional caption shown below image")
    order = models.PositiveIntegerField(default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:
        return f"{str(self.topic.title)} - Image #{self.order}"


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
    def student_count(self) -> int:
        return self.students.count()  # type: ignore[union-attr]

    def __str__(self) -> str:
        return f"{str(self.name)} ({str(self.course.name)}) - [{str(self.status)}]"


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

    def __str__(self) -> str:
        status = "DONE" if self.is_completed else "PENDING"
        return f"{str(self.batch.name)} - {str(self.topic.title)} [{status}]"


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

    def __str__(self) -> str:
        return f"{self.date} | {str(self.batch.name)} | {str(self.session_type)} ({self.students_attended}/{self.total_enrolled})"


class StudentAttendanceRecord(models.Model):
    objects = models.Manager()
    daily_log = models.ForeignKey(StaffDailyLog, on_delete=models.CASCADE, related_name='student_attendance_records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    is_present = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        unique_together = ('daily_log', 'student')

    def __str__(self) -> str:
        p = "Present" if self.is_present else "Absent"
        student_name = str(self.student.username) if self.student else "Unknown"  # type: ignore[union-attr]
        return f"{self.daily_log.date} - {student_name}: {p}"


class PlatformCapability(models.Model):
    """Feature/capability cards shown on the website homepage (e.g. '01 — Distributed Architecture')"""
    objects = models.Manager()
    number = models.CharField(
        max_length=5,
        help_text="Display number e.g. 01, 02, 03",
        default="01"
    )
    title = models.CharField(max_length=200, help_text="Card heading")
    description = models.TextField(help_text="Card body description shown on website")
    icon = models.CharField(
        max_length=50,
        blank=True,
        default="code",
        help_text="Icon identifier: code, layers, terminal, award, cpu, shield, database"
    )
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide from website")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Platform Capability / Feature Card"
        verbose_name_plural = "Platform Capabilities / Feature Cards"

    def __str__(self) -> str:
        return f"{str(self.number)} — {str(self.title)}"


class TopicQuizQuestion(models.Model):
    """MCQ Question in the Topic Question Bank (e.g. 20+ questions per topic)"""
    OPTION_CHOICES = (
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    )

    objects = models.Manager()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quiz_questions')
    question_text = models.TextField(help_text="The question prompt")
    option_a = models.TextField(help_text="Choice A")
    option_b = models.TextField(help_text="Choice B")
    option_c = models.TextField(help_text="Choice C")
    option_d = models.TextField(help_text="Choice D")
    correct_option = models.CharField(max_length=2, choices=OPTION_CHOICES, default='A', help_text="Correct answer letter (A, B, C, or D)")
    explanation = models.TextField(blank=True, default="", help_text="Detailed explanation shown during review")
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['topic', 'order', 'id']
        verbose_name = "Topic Quiz Question"
        verbose_name_plural = "Topic Quiz Questions"

    def __str__(self) -> str:
        return f"{self.topic.title} - Q#{self.order}: {self.question_text[:50]}"


class StudentTopicProgress(models.Model):
    """Tracks each student's progress and topic quiz pass/cooldown state"""
    objects = models.Manager()
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_progress_records')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='student_progress_records')
    is_completed = models.BooleanField(default=False, help_text="True if student scored >= 50% on the topic quiz")
    completed_at = models.DateTimeField(null=True, blank=True)
    attempts_count = models.PositiveIntegerField(default=0)
    last_score = models.PositiveIntegerField(default=0)
    last_total = models.PositiveIntegerField(default=5)
    last_percentage = models.FloatField(default=0.0)
    last_passed = models.BooleanField(default=False)
    can_reattempt_after = models.DateTimeField(
        null=True,
        blank=True,
        help_text="10-minute cooldown timestamp set if test was failed. Cannot re-attempt until this expires."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'topic')
        ordering = ['topic__order', 'id']
        verbose_name = "Student Topic Progress"
        verbose_name_plural = "Student Topic Progress Records"

    @property
    def is_in_cooldown(self) -> bool:
        if not self.can_reattempt_after:
            return False
        return timezone.now() < self.can_reattempt_after

    def cooldown_seconds_remaining(self) -> int:
        if not self.is_in_cooldown or not self.can_reattempt_after:
            return 0
        diff = (self.can_reattempt_after - timezone.now()).total_seconds()
        return max(0, int(diff))

    def __str__(self) -> str:
        status = "COMPLETED" if self.is_completed else "IN_PROGRESS"
        return f"{self.student.username} -> {self.topic.title} [{status}] (Attempts: {self.attempts_count})"


class TopicQuizAttempt(models.Model):
    """Detailed audit log of every topic test/quiz attempt taken by a student"""
    STATUS_CHOICES = (
        ('PASSED', 'Passed (>= 50%)'),
        ('FAILED_SCORE', 'Failed - Score Under 50%'),
        ('FAILED_SECURITY', 'Terminated - Security Violation (Tab switch / devtools)'),
    )

    objects = models.Manager()
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.PositiveIntegerField(default=0, help_text="Number of correct answers")
    total_questions = models.PositiveIntegerField(default=5, help_text="Total questions served in this attempt")
    percentage = models.FloatField(default=0.0, help_text="Percentage score achieved")
    is_passed = models.BooleanField(default=False, help_text="True if percentage >= 50.0")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='FAILED_SCORE')
    security_violations = models.PositiveIntegerField(default=0, help_text="Count of security infractions recorded")
    violation_details = models.TextField(blank=True, default="", help_text="Log of security warnings / exit triggers")
    questions_data = models.JSONField(default=list, blank=True, help_text="Snapshot of the 5 questions & choices served")
    selected_answers = models.JSONField(default=dict, blank=True, help_text="Map of question_id -> chosen option")
    time_taken_seconds = models.PositiveIntegerField(default=0, help_text="Time taken to finish the test")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Topic Quiz Attempt"
        verbose_name_plural = "Topic Quiz Attempts"

    def __str__(self) -> str:
        return f"{self.student.username} -> {self.topic.title}: {self.score}/{self.total_questions} ({self.percentage}%) [{self.status}]"

