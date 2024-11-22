% Load required modules
:- use_module(library(csv)).
:- use_module(library(http/http_server)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/json)).
:- dynamic student/3.

% Load CSV data into Prolog
load_csv_data(File) :-
    csv_read_file(File, Rows, [functor(student), arity(3)]),
    maplist(assert, Rows).

% Rule to check scholarship eligibility
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance_percentage, CGPA),
    Attendance_percentage >= 75,
    CGPA >= 9.0.

% Rule to check exam permission
permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance_percentage, _),
    Attendance_percentage >= 75.

% Add CORS headers to responses
add_cors_headers :-
    format('Access-Control-Allow-Origin: *~n'),
    format('Access-Control-Allow-Methods: GET, POST, OPTIONS~n'),
    format('Access-Control-Allow-Headers: Content-Type~n').

% Wrap HTTP replies with CORS headers
cors_reply_json_dict(Dict) :-
    add_cors_headers,
    reply_json_dict(Dict).

% Start the HTTP server
start_server(Port) :-
    http_server([port(Port)]).

% Define HTTP handlers
:- http_handler('/check_scholarship', check_scholarship_handler, []).
:- http_handler('/check_exam_permission', check_exam_permission_handler, []).
:- http_handler('/get_student_details', get_student_details_handler, []).

% Scholarship eligibility handler
check_scholarship_handler(Request) :-
    http_parameters(Request, [student_id(Student_ID_Atom, [atom])]),
    atom_number(Student_ID_Atom, Student_ID), 
    (eligible_for_scholarship(Student_ID) ->
        Reply = _{status: "eligible"};
        Reply = _{status: "not_eligible"}
    ),
    cors_reply_json_dict(Reply).

% Exam permission handler
check_exam_permission_handler(Request) :-
    http_parameters(Request, [student_id(Student_ID_Atom, [atom])]),
    atom_number(Student_ID_Atom, Student_ID), 
    (permitted_for_exam(Student_ID) ->
        Reply = _{status: "permitted"};
        Reply = _{status: "not_permitted"}
    ),
    cors_reply_json_dict(Reply).

% Handler to fetch student details
get_student_details_handler(Request) :-
    http_parameters(Request, [student_id(Student_ID_Atom, [atom])]),
    atom_number(Student_ID_Atom, Student_ID), 
    (student(Student_ID, Attendance_percentage, CGPA) ->
        Reply = _{student_id: Student_ID, attendance: Attendance_percentage, cgpa: CGPA};
        Reply = _{error: "Student not found"}
    ),
    cors_reply_json_dict(Reply).

% Initialize the system by loading the CSV and starting the server
initialize(File, Port) :-
    load_csv_data(File),
    start_server(Port).
