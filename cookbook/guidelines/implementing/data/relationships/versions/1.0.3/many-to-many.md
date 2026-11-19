
Use a junction table with FKs to both parent tables. The junction table's PK SHOULD be a composite of both FKs:

```sql
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    title     TEXT NOT NULL
);

CREATE TABLE enrollments (
    student_id  INTEGER NOT NULL REFERENCES students(student_id),
    course_id   INTEGER NOT NULL REFERENCES courses(course_id),
    enrolled_on TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (student_id, course_id)
);
```

Add additional indexes if you query the junction from either direction:

```sql
CREATE INDEX ix_enrollments_course_id ON enrollments(course_id);
```

