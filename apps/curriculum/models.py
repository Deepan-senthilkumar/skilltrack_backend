from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(help_text="Detailed course/subject overview")
    short_description = models.CharField(max_length=255, blank=True, default="")
    icon = models.CharField(max_length=50, default="code", help_text="Icon identifier e.g. django, python, code, database")
    banner_image = models.TextField(blank=True, default="")
    instructor_name = models.CharField(max_length=150, default="Lead Instructor")
    level = models.CharField(max_length=50, default="Beginner to Advanced")
    duration = models.CharField(max_length=50, default="8 Weeks")
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class Module(models.Model):
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
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    topic_id = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    explain = models.JSONField(default=list, help_text="List of explanation paragraphs (Tamil-English)")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['module__order', 'order', 'id']

    def __str__(self):
        return f"{self.module.name} - {self.title}"


class CodeExample(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='examples')
    label = models.CharField(max_length=150)
    code = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.topic.title} - {self.label}"


class Problem(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Detailed problem requirements / lab tasks")
    expected_output_hint = models.TextField(blank=True, default="")
    starter_code = models.TextField(blank=True, default="")
    test_criteria = models.JSONField(default=list, blank=True, help_text="Automated test criteria list")
    expected_keywords = models.JSONField(default=list, blank=True, help_text="Required code/output tokens")
    points = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.topic.title} - Lab #{self.order}: {self.title}"
