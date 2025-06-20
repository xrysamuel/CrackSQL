# Comparison Result of './output/test_translated_jooq_high_school_dataset.json'

## Comparison result of sample 0

### Execution result of source SQL statement

```postgresql
SELECT * FROM students WHERE student_name LIKE '%王%';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0001           王丹   Class 04
     S0052           王娜   Class 20
     S0053           王飞   Class 12
     S0054           王超   Class 19
     S0055           王静   Class 07
(... 71 more rows not shown)


### Execution result of Target SQL statement

```mysql
select *
from students
where student_name like '%王%'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0001           王丹   Class 04
     S0052           王娜   Class 20
     S0053           王飞   Class 12
     S0054           王超   Class 19
     S0055           王静   Class 07
(... 71 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 1

### Execution result of source SQL statement

```postgresql
SELECT course_name FROM courses WHERE teacher_id = 'T001';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
course_name
        美术1


### Execution result of Target SQL statement

```mysql
select course_name
from courses
where teacher_id = 'T001'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
course_name
        美术1


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 2

### Execution result of source SQL statement

```postgresql
SELECT c.course_name, t.teacher_name FROM courses c JOIN teachers t ON c.teacher_id = t.teacher_id;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
course_name teacher_name
    人工智能概论1           王丹
    人工智能概论1           林晨
    人工智能概论1          陈桂珍
    人工智能概论2           陈玉
    人工智能概论2          冷淑华
(... 295 more rows not shown)


### Execution result of Target SQL statement

```mysql
select c.course_name, t.teacher_name
from courses as c
  join teachers as t
    on c.teacher_id = t.teacher_id
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
course_name teacher_name
    人工智能概论1           王丹
    人工智能概论1           林晨
    人工智能概论1          陈桂珍
    人工智能概论2           陈玉
    人工智能概论2          冷淑华
(... 295 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 3

### Execution result of source SQL statement

```postgresql
SELECT s.student_name, s.class_name FROM students s WHERE s.class_name = 'Class 04';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_name class_name
          关建   Class 04
          刘健   Class 04
          刘宇   Class 04
         刘小红   Class 04
          刘文   Class 04
(... 46 more rows not shown)


### Execution result of Target SQL statement

```mysql
select s.student_name, s.class_name
from students as s
where s.class_name = 'Class 04'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_name class_name
          关建   Class 04
          刘健   Class 04
          刘宇   Class 04
         刘小红   Class 04
          刘文   Class 04
(... 46 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 4

### Execution result of source SQL statement

```postgresql
UPDATE students SET class_name = 'Class 05' WHERE student_id = 'S0001';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 05
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```mysql
update students
set
  class_name = 'Class 05'
where student_id = 'S0001'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 05
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---


## Comparison result of sample 5

### Execution result of source SQL statement

```postgresql
UPDATE teachers SET teacher_name = '吴丽丽' WHERE teacher_id = 'T001';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴丽丽
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```mysql
update teachers
set
  teacher_name = '吴丽丽'
where teacher_id = 'T001'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴丽丽
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---


## Comparison result of sample 6

### Execution result of source SQL statement

```postgresql
UPDATE courses SET teacher_id = 'T006' WHERE course_id = 'C001';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T006
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```mysql
update courses
set
  teacher_id = 'T006'
where course_id = 'C001'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T006
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---


## Comparison result of sample 7

### Execution result of source SQL statement

```postgresql
DELETE FROM students WHERE student_id = 'S0010';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 994 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```mysql
delete from students
where student_id = 'S0010'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 994 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---


## Comparison result of sample 8

### Execution result of source SQL statement

```postgresql
DELETE FROM teachers WHERE teacher_id = 'T010';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 94 more rows not shown)


### Execution result of Target SQL statement

```mysql
delete from teachers
where teacher_id = 'T010'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 94 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---


## Comparison result of sample 9

### Execution result of source SQL statement

```postgresql
DELETE FROM courses WHERE course_id = 'C009';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 294 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```mysql
delete from courses
where course_id = 'C009'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 294 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---


## Comparison result of sample 10

### Execution result of source SQL statement

```postgresql
SELECT student_id, student_name, class_name FROM (SELECT student_id, student_name, class_name, ROW_NUMBER() OVER (PARTITION BY class_name ORDER BY student_id) as rn FROM students) AS sub WHERE rn = 1;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0006           徐萍   Class 05
(... 15 more rows not shown)


### Execution result of Target SQL statement

```mysql
select student_id, student_name, class_name
from (
  select
    student_id,
    student_name,
    class_name,
    row_number() over (
      partition by class_name
      order by student_id
    ) as rn
  from students
) as sub
where rn = 1
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0006           徐萍   Class 05
(... 15 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 11

### Execution result of source SQL statement

```postgresql
SELECT T.teacher_name, C.course_name FROM teachers T JOIN LATERAL (SELECT course_name, course_id FROM courses WHERE teacher_id = T.teacher_id ORDER BY course_id DESC LIMIT 1) AS C ON TRUE;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
teacher_name course_name
         亢秀兰       通用技术2
          任博     数据科学基础1
          余杰       编程入门1
         冷淑华       社会实践4
         刘小红       哲学基础4
(... 93 more rows not shown)


### Execution result of Target SQL statement

```mysql
select T.teacher_name, C.course_name
from teachers as T
  join lateral (
    select course_name, course_id
    from courses
    where teacher_id = T.teacher_id
    order by course_id desc
    limit 1
  ) as C
    on true
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
teacher_name course_name
         亢秀兰       通用技术2
          任博     数据科学基础1
          余杰       编程入门1
         冷淑华       社会实践4
         刘小红       哲学基础4
(... 93 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 12

### Execution result of source SQL statement

```postgresql
SELECT DISTINCT ON (class_name) student_id, student_name, class_name FROM students ORDER BY class_name, student_id;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0006           徐萍   Class 05
(... 15 more rows not shown)


### Execution result of Target SQL statement

```mysql
select t.student_id, t.student_name, t.class_name
from (
  select distinct
    student_id,
    student_name,
    class_name,
    row_number() over (
      partition by class_name
      order by class_name, student_id
    ) as `rn`
  from students
) as t
where `rn` = 1
order by class_name, student_id
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0006           徐萍   Class 05
(... 15 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 13

### Execution result of source SQL statement

```postgresql
SELECT REGEXP_REPLACE(course_name, '\d+$', '') AS  base_course_name, COUNT(*) AS course_count FROM courses GROUP BY base_course_name ORDER BY course_count DESC;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
base_course_name  course_count
          人工智能概论            16
              体育            15
            信息技术            13
            创新思维             9
              化学            15
(... 20 more rows not shown)


### Execution result of Target SQL statement

```mysql
select
  regexp_replace(course_name, '\\d+$', '', 1, 1) as base_course_name,
  count(*) as course_count
from courses
group by base_course_name
order by course_count desc
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
base_course_name  course_count
          人工智能概论            16
              体育            15
            信息技术            13
            创新思维             9
              化学            15
(... 20 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 14

### Execution result of source SQL statement

```postgresql
ALTER TABLE students ADD PRIMARY KEY (student_id); INSERT INTO students (student_id, student_name, class_name) VALUES ('S0002', '张伟', 'Class 02') ON CONFLICT (student_id) DO UPDATE SET student_name = EXCLUDED.student_name, class_name = EXCLUDED.class_name;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           张伟   Class 02
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```mysql
alter table students add primary key (student_id);
insert into students (student_id, student_name, class_name)
values (
  'S0002', 
  '张伟', 
  'Class 02'
)
as `t`
on duplicate key update
  student_name = `t`.student_name,
  class_name = `t`.class_name;
```

--- Error Message ---
(1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'insert into students (student_id, student_name, class_name)\nvalues (\n  'S0002', ' at line 2")

### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): False
- Consistency of query results (@2): False
- Execution without errors (@3): False
- All correct (@4): False

--- Database Table Comparison ---
Unique to self: courses, students, teachers

--- Result Table Comparison ---


## Comparison result of sample 15

### Execution result of source SQL statement

```postgresql
INSERT INTO courses (course_id, course_name, teacher_id) VALUES ('C999', '数据结构', 'T001') RETURNING course_id;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 296 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
course_id
     C999


### Execution result of Target SQL statement

```mysql
insert into courses (course_id, course_name, teacher_id)
values (
  'C999', 
  '数据结构', 
  'T001'
)
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 296 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): False
- Execution without errors (@3): True
- All correct (@4): False

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
Unique to self: result


## Comparison result of sample 16

### Execution result of source SQL statement

```postgresql
SELECT t.teacher_name, JSONB_AGG(JSONB_BUILD_OBJECT('course_id', c.course_id, 'course_name', c.course_name)) AS courses_taught FROM teachers t JOIN courses c ON t.teacher_id = c.teacher_id GROUP BY t.teacher_name;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
teacher_name                                                                                                                                                                                                                                                                       courses_taught
         亢秀兰                                                                                                                                          [{'course_id': 'C130', 'course_name': '通用技术3'}, {'course_id': 'C237', 'course_name': '美术2'}, {'course_id': 'C292', 'course_name': '通用技术2'}]
          任博                                                                                                                                      [{'course_id': 'C120', 'course_name': '人工智能概论5'}, {'course_id': 'C219', 'course_name': '物理3'}, {'course_id': 'C264', 'course_name': '数据科学基础1'}]
          余杰 [{'course_id': 'C011', 'course_name': '信息技术4'}, {'course_id': 'C048', 'course_name': '体育1'}, {'course_id': 'C093', 'course_name': '心理健康1'}, {'course_id': 'C102', 'course_name': '生物1'}, {'course_id': 'C154', 'course_name': '化学5'}, {'course_id': 'C246', 'course_name': '编程入门1'}]
         冷淑华                                                                                                                                        [{'course_id': 'C025', 'course_name': '地理3'}, {'course_id': 'C098', 'course_name': '人工智能概论2'}, {'course_id': 'C255', 'course_name': '社会实践4'}]
         刘小红                                                                                                                                                                                       [{'course_id': 'C109', 'course_name': '心理健康3'}, {'course_id': 'C239', 'course_name': '哲学基础4'}]
(... 90 more rows not shown)


### Execution result of Target SQL statement

```mysql
set @t = @@group_concat_max_len;
set @@group_concat_max_len = 4294967295;
select
  t.teacher_name,
  json_merge_preserve(
    '[]',
    concat(
      '[',
      group_concat(json_object(
        'course_id', c.course_id,
        'course_name', c.course_name
      ) separator ','),
      ']'
    )
  ) as courses_taught
from teachers as t
  join courses as c
    on t.teacher_id = c.teacher_id
group by t.teacher_name;
set @@group_concat_max_len = @t;
```

--- Error Message ---
(1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'set @@group_concat_max_len = 4294967295;\nselect\n  t.teacher_name,\n  json_merge_p' at line 2")

### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): False
- Consistency of query results (@2): False
- Execution without errors (@3): False
- All correct (@4): False

--- Database Table Comparison ---
Unique to self: courses, students, teachers

--- Result Table Comparison ---
Unique to self: result


## Comparison result of sample 17

### Execution result of source SQL statement

```postgresql
SELECT t.teacher_name, COALESCE(STRING_AGG(c.course_name, ', '), '无课程') AS courses FROM teachers t LEFT JOIN courses c ON t.teacher_id = c.teacher_id GROUP BY t.teacher_name;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
teacher_name                            courses
         亢秀兰                  通用技术3, 美术2, 通用技术2
          任博              人工智能概论5, 物理3, 数据科学基础1
          余杰 信息技术4, 体育1, 心理健康1, 生物1, 化学5, 编程入门1
         冷淑华                地理3, 人工智能概论2, 社会实践4
         刘小红                       心理健康3, 哲学基础4
(... 92 more rows not shown)


### Execution result of Target SQL statement

```mysql
set @t = @@group_concat_max_len;
set @@group_concat_max_len = 4294967295;
select
  t.teacher_name,
  coalesce(
    group_concat(c.course_name separator ', '),
    '无课程'
  ) as courses
from teachers as t
  left outer join courses as c
    on t.teacher_id = c.teacher_id
group by t.teacher_name;
set @@group_concat_max_len = @t;
```

--- Error Message ---
(1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'set @@group_concat_max_len = 4294967295;\nselect\n  t.teacher_name,\n  coalesce(\n  ' at line 2")

### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): False
- Consistency of query results (@2): False
- Execution without errors (@3): False
- All correct (@4): False

--- Database Table Comparison ---
Unique to self: courses, students, teachers

--- Result Table Comparison ---
Unique to self: result


## Comparison result of sample 18

### Execution result of source SQL statement

```postgresql
SELECT student_name, class_name FROM students WHERE student_name ~ '王';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_name class_name
          王丹   Class 04
          王丹   Class 08
          王丹   Class 18
         王丹丹   Class 17
          王丽   Class 05
(... 71 more rows not shown)


### Execution result of Target SQL statement

```mysql
select student_name, class_name
from students
where student_name regexp '王'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_name class_name
          王丹   Class 04
          王丹   Class 08
          王丹   Class 18
         王丹丹   Class 17
          王丽   Class 05
(... 71 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 19

### Execution result of source SQL statement

```postgresql
WITH ClassStudents AS (SELECT class_name, ARRAY_AGG(student_name ORDER BY student_name) AS student_names FROM students GROUP BY class_name) SELECT * FROM ClassStudents WHERE '王丹' = ANY(student_names);
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
class_name                                                                                                                                                                                                                                                                                         student_names
  Class 04                                                                              [关建, 刘健, 刘宇, 刘小红, 刘文, 刘波, 刘玉珍, 华建, 吕俊, 周莹, 廉荣, 廖晨, 张淑兰, 张鹏, 徐红霞, 朱想, 李亮, 李建, 李建, 李淑兰, 李莉, 李萍, 李霞, 杜成, 杨波, 林慧, 汪桂兰, 潘强, 焦洁, 王丹, 王静, 田杰, 瞿楠, 罗红, 花兰英, 蓝荣, 袁成, 贺璐, 赖琳, 赵丹丹, 赵英, 赵雪, 邓秀芳, 郭桂荣, 郭玉华, 金伟, 钱建, 阎柳, 陈楠, 陈雪梅, 韩俊]
  Class 08 [万帅, 倪秀芳, 刘丹, 刘凤兰, 刘桂珍, 刘楠, 刘玲, 刘磊, 刘芳, 卢娟, 卫红霞, 印玉英, 吴博, 周畅, 孙琳, 常超, 张楠, 张浩, 徐红梅, 成文, 戴丽, 方波, 朱桂英, 朱琴, 李丽丽, 李敏, 李旭, 李欣, 李秀英, 李颖, 林林, 梁春梅, 梁秀云, 樊帅, 汪婷婷, 洪玉梅, 涂玉梅, 王丹, 王彬, 王欣, 王洁, 王秀珍, 王荣, 王鹏, 白红霞, 祝玉, 秦明, 管建国, 罗秀英, 舒霞, 苑桂兰, 苗雷, 范云, 萧俊, 袁帅, 贾桂荣, 邹艳, 郑婷婷, 郝小红, 郭凤兰, 金英, 陈斌, 韦超, 马琴, 黄桂珍, 黄玉兰, 黄超]
  Class 18                [何丽, 何婷婷, 冯婷婷, 刘淑兰, 刘艳, 刘雷, 华红, 叶华, 周慧, 夏颖, 孙亮, 孟桂香, 宁倩, 寇建华, 庄欣, 张丹, 张春梅, 张春梅, 张林, 张桂兰, 张秀兰, 张秀华, 张秀华, 张红霞, 徐峰, 文丽, 方杰, 曹秀英, 李帆, 李敏, 李秀珍, 李秀英, 杨建军, 桂婷, 梁建国, 段利, 毛莉, 江峰, 汪丽娟, 洪丹, 洪欢, 潘志强, 王丹, 王淑华, 王燕, 田佳, 秦雷, 苏晶, 蒋燕, 谢飞, 赵凤英, 郎淑兰, 郑丽华, 郭玉, 陈宁, 陈春梅, 陈杨, 陈秀芳, 韩晶, 魏文, 黎峰, 黎桂香, 龙宇]


### Execution result of Target SQL statement

```mysql
with
  ClassStudents as (
    select
      class_name,
      array_agg(student_name order by student_name) as student_names
    from students
    group by class_name
  )
select *
from ClassStudents
where '王丹' = student_names
```

--- Error Message ---
(1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'order by student_name) as student_names\n    from students\n    group by class_nam' at line 5")

### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): False
- Consistency of query results (@2): False
- Execution without errors (@3): False
- All correct (@4): False

--- Database Table Comparison ---
Unique to self: courses, students, teachers

--- Result Table Comparison ---
Unique to self: result


## Comparison result of sample 20

### Execution result of source SQL statement

```postgresql
UPDATE courses SET course_name = course_name || ' (修订版)' WHERE course_id = 'C001';
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001   体育3 (修订版)       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```mysql
update courses
set
  course_name = concat(
    cast(course_name as char),
    ' (修订版)'
  )
where course_id = 'C001'
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001   体育3 (修订版)       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---


## Comparison result of sample 21

### Execution result of source SQL statement

```mysql
REPLACE INTO courses (course_id, course_name, teacher_id) VALUES ('C002', '数据结构', 'T001');
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002        数据结构       T001
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
(... 296 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)


### Execution result of Target SQL statement

```postgresql
REPLACE not yet implemented. If you're interested in this feature, please comment on https://github.com/jOOQ/jOOQ/issues/16487: [1:9] REPLACE [*]INTO courses (course_id, course_name, teacher_id) VALUES ('C002', '数据结构', 'T001'...
```

--- Error Message ---
syntax error at or near "REPLACE"
LINE 1: REPLACE not yet implemented. If you're interested in this fe...
        ^


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): False
- Consistency of query results (@2): False
- Execution without errors (@3): False
- All correct (@4): False

--- Database Table Comparison ---
Unique to self: courses, students, teachers

--- Result Table Comparison ---


## Comparison result of sample 22

### Execution result of source SQL statement

```mysql
SELECT t.teacher_name, GROUP_CONCAT(c.course_name SEPARATOR ' | ') AS courses_taught FROM teachers t LEFT JOIN courses c ON t.teacher_id = c.teacher_id GROUP BY t.teacher_name;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
teacher_name                          courses_taught
         亢秀兰                     通用技术3 | 美术2 | 通用技术2
          任博                 物理3 | 数据科学基础1 | 人工智能概论5
          余杰 信息技术4 | 体育1 | 心理健康1 | 生物1 | 化学5 | 编程入门1
         冷淑华                   社会实践4 | 人工智能概论2 | 地理3
         刘小红                           心理健康3 | 哲学基础4
(... 92 more rows not shown)


### Execution result of Target SQL statement

```postgresql
select
  t.teacher_name,
  string_agg(cast(c.course_name as varchar), ' | ') as courses_taught
from teachers as t
  left outer join courses as c
    on t.teacher_id = c.teacher_id
group by t.teacher_name
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
teacher_name                          courses_taught
         亢秀兰                     通用技术3 | 美术2 | 通用技术2
          任博                 人工智能概论5 | 物理3 | 数据科学基础1
          余杰 信息技术4 | 体育1 | 心理健康1 | 生物1 | 化学5 | 编程入门1
         冷淑华                   地理3 | 人工智能概论2 | 社会实践4
         刘小红                           心理健康3 | 哲学基础4
(... 92 more rows not shown)


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): False
- Execution without errors (@3): True
- All correct (@4): False

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
Differences in table 'result':
@ (row: 1, col: courses_taught): self: 物理3 | 数据科学基础1 | 人工智能概论5, other: 人工智能概论5 | 物理3 | 数据科学基础1
@ (row: 3, col: courses_taught): self: 社会实践4 | 人工智能概论2 | 地理3, other: 地理3 | 人工智能概论2 | 社会实践4
@ (row: 5, col: courses_taught): self: 艺术鉴赏2 | 编程入门1 | 英语4, other: 英语4 | 编程入门1 | 艺术鉴赏2
@ (row: 7, col: courses_taught): self: 音乐3 | 化学5 | 美术1 | 地理4 | 心理健康1 | 艺术鉴赏3, other: 地理4 | 心理健康1 | 艺术鉴赏3 | 音乐3 | 美术1 | 化学5
@ (row: 8, col: courses_taught): self: 通用技术1 | 体育3, other: 体育3 | 通用技术1
@ (row: 9, col: courses_taught): self: 化学1 | 编程入门1 | 艺术鉴赏4 | 数学3 | 通用技术1 | 社会实践4, other: 社会实践4 | 通用技术1 | 数学3 | 艺术鉴赏4 | 编程入门1 | 化学1
@ (row: 13, col: courses_taught): self: 数学5 | 数学1, other: 数学1 | 数学5
@ (row: 14, col: courses_taught): self: 数学4 | 体育3 | 生涯规划2 | 物理4 | 信息技术4 | 美术2 | 生物3 | 信息技术1, other: 体育3 | 物理4 | 信息技术4 | 美术2 | 生物3 | 生涯规划2 | 数学4 | 信息技术1
@ (row: 15, col: courses_taught): self: 美术2 | 语文4 | 形体与健康4 | 数据科学基础3, other: 形体与健康4 | 数据科学基础3 | 语文4 | 美术2
@ (row: 16, col: courses_taught): self: 心理健康3 | 经济学原理4, other: 经济学原理4 | 心理健康3
...


## Comparison result of sample 23

### Execution result of source SQL statement

```mysql
SELECT student_id, student_name, class_name FROM students LIMIT 10, 5;
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0011           毛燕   Class 14
     S0012           姚佳   Class 02
     S0013           李英   Class 01
     S0014           梁波   Class 03
     S0015          田桂兰   Class 07


### Execution result of Target SQL statement

```postgresql
select student_id, student_name, class_name
from students
offset 10 rows
fetch next 5 rows only
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_id student_name class_name
     S0011           毛燕   Class 14
     S0012           姚佳   Class 02
     S0013           李英   Class 01
     S0014           梁波   Class 03
     S0015          田桂兰   Class 07


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): True
- Consistency of query results (@2): True
- Execution without errors (@3): True
- All correct (@4): True

--- Database Table Comparison ---
courses: No differences between self and other
students: No differences between self and other
teachers: No differences between self and other

--- Result Table Comparison ---
result: No differences between self and other


## Comparison result of sample 24

### Execution result of source SQL statement

```mysql
SELECT student_name, class_name FROM students WHERE FIND_IN_SET(class_name, 'Class 01,Class 04,Class 09');
```

--- Database Tables ---
Table: courses
course_id course_name teacher_id
     C001         体育3       T076
     C002     人工智能概论4       T020
     C003       心理健康5       T062
     C004         音乐3       T071
     C005       创新思维5       T049
(... 295 more rows not shown)

Table: students
student_id student_name class_name
     S0001           王丹   Class 04
     S0002           刘旭   Class 01
     S0003           宋超   Class 09
     S0004           李敏   Class 08
     S0005          郑婷婷   Class 08
(... 995 more rows not shown)

Table: teachers
teacher_id teacher_name
      T001          吴婷婷
      T002          樊金凤
      T003          黄淑珍
      T004           段芳
      T005           徐超
(... 95 more rows not shown)

--- Result Tables ---
Table: result
student_name class_name
          何利   Class 09
         何桂珍   Class 01
          倪刚   Class 09
          关建   Class 04
         冯秀华   Class 09
(... 155 more rows not shown)


### Execution result of Target SQL statement

```postgresql
Boolean field expected: [1:106] ...D_IN_SET(class_name, 'Class 01,Class 04,Class 09')[*];
```

--- Error Message ---
syntax error at or near "Boolean"
LINE 1: Boolean field expected: [1:106] ...D_IN_SET(class_name, 'Cla...
        ^


### Equivalence of the two execution results
- Consistency of data in the database after execution (@1): False
- Consistency of query results (@2): False
- Execution without errors (@3): False
- All correct (@4): False

--- Database Table Comparison ---
Unique to self: courses, students, teachers

--- Result Table Comparison ---
Unique to self: result

