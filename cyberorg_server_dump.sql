--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Debian 14.18-1.pgdg120+1)
-- Dumped by pg_dump version 14.18 (Debian 14.18-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO cyberorg;

--
-- Name: known_task_number; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.known_task_number (
    id integer NOT NULL,
    student_id integer NOT NULL,
    task_number integer NOT NULL
);


ALTER TABLE public.known_task_number OWNER TO cyberorg;

--
-- Name: known_task_number_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.known_task_number_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.known_task_number_id_seq OWNER TO cyberorg;

--
-- Name: known_task_number_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.known_task_number_id_seq OWNED BY public.known_task_number.id;


--
-- Name: maintenance_mode; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.maintenance_mode (
    id integer NOT NULL,
    is_enabled boolean NOT NULL,
    message text,
    enabled_by_id integer,
    enabled_at timestamp without time zone,
    disabled_at timestamp without time zone
);


ALTER TABLE public.maintenance_mode OWNER TO cyberorg;

--
-- Name: maintenance_mode_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.maintenance_mode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.maintenance_mode_id_seq OWNER TO cyberorg;

--
-- Name: maintenance_mode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.maintenance_mode_id_seq OWNED BY public.maintenance_mode.id;


--
-- Name: oge_parallel_plan; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.oge_parallel_plan (
    id integer NOT NULL,
    student_id integer NOT NULL,
    webinars_per_week integer NOT NULL,
    created_at timestamp without time zone,
    created_by_id integer NOT NULL,
    is_active boolean,
    hard_prog_webinars_per_week integer
);


ALTER TABLE public.oge_parallel_plan OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.oge_parallel_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oge_parallel_plan_id_seq OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.oge_parallel_plan_id_seq OWNED BY public.oge_parallel_plan.id;


--
-- Name: oge_parallel_plan_slot; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.oge_parallel_plan_slot (
    id integer NOT NULL,
    plan_id integer NOT NULL,
    slot_number integer NOT NULL,
    current_topic_id integer,
    current_topic_position integer,
    is_completed boolean
);


ALTER TABLE public.oge_parallel_plan_slot OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_slot_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.oge_parallel_plan_slot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oge_parallel_plan_slot_id_seq OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_slot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.oge_parallel_plan_slot_id_seq OWNED BY public.oge_parallel_plan_slot.id;


--
-- Name: oge_parallel_plan_topic_order; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.oge_parallel_plan_topic_order (
    id integer NOT NULL,
    plan_id integer NOT NULL,
    topic_id integer NOT NULL,
    order_index integer NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.oge_parallel_plan_topic_order OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_topic_order_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.oge_parallel_plan_topic_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oge_parallel_plan_topic_order_id_seq OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_topic_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.oge_parallel_plan_topic_order_id_seq OWNED BY public.oge_parallel_plan_topic_order.id;


--
-- Name: oge_parallel_plan_webinar; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.oge_parallel_plan_webinar (
    id integer NOT NULL,
    plan_id integer NOT NULL,
    webinar_id integer NOT NULL,
    slot_number integer NOT NULL,
    week_number integer NOT NULL,
    topic_id integer,
    position_in_topic integer NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.oge_parallel_plan_webinar OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_webinar_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.oge_parallel_plan_webinar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oge_parallel_plan_webinar_id_seq OWNER TO cyberorg;

--
-- Name: oge_parallel_plan_webinar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.oge_parallel_plan_webinar_id_seq OWNED BY public.oge_parallel_plan_webinar.id;


--
-- Name: oge_topic; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.oge_topic (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    task_numbers_str character varying(100),
    description text,
    is_active boolean,
    created_at timestamp without time zone,
    is_hard_prog boolean,
    priority integer
);


ALTER TABLE public.oge_topic OWNER TO cyberorg;

--
-- Name: oge_topic_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.oge_topic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oge_topic_id_seq OWNER TO cyberorg;

--
-- Name: oge_topic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.oge_topic_id_seq OWNED BY public.oge_topic.id;


--
-- Name: oge_topic_order; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.oge_topic_order (
    id integer NOT NULL,
    topic_id integer NOT NULL,
    order_index integer NOT NULL,
    is_active boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.oge_topic_order OWNER TO cyberorg;

--
-- Name: oge_topic_order_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.oge_topic_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oge_topic_order_id_seq OWNER TO cyberorg;

--
-- Name: oge_topic_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.oge_topic_order_id_seq OWNED BY public.oge_topic_order.id;


--
-- Name: planned_webinar; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.planned_webinar (
    id integer NOT NULL,
    study_plan_id integer NOT NULL,
    webinar_id integer NOT NULL,
    week_number integer NOT NULL
);


ALTER TABLE public.planned_webinar OWNER TO cyberorg;

--
-- Name: planned_webinar_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.planned_webinar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planned_webinar_id_seq OWNER TO cyberorg;

--
-- Name: planned_webinar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.planned_webinar_id_seq OWNED BY public.planned_webinar.id;


--
-- Name: student; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.student (
    id integer NOT NULL,
    first_name character varying(64),
    last_name character varying(64),
    platform_id character varying(100) NOT NULL,
    registration_date timestamp without time zone,
    target_score integer,
    hours_per_week integer,
    notes text,
    is_active boolean,
    initial_score integer,
    needs_python_basics boolean,
    task_26_deferred boolean,
    task_27_deferred boolean,
    academic_year integer NOT NULL,
    exam_type character varying(10) NOT NULL,
    grade integer,
    tariff character varying(50),
    course character varying(50)
);


ALTER TABLE public.student OWNER TO cyberorg;

--
-- Name: student_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_id_seq OWNER TO cyberorg;

--
-- Name: student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.student_id_seq OWNED BY public.student.id;


--
-- Name: study_plan; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.study_plan (
    id integer NOT NULL,
    student_id integer NOT NULL,
    created_at timestamp without time zone,
    created_by_id integer NOT NULL
);


ALTER TABLE public.study_plan OWNER TO cyberorg;

--
-- Name: study_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.study_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.study_plan_id_seq OWNER TO cyberorg;

--
-- Name: study_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.study_plan_id_seq OWNED BY public.study_plan.id;


--
-- Name: task_number; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.task_number (
    id integer NOT NULL,
    number integer NOT NULL
);


ALTER TABLE public.task_number OWNER TO cyberorg;

--
-- Name: task_number_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.task_number_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_number_id_seq OWNER TO cyberorg;

--
-- Name: task_number_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.task_number_id_seq OWNED BY public.task_number.id;


--
-- Name: update_notification; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.update_notification (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    version character varying(50),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by_id integer NOT NULL,
    is_active boolean,
    priority integer,
    show_until timestamp without time zone,
    background_color character varying(20),
    text_color character varying(20),
    icon character varying(50)
);


ALTER TABLE public.update_notification OWNER TO cyberorg;

--
-- Name: update_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.update_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.update_notification_id_seq OWNER TO cyberorg;

--
-- Name: update_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.update_notification_id_seq OWNED BY public.update_notification.id;


--
-- Name: update_notification_image; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.update_notification_image (
    id integer NOT NULL,
    notification_id integer NOT NULL,
    image_url character varying(500) NOT NULL,
    caption character varying(300),
    "position" integer
);


ALTER TABLE public.update_notification_image OWNER TO cyberorg;

--
-- Name: update_notification_image_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.update_notification_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.update_notification_image_id_seq OWNER TO cyberorg;

--
-- Name: update_notification_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.update_notification_image_id_seq OWNED BY public.update_notification_image.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password_hash character varying(256),
    role character varying(50) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    last_login timestamp without time zone
);


ALTER TABLE public.users OWNER TO cyberorg;

--
-- Name: user; Type: VIEW; Schema: public; Owner: cyberorg
--

CREATE VIEW public."user" AS
 SELECT users.id,
    users.username,
    users.password_hash,
    users.role,
    users.first_name,
    users.last_name,
    users.last_login
   FROM public.users;


ALTER TABLE public."user" OWNER TO cyberorg;

--
-- Name: user_notification_status; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.user_notification_status (
    id integer NOT NULL,
    user_id integer NOT NULL,
    notification_id integer NOT NULL,
    viewed_at timestamp without time zone,
    is_dismissed boolean
);


ALTER TABLE public.user_notification_status OWNER TO cyberorg;

--
-- Name: user_notification_status_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.user_notification_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_notification_status_id_seq OWNER TO cyberorg;

--
-- Name: user_notification_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.user_notification_status_id_seq OWNED BY public.user_notification_status.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO cyberorg;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: watched_webinar; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.watched_webinar (
    id integer NOT NULL,
    student_id integer NOT NULL,
    webinar_id integer NOT NULL,
    watched_at timestamp without time zone,
    created_by_id integer NOT NULL
);


ALTER TABLE public.watched_webinar OWNER TO cyberorg;

--
-- Name: watched_webinar_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.watched_webinar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.watched_webinar_id_seq OWNER TO cyberorg;

--
-- Name: watched_webinar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.watched_webinar_id_seq OWNED BY public.watched_webinar.id;


--
-- Name: webinar; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.webinar (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    url character varying(500) NOT NULL,
    date date,
    is_programming boolean,
    is_manual boolean,
    is_excel boolean,
    homework_number integer,
    category integer,
    for_beginners boolean,
    for_basic boolean,
    for_advanced boolean,
    for_expert boolean,
    for_mocks boolean,
    for_practice boolean,
    for_minisnap boolean,
    created_by_id integer NOT NULL,
    cover_url character varying(500),
    academic_year integer NOT NULL,
    for_summer boolean,
    exam_type character varying(10) NOT NULL,
    for_oge_part1 boolean,
    for_oge_part2 boolean,
    for_oge_hard boolean
);


ALTER TABLE public.webinar OWNER TO cyberorg;

--
-- Name: webinar_comment; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.webinar_comment (
    id integer NOT NULL,
    text text NOT NULL,
    created_at timestamp without time zone,
    webinar_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.webinar_comment OWNER TO cyberorg;

--
-- Name: webinar_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.webinar_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.webinar_comment_id_seq OWNER TO cyberorg;

--
-- Name: webinar_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.webinar_comment_id_seq OWNED BY public.webinar_comment.id;


--
-- Name: webinar_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.webinar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.webinar_id_seq OWNER TO cyberorg;

--
-- Name: webinar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.webinar_id_seq OWNED BY public.webinar.id;


--
-- Name: webinar_oge_topic_association; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.webinar_oge_topic_association (
    webinar_id integer NOT NULL,
    oge_topic_id integer NOT NULL
);


ALTER TABLE public.webinar_oge_topic_association OWNER TO cyberorg;

--
-- Name: webinar_task; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.webinar_task (
    id integer NOT NULL,
    text text NOT NULL,
    webinar_id integer NOT NULL,
    created_at timestamp without time zone,
    created_by_id integer NOT NULL
);


ALTER TABLE public.webinar_task OWNER TO cyberorg;

--
-- Name: webinar_task_association; Type: TABLE; Schema: public; Owner: cyberorg
--

CREATE TABLE public.webinar_task_association (
    webinar_id integer NOT NULL,
    task_number_id integer NOT NULL
);


ALTER TABLE public.webinar_task_association OWNER TO cyberorg;

--
-- Name: webinar_task_id_seq; Type: SEQUENCE; Schema: public; Owner: cyberorg
--

CREATE SEQUENCE public.webinar_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.webinar_task_id_seq OWNER TO cyberorg;

--
-- Name: webinar_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cyberorg
--

ALTER SEQUENCE public.webinar_task_id_seq OWNED BY public.webinar_task.id;


--
-- Name: known_task_number id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.known_task_number ALTER COLUMN id SET DEFAULT nextval('public.known_task_number_id_seq'::regclass);


--
-- Name: maintenance_mode id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.maintenance_mode ALTER COLUMN id SET DEFAULT nextval('public.maintenance_mode_id_seq'::regclass);


--
-- Name: oge_parallel_plan id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan ALTER COLUMN id SET DEFAULT nextval('public.oge_parallel_plan_id_seq'::regclass);


--
-- Name: oge_parallel_plan_slot id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_slot ALTER COLUMN id SET DEFAULT nextval('public.oge_parallel_plan_slot_id_seq'::regclass);


--
-- Name: oge_parallel_plan_topic_order id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_topic_order ALTER COLUMN id SET DEFAULT nextval('public.oge_parallel_plan_topic_order_id_seq'::regclass);


--
-- Name: oge_parallel_plan_webinar id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_webinar ALTER COLUMN id SET DEFAULT nextval('public.oge_parallel_plan_webinar_id_seq'::regclass);


--
-- Name: oge_topic id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_topic ALTER COLUMN id SET DEFAULT nextval('public.oge_topic_id_seq'::regclass);


--
-- Name: oge_topic_order id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_topic_order ALTER COLUMN id SET DEFAULT nextval('public.oge_topic_order_id_seq'::regclass);


--
-- Name: planned_webinar id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.planned_webinar ALTER COLUMN id SET DEFAULT nextval('public.planned_webinar_id_seq'::regclass);


--
-- Name: student id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.student ALTER COLUMN id SET DEFAULT nextval('public.student_id_seq'::regclass);


--
-- Name: study_plan id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.study_plan ALTER COLUMN id SET DEFAULT nextval('public.study_plan_id_seq'::regclass);


--
-- Name: task_number id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.task_number ALTER COLUMN id SET DEFAULT nextval('public.task_number_id_seq'::regclass);


--
-- Name: update_notification id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.update_notification ALTER COLUMN id SET DEFAULT nextval('public.update_notification_id_seq'::regclass);


--
-- Name: update_notification_image id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.update_notification_image ALTER COLUMN id SET DEFAULT nextval('public.update_notification_image_id_seq'::regclass);


--
-- Name: user_notification_status id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.user_notification_status ALTER COLUMN id SET DEFAULT nextval('public.user_notification_status_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: watched_webinar id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.watched_webinar ALTER COLUMN id SET DEFAULT nextval('public.watched_webinar_id_seq'::regclass);


--
-- Name: webinar id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar ALTER COLUMN id SET DEFAULT nextval('public.webinar_id_seq'::regclass);


--
-- Name: webinar_comment id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_comment ALTER COLUMN id SET DEFAULT nextval('public.webinar_comment_id_seq'::regclass);


--
-- Name: webinar_task id; Type: DEFAULT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_task ALTER COLUMN id SET DEFAULT nextval('public.webinar_task_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.alembic_version (version_num) FROM stdin;
0042987a1260
\.


--
-- Data for Name: known_task_number; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.known_task_number (id, student_id, task_number) FROM stdin;
1	1	1
2	1	4
3	1	5
4	1	7
5	1	8
6	1	10
7	1	11
8	1	14
9	1	19
10	1	20
11	1	21
12	1	13
13	1	15
14	2	1
15	2	2
16	2	3
17	2	4
18	2	5
19	2	8
20	2	9
21	2	10
22	2	14
23	2	16
24	3	14
25	3	19
26	3	20
27	3	21
28	4	1
29	4	2
30	4	3
31	4	7
32	4	10
33	4	11
34	4	18
35	5	1
36	5	2
37	5	3
38	5	10
39	5	12
40	5	14
41	5	16
42	5	18
43	5	22
44	5	23
45	8	1
46	8	2
47	8	3
48	8	4
49	8	5
50	8	6
51	9	1
52	9	2
53	9	3
54	9	4
55	9	5
56	9	6
57	9	7
58	9	8
59	9	9
60	9	10
61	9	12
62	9	14
63	9	15
64	9	16
65	9	17
66	9	18
67	9	19
68	9	20
69	9	21
70	9	22
71	9	23
72	10	1
73	10	2
74	10	3
75	10	4
76	10	6
77	10	10
78	10	13
79	11	1
80	11	2
81	11	3
82	11	4
83	11	5
84	11	6
85	11	7
86	11	8
87	11	9
88	11	10
89	11	11
90	11	12
91	11	13
92	11	14
93	11	15
94	11	16
95	11	17
96	11	18
97	11	19
98	11	20
99	11	21
100	11	22
101	11	23
102	16	1
103	16	2
104	16	3
105	16	4
106	16	6
107	16	7
108	16	8
109	16	10
110	16	11
111	16	18
112	19	1
113	19	2
114	19	3
115	19	4
116	19	5
117	19	6
118	19	7
119	19	8
120	19	9
121	19	10
122	19	11
123	19	12
124	19	13
125	19	14
126	19	15
127	19	16
128	19	17
129	19	18
130	19	19
131	19	20
132	19	21
133	19	22
134	19	23
135	19	25
143	22	1
144	22	2
145	22	3
146	22	4
147	22	7
148	22	9
149	22	10
150	24	1
151	24	2
152	24	3
153	24	4
154	24	5
155	24	6
156	24	7
157	24	8
158	24	9
159	24	10
160	24	11
161	24	12
162	24	13
163	24	14
164	24	15
165	24	16
166	24	17
167	24	18
168	24	19
169	24	20
170	24	21
216	25	1
217	25	2
218	25	3
219	25	4
220	25	5
221	25	6
222	25	8
223	25	10
224	25	11
225	25	12
226	25	13
227	25	14
228	25	15
229	25	16
230	25	18
231	25	19
232	25	20
233	25	21
260	26	1
261	26	2
262	26	3
263	26	4
264	26	5
265	26	6
266	26	8
267	26	9
268	26	10
269	26	11
270	26	12
271	26	13
272	26	14
273	26	15
274	26	16
275	26	17
276	26	18
277	26	19
278	26	20
279	26	21
280	26	22
281	26	23
\.


--
-- Data for Name: maintenance_mode; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.maintenance_mode (id, is_enabled, message, enabled_by_id, enabled_at, disabled_at) FROM stdin;
1	f	Коржик усердно работает, чтобы поскорее выпустить обновление ❤️ Скоро вернёмся!	1	2025-09-12 13:40:15.904561	2025-09-12 16:31:37.172703
\.


--
-- Data for Name: oge_parallel_plan; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.oge_parallel_plan (id, student_id, webinars_per_week, created_at, created_by_id, is_active, hard_prog_webinars_per_week) FROM stdin;
2	32	2	2025-09-12 15:33:08.623656	1	t	0
\.


--
-- Data for Name: oge_parallel_plan_slot; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.oge_parallel_plan_slot (id, plan_id, slot_number, current_topic_id, current_topic_position, is_completed) FROM stdin;
3	2	1	1	4	f
4	2	2	6	4	f
\.


--
-- Data for Name: oge_parallel_plan_topic_order; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.oge_parallel_plan_topic_order (id, plan_id, topic_id, order_index, created_at) FROM stdin;
\.


--
-- Data for Name: oge_parallel_plan_webinar; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.oge_parallel_plan_webinar (id, plan_id, webinar_id, slot_number, week_number, topic_id, position_in_topic, created_at) FROM stdin;
1	2	230	1	1	1	0	2025-09-12 15:33:08.641653
2	2	248	2	1	6	0	2025-09-12 15:33:08.647416
3	2	231	1	2	1	1	2025-09-12 15:33:08.651348
4	2	249	2	2	6	1	2025-09-12 15:33:08.655165
5	2	232	1	3	1	2	2025-09-12 15:33:08.673184
6	2	250	2	3	6	2	2025-09-12 15:33:08.677309
7	2	233	1	4	1	3	2025-09-12 15:33:08.680485
8	2	251	2	4	6	3	2025-09-12 15:33:08.683524
\.


--
-- Data for Name: oge_topic; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.oge_topic (id, name, task_numbers_str, description, is_active, created_at, is_hard_prog, priority) FROM stdin;
4	Алгебра логики	3, 8		t	2025-09-12 14:36:38.483825	\N	\N
5	Алгоритмы и исполнители	5, 15		t	2025-09-12 14:36:55.630424	\N	\N
7	Электронные таблицы и текстовый редактор	7, 13, 14		t	2025-09-12 14:37:16.7617	\N	\N
8	Файловая система	11, 12		t	2025-09-12 14:37:35.562704	\N	\N
1	Системы счисления	10		t	2025-09-12 14:32:05.315382	\N	1
6	Программирование	6		t	2025-09-12 14:37:04.880684	\N	2
2	Графы	4, 9		t	2025-09-12 14:36:03.492166	\N	3
3	Кодирование информации	1, 2		t	2025-09-12 14:36:15.496813	\N	4
\.


--
-- Data for Name: oge_topic_order; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.oge_topic_order (id, topic_id, order_index, is_active, created_at) FROM stdin;
1	1	0	t	2025-09-12 15:32:12.389421
2	6	1	t	2025-09-12 15:32:12.395294
3	2	2	t	2025-09-12 15:32:12.398793
4	3	3	t	2025-09-12 15:32:12.401846
5	4	4	t	2025-09-12 15:32:12.404522
6	5	5	t	2025-09-12 15:32:12.406857
7	7	6	t	2025-09-12 15:32:12.409653
8	8	7	t	2025-09-12 15:32:12.411797
\.


--
-- Data for Name: planned_webinar; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.planned_webinar (id, study_plan_id, webinar_id, week_number) FROM stdin;
1	1	14	1
2	1	16	1
3	1	21	2
4	1	25	2
5	1	28	3
6	1	29	3
7	1	17	4
8	1	32	4
9	1	35	5
10	1	34	5
11	2	39	1
12	2	30	1
13	2	31	1
14	2	32	2
15	2	35	2
16	2	36	2
17	2	37	3
18	2	38	3
19	2	40	3
20	2	42	4
21	2	43	4
22	2	44	4
23	2	46	5
24	2	48	5
25	2	49	5
26	3	80	1
27	3	103	1
28	3	81	2
29	3	104	2
30	3	82	3
31	3	105	3
32	3	83	4
33	3	110	4
34	3	84	5
35	3	115	5
36	3	70	1
37	3	72	1
38	3	73	1
39	3	74	1
40	3	79	1
41	4	13	1
42	4	14	1
43	4	15	1
44	4	20	2
45	4	21	2
46	5	11	1
47	5	12	2
48	5	13	3
49	5	14	4
50	5	15	5
51	5	6	1
52	5	7	1
53	5	8	1
54	5	9	1
55	5	10	1
56	6	18	1
57	6	23	1
58	6	17	1
59	6	31	2
60	6	40	2
61	6	41	2
62	6	42	3
63	6	44	3
64	6	46	3
65	6	47	4
66	6	49	4
67	6	50	4
68	7	31	1
69	7	159	1
70	7	160	3
71	7	76	2
72	7	73	2
73	7	79	3
74	7	165	4
75	7	168	4
76	7	80	1
77	7	81	2
78	7	82	3
79	7	83	4
80	7	116	1
81	7	121	2
82	7	122	3
83	7	125	4
84	8	13	1
85	8	152	1
86	8	15	1
87	8	18	1
88	8	154	2
89	8	27	2
90	8	39	2
91	8	28	3
92	8	29	3
93	8	155	3
94	8	30	3
95	8	17	1
96	8	156	4
97	8	38	4
98	8	49	4
99	8	166	4
100	9	1	1
101	9	2	1
102	9	3	1
103	9	4	1
104	9	5	2
105	9	6	2
106	9	7	2
107	9	8	2
108	9	9	3
109	9	10	3
110	9	11	1
111	9	12	3
112	9	13	2
113	9	152	5
114	9	14	3
115	9	15	4
116	9	16	4
117	9	18	4
118	9	20	5
119	9	21	5
120	9	17	3
121	10	1	1
122	10	2	1
123	10	3	1
124	10	4	1
125	10	5	1
126	10	6	1
127	10	7	2
128	10	8	2
129	10	9	2
130	10	10	2
131	10	14	2
132	10	18	3
133	10	20	3
134	10	21	3
135	10	22	3
136	10	24	3
137	10	25	4
138	10	27	4
139	10	39	4
140	10	28	4
141	10	29	4
142	10	17	3
143	11	20	1
144	11	21	1
145	11	22	1
146	11	23	2
147	11	24	2
148	11	25	2
149	11	26	3
150	11	27	3
151	11	28	3
152	11	29	4
153	11	30	4
154	11	32	4
155	12	103	1
156	12	23	1
157	12	41	1
158	12	104	2
159	12	158	2
160	12	48	2
161	12	105	3
162	12	54	3
163	12	60	3
164	12	110	4
165	12	73	4
166	12	79	4
238	14	31	2
239	14	41	1
240	14	43	4
241	14	44	4
242	14	50	2
243	14	51	1
244	14	58	3
245	14	60	3
246	14	70	2
247	14	175	4
248	14	178	3
249	14	49	1
250	15	12	1
251	15	13	1
252	15	14	1
253	15	15	2
254	15	20	2
255	15	16	2
256	15	21	3
257	15	23	3
258	15	18	3
259	15	22	4
260	15	24	4
270	17	179	1
271	17	170	1
272	17	120	1
273	17	96	1
274	17	174	2
275	17	184	2
276	17	129	2
277	17	183	2
278	17	182	3
279	17	130	3
280	17	158	3
281	17	185	3
282	17	181	4
283	17	188	4
284	17	131	4
285	17	187	4
286	18	181	1
287	18	182	1
288	18	183	1
289	18	184	1
290	18	137	1
291	18	174	2
292	18	42	2
293	18	175	2
294	18	185	2
295	18	186	2
296	18	31	3
297	18	179	3
298	18	188	3
299	18	187	3
300	18	138	3
301	19	12	1
302	19	20	1
303	19	32	1
304	19	36	1
305	19	21	2
306	19	22	2
307	19	34	2
308	19	37	2
309	19	25	3
310	19	26	3
311	19	51	3
312	19	53	3
313	19	39	4
314	19	29	4
315	19	17	4
316	19	4	4
317	19	178	4
318	20	172	1
319	20	75	1
320	20	68	1
321	20	77	1
322	20	65	1
323	20	177	1
324	20	156	1
325	20	70	1
326	20	178	1
327	20	182	1
328	20	181	1
329	20	41	1
330	20	31	2
331	20	79	3
348	22	195	1
349	22	196	1
350	22	198	1
351	23	1	1
352	23	2	1
353	23	206	1
354	23	3	2
355	23	5	2
356	23	207	2
357	23	6	3
358	23	7	3
359	23	208	3
360	23	8	4
361	23	9	4
362	23	209	4
363	24	2	1
364	24	5	1
365	24	10	1
366	24	206	1
367	24	1	2
368	24	6	2
369	24	8	2
370	24	207	2
371	24	3	3
372	24	7	3
373	24	9	3
374	24	208	3
375	24	4	4
376	24	209	4
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.student (id, first_name, last_name, platform_id, registration_date, target_score, hours_per_week, notes, is_active, initial_score, needs_python_basics, task_26_deferred, task_27_deferred, academic_year, exam_type, grade, tariff, course) FROM stdin;
31	Ученик	ЕГЭ	тест	2025-09-12 15:05:36.448236	85	9		t	\N	f	f	f	2026	ege	11	all_inclusive	yearly
33	 Anya	Krishtal	137860	2025-09-12 16:43:57.473995	100	12		t	\N	f	f	f	2026	ege	11	all_inclusive	yearly
1	Маша	Сидорович-Войно	48494	2025-04-02 16:08:23.222668	80	8		t	54	f	f	f	2025	ege	\N	\N	\N
2	Avidy	Bk	-	2025-04-03 05:35:40.716817	85	9		t	\N	f	f	f	2025	ege	\N	\N	\N
32	Ученик	ОГЭ	тест2	2025-09-12 15:13:35.483518	5	9		t	\N	f	f	f	2026	oge	\N	\N	\N
3	Татьяна	Ферулева	91528	2025-04-03 06:09:21.937487	96	9		t	68	f	f	f	2025	ege	\N	\N	\N
4	Кира 	Роднова	89975	2025-04-03 08:36:06.203697	80	9		t	40	f	f	f	2025	ege	\N	\N	\N
5	Денис	Козик	110693	2025-04-03 08:53:41.660205	90	9		t	\N	f	f	f	2025	ege	\N	\N	\N
6	Виолетта	Ненашева-Музыкантова	122845	2025-04-03 08:58:55.970502	90	4		t	\N	f	f	f	2025	ege	\N	\N	\N
7	Денис	Попов	80040	2025-04-04 12:50:36.144525	95	15		t	65	f	f	f	2025	ege	\N	\N	\N
8	Danilka	Petrukovich	109036	2025-04-06 09:52:43.509391	80	10		t	\N	f	f	f	2025	ege	\N	\N	\N
9	 Даша	Алякина	89537	2025-04-07 05:07:43.720598	100	12	1. 80+, но чем выше тем лучше😊\r\n2. 1, 3, 4, 7, 9, 13, 18, 22 (но все равно иногда возникают недопонимания)\r\n3. все остальные не рассматривались\r\n4. да, все хорошо\r\n5. не писала\r\n6. 10 - 11\r\n7. 11\r\nВсё включено. 	t	70	f	f	f	2025	ege	\N	\N	\N
10	Максим	Харитонов	вк	2025-04-07 05:53:49.276451	85	12	1. Нацелен на 50 баллов  (Задания 1-23)\r\n2. Задания под номером 1,2,3,5 4,10, 13\r\n3. Все задания кроме выше перечисленных\r\n4. Не особо знаком с программированием, в школе старался всегда решать аналитическим методом, но готов к активному изучению\r\n5. На 35-40 баллов\r\n6. 20-25 часов\r\n7. в 11\r\nВсё включено. Трёхмесячный курс с куратором и проверками - информатика БУ ЕГЭ 2024-2025. Преподаватель: Владимир Николаевич	t	\N	f	f	f	2025	ege	\N	\N	\N
11	Кирилл	Сидоров	demonlil	2025-04-07 06:26:22.368659	100	13	1)80+\r\n2)1-6,9,10,12-14,18-20,24\r\n3)17,22,25,26,27\r\n4)знаком\r\n5)последний на 64\r\n6) 10-12\r\n7)11\r\n8) всë включено	t	70	f	f	f	2025	ege	\N	\N	\N
12	Ксения	Чувашева	104759	2025-04-07 06:37:56.975611	80	1	Пробники мы не писали.. Я в 11 классе. Всё включено. Трёхмесячный курс с куратором и проверками - информатика БУ ЕГЭ 2024-2025. Преподаватель: Владимир Николаевич	t	\N	f	f	f	2025	ege	\N	\N	\N
13	Сергей	Вторушин	100123	2025-04-07 07:39:14.760977	100	9	Всё включено. курс с куратором и\r\nпроверками информатика БУ ЕГЭ 2025-\r\n2026. Преподаватель: Владимир\r\nНиколаевич	t	\N	t	f	f	2025	ege	\N	\N	\N
14	Алешка	Нижегородов	123846	2025-04-08 11:11:04.519439	70	12	хочет балл 55-77 \r\n10-15 часов\r\n\r\nпри корректировке плана нужно учитывать, что он по другим предметам тоже с нуля, т.е. не ставить много занятий (4 оптимально)	t	\N	t	f	f	2025	ege	\N	\N	\N
15	Игорь 	Капустин	90255	2025-04-09 08:20:40.285172	80	12	1. 70+\r\nя не решал никакие задания до этого, с момента подключения успел частично изучить: 1, 4, 5, 7, 8, 9, 11, 13, 15, 17\r\nпробники еще не писал\r\nготов уделять 8 часов в неделю(4-5 вебов + домашка в неделю)\r\nв 11 классе\r\nВ школе информатику практически не изучал, так что все с нуля, но разбираюсь во всем довольно легко(пока что)\r\nСамопроверка. Все вебинары и ДЗ без проверок и кураторов - информатика БУ ЕГЭ 2024-2025. Преподаватель: Владимир Николаевич\r\n	t	\N	f	f	f	2025	ege	\N	\N	\N
16	Данил	Калашников	117007	2025-04-12 09:20:03.092884	85	15		t	\N	t	f	f	2025	ege	\N	\N	\N
17	Роман	Коробов	120231	2025-04-16 09:50:39.806669	100	9	10 класс, нужно 90+ в целом	t	\N	f	f	f	2025	ege	\N	\N	\N
18	Радмир 	Хакимов	92005	2025-04-19 05:24:28.002181	90	15		t	73	f	f	f	2025	ege	\N	\N	\N
19	Руслан	Еликбаев	44763	2025-04-19 14:42:46.234998	95	11		t	\N	f	f	f	2025	ege	\N	\N	\N
20	Тимур	Афонин	75223	2025-04-20 12:39:01.635683	100	24		t	70	f	f	f	2025	ege	\N	\N	\N
22	Михаил	Шкутов	id383740661	2025-04-23 09:18:13.141753	90	10		t	70	f	f	f	2025	ege	\N	\N	\N
23	Ваня	Кураев	125574	2025-04-24 14:31:44.093505	100	9	10 класс	t	\N	f	f	f	2025	ege	\N	\N	\N
24	 София	Загребова	104832	2025-05-07 10:48:33.315339	100	15		t	85	f	f	f	2025	ege	\N	\N	\N
25	 Артём 	Смит	81940	2025-05-09 06:36:40.024067	90	13		t	70	f	f	f	2025	ege	\N	\N	\N
26	Александр 	Атланов	28932	2025-05-26 07:00:35.271949	100	16		t	85	f	f	f	2025	ege	\N	\N	\N
27	Эмилия	Варик	127413	2025-05-30 08:57:18.158983	90	9		t	\N	t	f	f	2025	ege	\N	\N	\N
28	Савелий	Мазоватов	87261	2025-05-31 06:41:56.825809	100	30		t	\N	f	f	f	2025	ege	\N	\N	\N
29	тест	тест	4565445	2025-06-14 19:09:48.436434	80	12		t	\N	f	f	f	2025	ege	\N	\N	\N
30	Артём	Вакифов	53202	2025-06-24 08:10:16.046124	100	15		t	\N	f	f	f	2025	ege	\N	\N	\N
\.


--
-- Data for Name: study_plan; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.study_plan (id, student_id, created_at, created_by_id) FROM stdin;
1	1	2025-04-02 16:09:19.497453	1
2	2	2025-04-03 05:41:54.535331	1
3	3	2025-04-03 06:25:19.670652	1
4	4	2025-04-03 08:46:38.135481	7
5	6	2025-04-03 09:01:23.844676	7
6	5	2025-04-03 10:34:25.128289	7
7	9	2025-04-07 05:25:58.019138	7
8	10	2025-04-07 06:04:20.700032	7
9	13	2025-04-07 07:41:51.639374	7
10	16	2025-04-12 09:23:40.355292	7
11	17	2025-04-16 10:06:47.152863	8
12	19	2025-04-19 14:44:30.970804	1
14	22	2025-04-23 09:36:08.314117	7
15	23	2025-04-24 14:49:52.596867	8
17	24	2025-05-07 11:01:46.638914	7
18	26	2025-05-26 07:15:07.028049	7
19	29	2025-06-14 19:14:24.320386	1
20	30	2025-06-24 08:18:59.584803	7
22	29	2025-08-07 07:12:22.169424	1
23	31	2025-09-12 15:09:05.32417	1
24	33	2025-09-12 16:45:33.854828	11
\.


--
-- Data for Name: task_number; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.task_number (id, number) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
11	11
12	12
13	13
14	14
15	15
16	16
17	17
18	18
19	19
20	20
21	21
22	22
23	23
24	24
25	25
26	26
27	27
\.


--
-- Data for Name: update_notification; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.update_notification (id, title, content, version, created_at, updated_at, created_by_id, is_active, priority, show_until, background_color, text_color, icon) FROM stdin;
1	Готовность к новому учебному году	Что нового:\r\n\r\n— Тёмная тема\r\n\r\nДобавлена тёмная тема и переключение  между ними\r\n\r\n[IMG:bba0f830-8aa0-40cf-9d3f-1ac8fc067f96.jpg]\r\n\r\n[IMG:3e66db34-0dc4-4503-9403-436eae119efb.jpg]\r\n\r\n[SLIDE]\r\n\r\n— Разделение детей на ЕГЭ и ОГЭ, а также разделение по годам\r\n\r\n[IMG:2-1.jpg]\r\n\r\n[IMG:2-2.jpg]\r\n\r\n[SLIDE]\r\n\r\n— Полноценная поддержка ОГЭ \r\n\r\nСтруктура планов ОГЭ отличается от ЕГЭ, поэтому под ОГЭ создан отдельный алгоритм. Принцип планов ОГЭ состоит в том, что несколько тем изучаются параллельно. \r\n\r\nПланы составляются автоматически на основе выбранного количества вебинаров в неделю - от 1 до 3. При одном вебинаре темы изучаются последовательно, а при двух-трех вебинарах система создает параллельные слоты, где ученик может изучать разные темы одновременно.\r\n\r\nЕсть четыре приоритетные темы, которые система ставит в начало: Системы счисления (1), Программирование (2), Графы (3) и Кодирование информации (4). Когда одна тема заканчивается, система автоматически подставляет следующую из очереди. У остальных тем пока нет приоритетов, потому что их нет в расписании.\r\n\r\nДополнительно можно добавить хард-вебинары ОГЭ - это отдельный слот для сложных вебинаров, который работает параллельно с основными темами. \r\n\r\nВизуально план отображается по неделям с разбивкой по слотам, где видно какой вебинар в какой теме и на какой позиции\r\n\r\n[IMG:3-1.jpg]\r\n\r\n[IMG:3-2.jpg]\r\n\r\n[IMG:3-3.jpg]\r\n\r\n[IMG:3-4.jpg]\r\n\r\n[SLIDE]\r\n\r\nПлан, который составила платформа:\r\n\r\nВот ваш план вебинаров исходя из вашего уровня и желаемого балла.\r\n\r\nЦифрами вебинары примерно разделены на недели. После того, как пройдете этот материал, напишите нам для корректировки плана подготовки!\r\n\r\n1️⃣\r\n\r\n🔢 Системы счисления. Изучение с самого нуля для ОГЭ по информатике 2026. Теория\r\nhttps://3.shkolkovo.online/lesson/34984\r\n\r\n💻 Как написать свою первую программу на Python? Типы данных, арифметические выражения, ввод-вывод в Python\r\nhttps://3.shkolkovo.online/lesson/34985\r\n\r\n2️⃣\r\n\r\n🔢 Вся теория по системам счисления, необходимая для ОГЭ по информатике\r\nhttps://3.shkolkovo.online/lesson/34987\r\n\r\n💻 Ветвление в Python. Операторы выбора if-else\r\nhttps://3.shkolkovo.online/lesson/34989\r\n\r\n3️⃣\r\n\r\n🔢 Системы счисления. Решаем задание №10 из ОГЭ по информатике\r\nhttps://3.shkolkovo.online/lesson/34988\r\n\r\n💻 Вложенное ветвление в Python\r\nhttps://3.shkolkovo.online/lesson/34993\r\n\r\n4️⃣\r\n\r\n🔢 Системы счисления. Дополнительная практика. Решаем задачи №10 из ОГЭ по информатике\r\nhttps://3.shkolkovo.online/lesson/34991\r\n\r\n💻 Циклы. Цикл с условием (цикл while) в Python\r\nhttps://3.shkolkovo.online/lesson/34997\r\n\r\n📅 Планирование:\r\n\r\nВажно распределить время правильно, чтобы охватить все темы. Вы начали готовиться уже сейчас, что похвально! Этого времени хватит на то, чтобы готовиться к информатике без спешки и стресса.\r\n\r\nГлобально вам предстоит изучить задания №1–16.\r\n\r\nВам нужно смотреть 2 вебинара и качественно выполнять домашнее задание к каждому.\r\n\r\nЭто поможет лучше закрепить материал, так как в первую очередь опыт мы получаем на практике.\r\nОдному домашнему заданию не стоит уделять более 1,5–2 часов, если решите не всё — не переживайте и помните, что вы всегда можете обратиться за помощью к кураторам в чате!\r\nКак только обретете небольшую базу, старайтесь писать пробники хотя бы раз в две недели 🧡\r\n\r\n📆 Подытожим ваш план по информатике на неделю:\r\n✔️ 2 вебинара\r\n✔️ домашняя работа к каждому вебинару\r\n✔️ решать пробники 2 раза в месяц\r\n\r\n📑 При желании можете пользоваться шаблоном нашей таблицы для планирования своей подготовки к ОГЭ: https://docs.google.com/spreadsheets/d/10BHRb5qGx00xk2g634qz2K8Yuh-r4fqKpmgYjcRXauY/edit?usp=sharing\r\nВ ней вы можете отмечать просмотренные вебинары и выполненные домашние задания сразу по нескольким предметам, планировать учебные и не только дела на предстоящий день или неделю.\r\nЧтобы сохранить шаблон себе, нужно нажать в левом верхнем углу на "Файл" ⮕ "Создать копию"\r\n\r\n❗️ Если вдруг нагрузка окажется слишком высокой или будут возникать трудности, то напишите повторно.\r\n\r\nПрочтите план внимательно. Всё ли вам понятно? Если да, то двигаемся дальше: поговорим немного про структуру экзамена и обсудим навигацию по курсу.\r\n\r\n[SLIDE]\r\n\r\n— Изменение процесса составления плана ЕГЭ\r\n\r\nРаньше при составлении плана можно было указать квоту на 26 и 27 задания. Эта идея расширилась и теперь можно регулировать квоты по всем блокам. Для этого создана отдельная страница при составлении плана – ⚡️Анализ блоков вебинаров, где платформа предлагает рекомендованное количество вебинаров по каждому блоку, но вы теперь можете корректировать их вручную. \r\n\r\nПроцесс составления плана теперь выглядит следующим образом:\r\n1) Выбор заданий для плана\r\n2) ⚡️Анализ блоков вебинаров \r\n3) Ручная перестановка вебинаров по желанию\r\n\r\n[IMG:4-1.jpg]\r\n\r\n[IMG:4-2.jpg]\r\n\r\n[IMG:4-3.jpg]\r\n\r\n[IMG:4-4.jpg]\r\n\r\n[SLIDE]\r\n\r\n— Теперь все 3 сообщения, которые нужно скинуть ученику в ЕГЭ, отображаются прямо в плане\r\n\r\nДля этого теперь я прошу при создании ученика указывать класс, тариф и курс (у всех пока годовой). В зависимости от этого формируются 2-е сообщение с Общей структурой экзамена и материалами и 3-е сообщение с Организационной информацией\r\n\r\n[IMG:5-1.jpg]\r\n\r\n[IMG:5-2.jpg]\r\n\r\n[IMG:5-3.jpg]\r\n\r\n[IMG:5-4.jpg]\r\n\r\n[IMG:5-5.jpg]\r\n\r\n[SLIDE]\r\n	2.0	2025-09-12 16:12:28.177431	2025-09-12 16:31:27.863996	1	f	3	2025-09-11 00:00:00	#667eea	#ffffff	rocket
\.


--
-- Data for Name: update_notification_image; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.update_notification_image (id, notification_id, image_url, caption, "position") FROM stdin;
1	1	uploads/update_images/bba0f830-8aa0-40cf-9d3f-1ac8fc067f96.jpg	\N	0
2	1	uploads/update_images/3e66db34-0dc4-4503-9403-436eae119efb.jpg	\N	1
3	1	uploads/update_images/e60d1695-5eeb-47bd-b308-a5ea201c1514.jpg	\N	2
4	1	uploads/update_images/5823a2d8-2912-41eb-9dce-f03c0e9e815e.jpg	\N	3
5	1	uploads/update_images/1484ae6c-acb0-42ec-b834-30c470b75055.jpg	\N	4
6	1	uploads/update_images/ca9c1598-2393-4781-9b9e-a9e03edc2703.jpg	\N	5
7	1	uploads/update_images/65ee1473-a4fb-4a46-a681-26f4c07bf8a6.jpg	\N	6
8	1	uploads/update_images/c826ef59-f97b-4f1a-a2dc-4dd0afb76170.jpg	\N	7
9	1	uploads/update_images/e2e93446-49da-4967-9eac-c0025cec6f05.jpg	\N	8
10	1	uploads/update_images/0ba19d44-3ab5-40bf-8da8-7752868bb51c.jpg	\N	9
11	1	uploads/update_images/eff18682-132d-439a-8f65-aa6c6c46dbf1.jpg	\N	10
12	1	uploads/update_images/87191f63-156e-467d-b2cc-c55b37538217.jpg	\N	11
13	1	uploads/update_images/e077487a-8763-49d7-bd66-07e9a6d32ec5.jpg	\N	12
14	1	uploads/update_images/2c595942-a673-42e0-b41e-8bede065b429.jpg	\N	13
15	1	uploads/update_images/ae95d31d-971e-4836-b850-becd46382bc6.jpg	\N	14
16	1	uploads/update_images/cc5a1561-095e-4a34-bbea-50c1a0b80d32.jpg	\N	15
17	1	uploads/update_images/aa54a184-d1c2-4ef5-81ee-8fc6faefe472.jpg	\N	16
\.


--
-- Data for Name: user_notification_status; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.user_notification_status (id, user_id, notification_id, viewed_at, is_dismissed) FROM stdin;
4	1	1	2025-09-12 16:15:18.768071	f
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.users (id, username, password_hash, role, first_name, last_name, last_login) FROM stdin;
5	velukayataina	scrypt:32768:8:1$qgSj2kdH7o8ZSEdg$510945f113cb88ca89dc1f6ec558e4981b1d38ead1cb7f475a387e8ae1dbfc2a4d002599bcdda9784624a64cf23d39c60f0fd5d85bb4e11a2b24f8c490377303	admin	Таина	Житина	2025-04-03 23:24:25.986663
6	mkhorinova	scrypt:32768:8:1$c56XLNjyjJfqSnuO$c7bdf1998ce2207a6775c2990ca3fada497b45e5c3fe0027bdbeb38d25b772b852b30c581cf8212019c2c991c8dafc9ed884369e57434ea9e7f5744a37ce31d6	organizational_curator	Муслима	Хоринова	2025-04-20 12:41:10.150509
10	arr_niga	scrypt:32768:8:1$zbp0vGuW9SFZlpbb$57857c9c0ca2f7707c6d6e5cac4e384b2e2593f65f1fdbb1325e5c84c69d7dc9078aebbd52cc37c99a2b1aaf7469fbe08f0154ff595c7f1fd3ece64a8f184626	organizational_curator	Артём	Нигматулин	2025-04-03 23:24:26.369599
14	qwrttq	pbkdf2:sha256:600000$ZshyfMwXBFst4uqb$c9a71a5a204ac935e02d3432ad7d8a35e90841e90fb15913f5149a3d26ce5d4e	educational_curator	Пётр	Алексеенко	2025-04-10 12:16:53.711252
15	mirai588	pbkdf2:sha256:600000$mto5eUWQy5l29qgV$f416411788b45773296286ab054a65040bf32172c4bb613162a643519e09c5a9	educational_curator	Виктория	Сёмина	2025-04-10 12:17:46.228677
16	berezovskiym	pbkdf2:sha256:600000$34ONf09oJbHMT7la$77091b32c5a12edcdaf59fd94ab57cc2f3469b83d96809ac2fa7328b81872344	educational_curator	Максим	Березовский	2025-04-10 12:18:22.990729
17	sorryhanzodenis	pbkdf2:sha256:600000$4JN5o14Ti3nt2xsM$f52c6d7625f85e2c47a65a2a293683505d39a9771da8d1878ca3a0100c736d80	educational_curator	Денис	Салтыков	2025-04-10 12:19:01.263964
19	suetolog9999	pbkdf2:sha256:600000$HWdOz51nCHFFiaLs$53c02057e4571064fe13b923962332050efea7a0a5dc20c8fe1a0f83398cbeef	educational_curator	Камиль	Миргасимов	2025-04-10 12:20:10.719341
20	sofia__kataeva	pbkdf2:sha256:600000$aoUjgHclGAXWL3Vm$f848f5a425155a64ee2aef9eb87f1139b92e5a75ee4e3e5dbd62602fe88a7aa9	educational_curator	София	Татаурова	2025-04-18 20:31:12.867391
22	saitaiu_x	pbkdf2:sha256:600000$ZDtSYPXmWBk0kg5D$2ab96575abea9a72193dc18b2ed690ebad8134c7f20e2498e068f5e6d3ace076	educational_curator	Екатерина	Попова	2025-04-10 12:21:59.548616
24	slav4ik_21	pbkdf2:sha256:600000$WzxzXaf0BXI6sALn$b380f4a0f2c0ac272f531dd4bad7c19187ff94701f030dd8e4fcf566e66837e5	educational_curator	Слава	Никитин	2025-04-10 12:23:44.04337
8	lllsbp	pbkdf2:sha256:600000$KvlwHghgiDMbzod0$94bb1ef21261a2655c4593723d6dc3c94f7f923ce7787fe9794b351e3dac5b22	organizational_curator	Самира	Шигалугова	2025-05-30 14:18:34.821302
7	pollliin	pbkdf2:sha256:600000$8qxTJOcgk09iDVEN$802a8aa5ff8664f5674066844e099ee47865dff8d00b6c4ca6ff0b1861b5bc26	admin	Полина	Гусева	2025-06-24 08:18:59.84756
3	zinger_s	scrypt:32768:8:1$1uUM5J5yPSS8axhE$2fa6134807a4eb58342a31bc30aaa693db8378cabf14a38f011bea8b4c328bccb6d9d8dd3730bbe7d874b54cf9d37fc858c338fef0f1dc6b83e3561187c4a8c6	super_admin	Александра	Смирнова	2025-07-02 12:01:19.970537
13	koshachya_myatka	pbkdf2:sha256:600000$yc1Y6nZtKyxybq9r$c246d35738d94acac2629285dbb13eef8af53bba0b2221c5d7d93a1468c166c6	educational_curator	Анна	Парамонова	2025-05-11 06:39:04.453087
18	dsrgvaa	pbkdf2:sha256:600000$4HkFAZdxg1ZJi19K$32170149d84f8d5d9ef943525a0854e6c13a34c087c641ee2317ccd2598be1d8	educational_curator	Даша	Сергеева	2025-04-29 16:39:38.148763
23	hom1c1d3	pbkdf2:sha256:600000$vyjMc5rLJPdgGh5C$f375368d4259fc6de3fa27c70b048d7ae87fb3e4a79d2012f859e2f2c6c61110	educational_curator	Антон	Караваев	2025-05-13 13:14:26.928977
9	elya_na_svyazi	pbkdf2:sha256:600000$t6tyrDoOhkURggXK$772ad47c3311511446d4da24c07ca59c3b6e9fbaeb071a73495711033bc455fe	organizational_curator	Элина	Аметова	2025-07-03 07:49:49.978668
2	katherinevstheworld	pbkdf2:sha256:600000$HdKeIO1i1fUDg9at$4e7e1c559a8ad2a45c5b269a852bd27297e869516df2ed948771efc61fbc88a8	super_admin	Катерина	Бриль	2025-06-10 05:19:59.288009
32	@ksevlii	pbkdf2:sha256:600000$H5C4oM1FXttPEm0d$b433b5c061dc28418c8458022b375957a4086e68634675fadffa437e0afc3240	educational_curator	Ксения	Бусыгина	2025-07-02 12:04:09.374609
21	itghoul	pbkdf2:sha256:600000$2tj9Dw9VVNXnN8wA$eaad21d33bc727aca8b1e02cb38166ba11f46dbac477f507e42fc9e76cb688b4	educational_curator	Милана	Фомина	2025-07-02 16:42:04.191278
12	amalia_m_21	pbkdf2:sha256:600000$d4ES8lumxV4J78Bz$8a687b04222651dbf64886e58494eb9c9ca23040d3e649acc7a02d0e5d7e6205	organizational_curator	Амалия	Мордвинова	2025-07-06 10:32:40.409608
28	test	pbkdf2:sha256:600000$DsgRIZRMABqXKUhY$a350615efa43637f71c199047ddf85ddd1f6278f2a8e3eeef7b747e35b218ee9	educational_curator	Учебный	Куратор	2025-07-06 10:48:03.069778
31	@id_r0ach	pbkdf2:sha256:600000$2lhQkGLLTxRFzjNk$51a57a6c4ca33cb71c59679e4adb1ae1b8c02663d8c273053e670df9784c4632	educational_curator	Денис	Яшин	2025-07-07 13:56:47.1388
30	@arti_underskill	pbkdf2:sha256:600000$SqZSkNjHaejDUHCO$ba2ea744aa1ac993a6f50f00c30cf67118ffa2812aa98b605b3a39303cf0d81c	organizational_curator	Данил	Медведев	2025-09-12 16:48:45.054983
25	radhatboi	pbkdf2:sha256:600000$OdRqtrqvnAKe2JZ6$a2eeb011861e8703f41ded4390f5da27eabb8e12c5acf64239a367c5b061120a	educational_curator	Михаил	Солодилов	2025-07-04 15:42:25.227728
11	dariashupikova	pbkdf2:sha256:600000$aSz2JGwjvlJmq5qe$646e7ff487e884254a6b48f57e1a2628bde9a808ea1d3cefb0d121717d78cd70	super_admin	Дарья	Шупикова	2025-09-12 16:46:05.697028
29	testorg	pbkdf2:sha256:600000$YY8ZYQEnoY1n8PP4$45d88d98d21010c82589c15569818d6ac737635736811951e3539bdc0bfbb7d2	organizational_curator	Организационный	Куратор	2025-09-12 16:32:03.72885
33	maneshechka	scrypt:32768:8:1$noY9XfVo1epgQQqC$2771efcf112a630ae55a72da29c6642fa69b4cd7786668e3753fef7f4dd879259e2874205e42a9983dbdcd2c2f639cfa0bd842b4e4bb3aeeb4a6b8f7c0739165	super_admin	Мане	Овсепян	2025-09-12 16:41:38.180089
1	makarkonev	pbkdf2:sha256:600000$XQ4TV2KQx8diL3vW$0fab38c25704578b7625e9821845ee92437e65238cf332f4aea7ab6b7a549b65	super_admin	Макар	Конев	2025-09-12 17:03:00.238447
\.


--
-- Data for Name: watched_webinar; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.watched_webinar (id, student_id, webinar_id, watched_at, created_by_id) FROM stdin;
1	2	11	2025-04-03 05:38:12.013912	1
2	2	12	2025-04-03 05:38:12.019342	1
3	2	17	2025-04-03 05:38:12.024284	1
4	2	18	2025-04-03 05:38:12.028154	1
5	2	20	2025-04-03 05:38:12.031744	1
6	2	22	2025-04-03 05:38:12.035309	1
7	2	23	2025-04-03 05:38:12.039236	1
8	2	24	2025-04-03 05:38:12.042733	1
9	2	25	2025-04-03 05:38:12.046304	1
10	2	26	2025-04-03 05:38:12.04981	1
11	2	29	2025-04-03 05:38:12.053572	1
12	2	27	2025-04-03 05:38:12.057143	1
13	2	28	2025-04-03 05:38:12.060368	1
14	3	64	2025-04-03 06:11:39.308664	1
15	3	63	2025-04-03 06:11:39.311904	1
16	3	4	2025-04-03 06:11:39.314161	1
17	3	62	2025-04-03 06:11:39.316387	1
18	3	61	2025-04-03 06:11:39.318619	1
19	3	60	2025-04-03 06:11:39.32083	1
20	3	59	2025-04-03 06:11:39.323112	1
21	3	58	2025-04-03 06:11:39.325365	1
22	3	57	2025-04-03 06:11:39.327703	1
23	3	56	2025-04-03 06:11:39.329908	1
24	3	55	2025-04-03 06:11:39.332484	1
25	3	54	2025-04-03 06:11:39.335288	1
26	3	53	2025-04-03 06:11:39.337748	1
27	3	52	2025-04-03 06:11:39.340148	1
28	3	51	2025-04-03 06:11:39.342436	1
29	3	50	2025-04-03 06:11:39.344735	1
30	3	49	2025-04-03 06:11:39.347135	1
31	3	48	2025-04-03 06:11:39.349826	1
32	3	47	2025-04-03 06:11:39.352218	1
33	3	46	2025-04-03 06:11:39.354696	1
34	3	45	2025-04-03 06:11:39.356837	1
35	3	44	2025-04-03 06:11:39.359158	1
36	3	43	2025-04-03 06:11:39.361197	1
37	3	42	2025-04-03 06:11:39.363449	1
38	3	41	2025-04-03 06:11:39.365664	1
39	3	40	2025-04-03 06:11:39.368518	1
40	3	38	2025-04-03 06:11:39.370645	1
41	3	37	2025-04-03 06:11:39.372816	1
42	3	34	2025-04-03 06:11:39.375058	1
43	3	36	2025-04-03 06:11:39.377253	1
44	3	35	2025-04-03 06:11:39.379563	1
45	3	32	2025-04-03 06:11:39.382032	1
46	3	31	2025-04-03 06:11:39.384422	1
47	3	17	2025-04-03 06:11:39.386677	1
48	3	30	2025-04-03 06:11:39.389067	1
49	3	10	2025-04-03 06:11:39.391419	1
50	3	9	2025-04-03 06:11:39.393645	1
51	3	8	2025-04-03 06:11:39.396081	1
52	3	7	2025-04-03 06:11:39.398374	1
53	3	6	2025-04-03 06:11:39.400537	1
54	3	5	2025-04-03 06:11:39.402862	1
55	3	3	2025-04-03 06:11:39.405177	1
56	3	2	2025-04-03 06:11:39.407388	1
57	3	1	2025-04-03 06:11:39.409489	1
58	3	29	2025-04-03 06:11:39.411802	1
59	3	28	2025-04-03 06:11:39.414142	1
60	3	39	2025-04-03 06:11:39.416489	1
61	3	27	2025-04-03 06:11:39.418606	1
62	3	19	2025-04-03 06:11:39.420818	1
63	3	26	2025-04-03 06:11:39.423079	1
64	3	25	2025-04-03 06:11:39.425216	1
65	3	24	2025-04-03 06:11:39.427527	1
66	3	23	2025-04-03 06:11:39.430216	1
67	3	22	2025-04-03 06:11:39.432681	1
68	3	21	2025-04-03 06:11:39.435081	1
69	3	20	2025-04-03 06:11:39.437483	1
70	3	18	2025-04-03 06:11:39.439934	1
71	3	16	2025-04-03 06:11:39.442274	1
72	3	15	2025-04-03 06:11:39.444595	1
73	3	14	2025-04-03 06:11:39.446952	1
74	3	13	2025-04-03 06:11:39.449207	1
75	3	12	2025-04-03 06:11:39.451657	1
76	3	11	2025-04-03 06:11:39.453732	1
77	4	13	2025-04-03 08:46:47.615964	7
78	4	14	2025-04-03 08:46:47.615978	7
79	4	15	2025-04-03 08:46:47.615988	7
80	4	20	2025-04-03 08:46:47.615996	7
81	4	21	2025-04-03 08:46:47.616005	7
82	5	11	2025-04-03 08:54:29.594546	7
83	5	12	2025-04-03 08:54:29.597981	7
84	5	13	2025-04-03 08:54:29.601776	7
85	5	14	2025-04-03 08:54:29.604815	7
86	5	15	2025-04-03 08:54:29.608006	7
87	5	20	2025-04-03 08:54:29.611732	7
88	5	22	2025-04-03 08:54:29.614814	7
89	5	26	2025-04-03 08:54:29.617536	7
90	5	27	2025-04-03 08:55:36.594525	7
91	5	28	2025-04-03 08:55:36.597405	7
92	5	29	2025-04-03 08:55:36.600039	7
93	5	30	2025-04-03 08:55:36.602638	7
94	5	32	2025-04-03 08:55:36.605161	7
95	5	34	2025-04-03 08:55:36.607768	7
96	5	35	2025-04-03 08:55:36.610377	7
97	5	36	2025-04-03 08:55:36.613002	7
98	5	37	2025-04-03 08:55:36.615541	7
99	5	38	2025-04-03 08:55:36.618045	7
100	5	39	2025-04-03 08:55:36.621127	7
101	5	43	2025-04-03 08:55:36.623939	7
102	8	11	2025-04-06 09:53:00.256086	7
103	8	12	2025-04-06 09:53:00.259068	7
104	8	13	2025-04-06 09:53:00.261847	7
105	8	14	2025-04-06 09:53:00.264102	7
106	8	15	2025-04-06 09:53:00.266273	7
107	8	16	2025-04-06 09:53:00.268907	7
108	8	17	2025-04-06 09:53:00.271194	7
109	8	18	2025-04-06 09:53:00.273189	7
110	8	19	2025-04-06 09:53:21.828983	7
111	8	24	2025-04-06 09:53:21.832432	7
112	8	21	2025-04-06 09:53:21.834619	7
113	8	37	2025-04-06 09:53:21.836993	7
114	8	22	2025-04-06 09:53:21.839837	7
115	8	36	2025-04-06 09:53:21.842267	7
116	8	20	2025-04-06 09:53:21.844433	7
117	8	26	2025-04-06 09:53:21.84658	7
118	8	27	2025-04-06 09:53:21.849308	7
119	8	33	2025-04-06 09:53:21.851448	7
120	8	25	2025-04-06 09:53:21.853848	7
121	8	28	2025-04-06 09:53:21.855978	7
122	8	29	2025-04-06 09:53:21.858662	7
123	8	35	2025-04-06 09:53:21.860992	7
124	8	23	2025-04-06 09:53:21.863215	7
125	8	30	2025-04-06 09:53:21.865813	7
126	9	11	2025-04-07 05:08:37.712943	7
127	9	12	2025-04-07 05:08:37.715477	7
128	9	13	2025-04-07 05:08:37.71774	7
129	9	14	2025-04-07 05:08:37.72087	7
130	9	15	2025-04-07 05:08:37.723574	7
131	9	16	2025-04-07 05:08:37.725783	7
132	9	18	2025-04-07 05:08:37.728079	7
133	9	19	2025-04-07 05:08:37.730317	7
134	9	20	2025-04-07 05:08:37.733374	7
135	9	21	2025-04-07 05:08:37.735836	7
136	9	22	2025-04-07 05:08:37.738257	7
137	9	23	2025-04-07 05:08:37.740601	7
138	9	24	2025-04-07 05:08:37.743511	7
139	9	25	2025-04-07 05:08:37.745831	7
140	9	26	2025-04-07 05:08:37.748423	7
141	9	39	2025-04-07 05:08:37.750532	7
142	9	27	2025-04-07 05:09:01.276046	7
143	9	28	2025-04-07 05:09:01.280639	7
144	9	156	2025-04-07 05:09:01.284164	7
145	9	139	2025-04-07 05:09:01.289002	7
146	9	29	2025-04-07 05:09:01.293737	7
147	9	154	2025-04-07 05:09:01.298287	7
148	9	30	2025-04-07 05:09:01.302564	7
149	9	32	2025-04-07 05:09:01.306312	7
150	9	33	2025-04-07 05:09:28.576076	7
151	9	34	2025-04-07 05:09:28.580179	7
152	9	35	2025-04-07 05:09:28.583884	7
153	9	36	2025-04-07 05:09:28.587341	7
154	9	37	2025-04-07 05:09:28.590661	7
155	9	38	2025-04-07 05:09:28.59616	7
156	9	40	2025-04-07 05:09:28.59984	7
157	9	41	2025-04-07 05:09:28.603646	7
158	9	43	2025-04-07 05:09:28.607557	7
159	9	44	2025-04-07 05:09:28.612339	7
160	9	46	2025-04-07 05:09:28.616518	7
161	9	47	2025-04-07 05:09:28.62136	7
162	9	48	2025-04-07 05:09:28.625033	7
163	9	49	2025-04-07 05:09:28.629955	7
164	9	50	2025-04-07 05:09:28.63376	7
165	9	157	2025-04-07 05:09:28.637684	7
166	9	158	2025-04-07 05:09:28.641447	7
167	9	51	2025-04-07 05:10:01.211976	7
168	9	54	2025-04-07 05:10:01.215975	7
169	9	55	2025-04-07 05:10:01.220021	7
170	9	103	2025-04-07 05:10:01.223875	7
171	9	56	2025-04-07 05:10:01.228549	7
172	9	57	2025-04-07 05:10:01.232388	7
173	9	59	2025-04-07 05:10:01.236126	7
174	9	104	2025-04-07 05:10:01.240438	7
175	9	60	2025-04-07 05:10:01.244695	7
176	9	61	2025-04-07 05:10:01.248277	7
177	9	63	2025-04-07 05:10:01.251746	7
178	9	105	2025-04-07 05:10:01.255228	7
179	9	64	2025-04-07 05:10:01.259355	7
180	9	65	2025-04-07 05:10:01.263005	7
181	9	66	2025-04-07 05:10:01.266579	7
182	9	110	2025-04-07 05:10:01.269797	7
183	10	1	2025-04-07 05:54:17.742691	7
184	10	2	2025-04-07 05:54:17.747248	7
185	10	3	2025-04-07 05:54:17.75117	7
186	10	5	2025-04-07 05:54:17.755385	7
187	10	6	2025-04-07 05:54:17.759263	7
188	10	7	2025-04-07 05:54:17.76326	7
189	10	8	2025-04-07 05:54:17.767226	7
190	10	9	2025-04-07 05:54:17.77096	7
191	10	10	2025-04-07 05:54:17.774947	7
192	10	11	2025-04-07 05:54:17.780006	7
193	10	12	2025-04-07 05:54:17.784974	7
194	10	14	2025-04-07 05:54:17.788666	7
195	10	16	2025-04-07 05:54:17.792469	7
196	10	19	2025-04-07 05:54:17.797419	7
197	10	20	2025-04-07 05:54:17.80149	7
198	10	21	2025-04-07 05:54:17.805535	7
199	10	22	2025-04-07 05:54:17.809855	7
200	10	24	2025-04-07 05:54:17.814731	7
201	10	25	2025-04-07 05:54:17.818795	7
202	10	26	2025-04-07 05:54:17.822691	7
203	10	32	2025-04-07 05:54:17.826306	7
204	10	34	2025-04-07 05:54:56.367754	7
205	10	35	2025-04-07 05:54:56.370747	7
206	10	36	2025-04-07 05:54:56.373067	7
207	10	37	2025-04-07 05:54:56.375366	7
208	10	40	2025-04-07 05:54:56.378206	7
209	10	42	2025-04-07 05:54:56.380488	7
210	10	44	2025-04-07 05:54:56.382885	7
211	10	51	2025-04-07 05:54:56.385261	7
212	10	58	2025-04-07 05:54:56.388024	7
213	10	53	2025-04-07 05:54:56.390288	7
214	10	55	2025-04-07 05:54:56.392562	7
215	10	57	2025-04-07 05:54:56.394886	7
216	10	59	2025-04-07 05:54:56.397697	7
217	10	63	2025-04-07 05:54:56.400149	7
218	10	64	2025-04-07 05:54:56.402436	7
219	10	65	2025-04-07 05:54:56.404469	7
220	11	11	2025-04-07 06:29:21.119711	7
221	11	12	2025-04-07 06:29:21.126729	7
222	11	13	2025-04-07 06:29:21.132734	7
223	11	15	2025-04-07 06:29:21.137443	7
224	11	18	2025-04-07 06:29:21.143212	7
225	11	20	2025-04-07 06:29:21.14824	7
226	11	25	2025-04-07 06:29:21.152802	7
227	11	26	2025-04-07 06:29:21.1574	7
228	11	27	2025-04-07 06:29:21.163657	7
229	11	28	2025-04-07 06:29:21.168268	7
230	11	29	2025-04-07 06:29:21.173085	7
231	11	30	2025-04-07 06:29:21.177753	7
232	11	32	2025-04-07 06:29:21.184364	7
233	11	35	2025-04-07 06:29:21.190343	7
234	11	38	2025-04-07 06:29:21.19632	7
235	11	40	2025-04-07 06:29:21.203415	7
236	11	36	2025-04-07 06:29:21.214043	7
237	11	153	2025-04-07 06:29:21.22002	7
238	11	37	2025-04-07 06:29:21.22703	7
239	11	154	2025-04-07 06:29:21.240659	7
240	11	41	2025-04-07 06:29:21.248035	7
241	11	42	2025-04-07 06:29:21.250289	7
242	11	43	2025-04-07 06:29:21.253004	7
243	11	156	2025-04-07 06:29:21.256058	7
244	11	44	2025-04-07 06:29:21.259044	7
245	11	46	2025-04-07 06:29:21.262095	7
246	11	47	2025-04-07 06:29:21.264481	7
247	11	157	2025-04-07 06:29:21.268698	7
248	11	48	2025-04-07 06:29:21.271945	7
249	11	49	2025-04-07 06:29:21.275485	7
250	11	80	2025-04-07 06:29:21.278347	7
251	11	97	2025-04-07 06:29:21.281382	7
252	11	50	2025-04-07 06:29:21.28483	7
253	11	160	2025-04-07 06:29:21.287967	7
254	11	98	2025-04-07 06:29:21.290847	7
255	11	81	2025-04-07 06:29:21.296754	7
256	11	158	2025-04-07 06:29:21.300433	7
257	11	51	2025-04-07 06:29:21.303294	7
258	11	99	2025-04-07 06:29:21.306317	7
259	11	82	2025-04-07 06:29:21.309404	7
260	11	52	2025-04-07 06:29:21.31316	7
261	11	58	2025-04-07 06:29:21.316112	7
262	11	100	2025-04-07 06:29:21.318807	7
263	11	84	2025-04-07 06:29:21.321577	7
264	11	53	2025-04-07 06:30:06.955115	7
265	11	54	2025-04-07 06:30:06.960454	7
266	11	103	2025-04-07 06:30:06.965094	7
267	11	83	2025-04-07 06:30:06.96981	7
268	11	55	2025-04-07 06:30:06.975502	7
269	11	56	2025-04-07 06:30:06.980028	7
270	11	104	2025-04-07 06:30:06.98447	7
271	11	85	2025-04-07 06:30:06.988976	7
272	11	59	2025-04-07 06:30:06.994383	7
273	11	60	2025-04-07 06:30:06.999176	7
274	11	105	2025-04-07 06:30:07.001238	7
275	11	86	2025-04-07 06:30:07.003293	7
276	11	61	2025-04-07 06:30:07.00578	7
277	11	62	2025-04-07 06:30:07.00783	7
278	11	110	2025-04-07 06:30:07.010302	7
279	11	87	2025-04-07 06:30:07.01248	7
280	11	63	2025-04-07 06:30:39.274541	7
281	11	64	2025-04-07 06:30:39.277119	7
282	11	88	2025-04-07 06:30:39.279501	7
283	11	115	2025-04-07 06:30:39.281852	7
284	11	65	2025-04-07 06:30:39.284695	7
285	11	66	2025-04-07 06:30:39.287032	7
286	11	89	2025-04-07 06:30:39.289305	7
287	11	116	2025-04-07 06:30:39.291666	7
288	11	67	2025-04-07 06:30:39.294654	7
289	11	68	2025-04-07 06:30:39.296943	7
290	11	90	2025-04-07 06:30:39.299268	7
291	11	120	2025-04-07 06:30:39.301551	7
292	11	69	2025-04-07 06:30:39.304392	7
293	11	70	2025-04-07 06:30:39.306675	7
294	11	91	2025-04-07 06:30:39.309042	7
295	11	121	2025-04-07 06:30:39.311141	7
296	15	20	2025-04-09 08:24:04.961163	7
297	15	21	2025-04-09 08:24:04.966463	7
298	15	22	2025-04-09 08:24:04.970326	7
299	15	11	2025-04-09 08:24:04.974286	7
300	15	12	2025-04-09 08:24:04.978399	7
301	15	13	2025-04-09 08:24:04.984523	7
302	15	14	2025-04-09 08:24:04.992166	7
303	15	15	2025-04-09 08:24:05.003207	7
304	15	16	2025-04-09 08:24:05.009942	7
305	15	17	2025-04-09 08:24:05.016876	7
306	15	18	2025-04-09 08:24:05.023907	7
307	17	11	2025-04-16 09:52:52.55443	8
308	17	12	2025-04-16 09:53:18.193265	8
309	17	13	2025-04-16 09:55:16.387027	8
310	17	14	2025-04-16 09:55:39.109599	8
311	17	15	2025-04-16 09:55:45.824508	8
312	17	16	2025-04-16 09:55:52.7102	8
313	17	18	2025-04-16 09:56:02.20445	8
314	17	1	2025-04-16 10:11:25.32743	8
315	17	2	2025-04-16 10:11:25.332504	8
316	17	3	2025-04-16 10:11:25.337658	8
317	17	4	2025-04-16 10:11:25.342636	8
318	17	5	2025-04-16 10:11:25.347168	8
319	17	6	2025-04-16 10:11:25.351109	8
320	17	7	2025-04-16 10:11:25.355546	8
321	17	8	2025-04-16 10:11:25.359499	8
322	17	9	2025-04-16 10:11:25.362896	8
323	17	10	2025-04-16 10:11:25.36451	8
324	18	11	2025-04-19 05:26:45.215334	7
325	18	12	2025-04-19 05:26:45.218501	7
326	18	13	2025-04-19 05:26:45.220944	7
327	18	103	2025-04-19 05:26:45.223282	7
328	18	14	2025-04-19 05:26:45.226238	7
329	18	15	2025-04-19 05:26:45.229016	7
330	18	16	2025-04-19 05:26:45.23223	7
331	18	104	2025-04-19 05:26:45.234845	7
332	18	17	2025-04-19 05:26:45.238022	7
333	18	18	2025-04-19 05:26:45.241011	7
334	18	20	2025-04-19 05:26:45.243366	7
335	18	21	2025-04-19 05:26:45.245655	7
336	18	105	2025-04-19 05:26:45.250127	7
337	18	22	2025-04-19 05:26:45.257456	7
338	18	23	2025-04-19 05:26:45.263291	7
339	18	25	2025-04-19 05:26:45.269064	7
340	18	110	2025-04-19 05:26:45.274501	7
341	22	19	2025-04-23 09:18:45.453265	7
342	22	25	2025-04-23 09:18:45.470694	7
343	22	26	2025-04-23 09:18:45.484901	7
344	22	39	2025-04-23 09:18:45.501668	7
345	22	27	2025-04-23 09:18:45.517216	7
346	22	28	2025-04-23 09:18:45.528063	7
347	22	30	2025-04-23 09:18:45.536869	7
348	22	32	2025-04-23 09:18:45.542352	7
349	22	33	2025-04-23 09:18:45.549341	7
350	22	36	2025-04-23 09:18:45.562817	7
351	22	37	2025-04-23 09:18:45.567979	7
352	22	38	2025-04-23 09:18:45.572818	7
353	22	40	2025-04-23 09:18:45.577553	7
354	22	11	2025-04-23 09:23:10.607331	7
355	22	12	2025-04-23 09:23:10.623767	7
356	22	13	2025-04-23 09:23:10.635646	7
357	22	14	2025-04-23 09:23:10.646212	7
358	22	15	2025-04-23 09:25:17.236174	7
359	22	16	2025-04-23 09:25:17.247874	7
360	22	18	2025-04-23 09:25:17.258693	7
361	22	20	2025-04-23 09:25:17.275724	7
362	22	21	2025-04-23 09:25:17.286974	7
363	22	22	2025-04-23 09:25:17.297376	7
364	22	23	2025-04-23 09:25:17.309056	7
365	22	24	2025-04-23 09:25:17.321561	7
366	24	13	2025-05-07 10:48:49.041466	7
367	24	21	2025-05-07 10:48:49.04732	7
368	24	23	2025-05-07 10:48:49.052035	7
369	24	80	2025-05-07 10:48:49.056685	7
370	24	103	2025-05-07 10:48:49.061283	7
371	24	25	2025-05-07 10:48:49.06719	7
372	24	29	2025-05-07 10:48:49.071773	7
373	24	30	2025-05-07 10:48:49.076186	7
374	24	81	2025-05-07 10:48:49.081167	7
375	24	104	2025-05-07 10:48:49.085814	7
376	24	32	2025-05-07 10:48:49.094187	7
377	24	35	2025-05-07 10:48:49.098958	7
378	24	37	2025-05-07 10:48:49.103458	7
379	24	82	2025-05-07 10:48:49.107808	7
380	24	105	2025-05-07 10:48:49.112314	7
381	24	38	2025-05-07 10:48:49.117792	7
382	24	41	2025-05-07 10:48:49.122267	7
383	24	43	2025-05-07 10:48:49.12715	7
384	24	84	2025-05-07 10:48:49.13156	7
385	24	110	2025-05-07 10:48:49.135961	7
386	24	44	2025-05-07 10:49:25.797299	7
387	24	46	2025-05-07 10:49:25.803614	7
388	24	48	2025-05-07 10:49:25.808471	7
389	24	83	2025-05-07 10:49:25.813435	7
390	24	115	2025-05-07 10:49:25.818219	7
391	24	49	2025-05-07 10:49:25.824338	7
392	24	50	2025-05-07 10:49:25.829385	7
393	24	51	2025-05-07 10:49:25.834693	7
394	24	85	2025-05-07 10:49:25.839365	7
395	24	116	2025-05-07 10:49:25.844237	7
396	24	53	2025-05-07 10:49:25.853657	7
397	24	54	2025-05-07 10:49:25.859103	7
398	24	56	2025-05-07 10:49:25.864441	7
399	24	86	2025-05-07 10:49:25.870245	7
400	24	121	2025-05-07 10:49:25.87671	7
401	24	58	2025-05-07 10:49:25.883718	7
402	24	59	2025-05-07 10:49:25.888727	7
403	24	60	2025-05-07 10:49:25.894102	7
404	24	87	2025-05-07 10:49:25.899386	7
405	24	122	2025-05-07 10:49:25.904541	7
406	24	61	2025-05-07 10:49:51.908175	7
407	24	67	2025-05-07 10:49:51.924364	7
408	24	88	2025-05-07 10:49:51.938032	7
409	24	89	2025-05-07 10:49:51.954271	7
410	24	125	2025-05-07 10:49:51.971207	7
411	24	70	2025-05-07 10:49:51.988989	7
412	24	71	2025-05-07 10:49:52.001038	7
413	24	90	2025-05-07 10:49:52.005853	7
414	24	91	2025-05-07 10:49:52.010823	7
415	24	126	2025-05-07 10:49:52.016067	7
416	24	72	2025-05-07 10:49:52.022089	7
417	24	73	2025-05-07 10:49:52.026968	7
418	24	92	2025-05-07 10:49:52.031518	7
419	24	93	2025-05-07 10:49:52.036381	7
420	24	127	2025-05-07 10:49:52.041243	7
421	24	76	2025-05-07 10:49:52.04726	7
422	24	79	2025-05-07 10:49:52.052241	7
423	24	94	2025-05-07 10:49:52.057213	7
424	24	95	2025-05-07 10:49:52.061971	7
425	24	128	2025-05-07 10:49:52.066498	7
426	25	7	2025-05-09 06:37:40.047875	7
427	25	8	2025-05-09 06:37:40.053657	7
428	25	9	2025-05-09 06:37:40.058546	7
429	25	10	2025-05-09 06:37:40.063319	7
430	25	11	2025-05-09 06:37:40.068876	7
431	25	12	2025-05-09 06:37:40.073662	7
432	25	13	2025-05-09 06:37:40.079957	7
433	25	14	2025-05-09 06:37:40.084681	7
434	25	15	2025-05-09 06:37:40.089342	7
435	25	16	2025-05-09 06:37:40.093806	7
436	25	17	2025-05-09 06:37:40.100005	7
437	25	18	2025-05-09 06:37:40.104615	7
438	25	19	2025-05-09 06:37:40.109197	7
439	25	20	2025-05-09 06:37:40.113742	7
440	25	21	2025-05-09 06:37:40.11829	7
441	25	22	2025-05-09 06:37:40.123875	7
442	25	23	2025-05-09 06:37:40.128597	7
443	25	24	2025-05-09 06:37:40.133255	7
444	25	25	2025-05-09 06:37:40.137872	7
445	25	26	2025-05-09 06:38:04.18774	7
446	25	27	2025-05-09 06:38:04.192981	7
447	25	28	2025-05-09 06:38:04.197533	7
448	25	29	2025-05-09 06:38:04.2023	7
449	25	30	2025-05-09 06:38:04.207209	7
450	25	32	2025-05-09 06:38:04.213595	7
451	25	33	2025-05-09 06:38:04.218219	7
452	25	34	2025-05-09 06:38:04.222809	7
453	25	35	2025-05-09 06:38:04.227524	7
454	25	36	2025-05-09 06:38:04.232099	7
455	25	37	2025-05-09 06:38:04.238014	7
456	25	38	2025-05-09 06:38:04.24286	7
457	25	39	2025-05-09 06:38:04.248399	7
458	25	41	2025-05-09 06:38:04.254504	7
459	25	43	2025-05-09 06:38:04.259466	7
460	25	44	2025-05-09 06:38:04.265278	7
461	25	45	2025-05-09 06:38:04.271823	7
462	25	46	2025-05-09 06:38:04.276913	7
463	25	48	2025-05-09 06:38:04.282012	7
464	25	49	2025-05-09 06:38:04.289398	7
465	26	11	2025-05-26 07:00:52.991145	7
466	26	12	2025-05-26 07:00:52.998657	7
467	26	13	2025-05-26 07:00:53.006193	7
468	26	14	2025-05-26 07:00:53.012852	7
469	26	15	2025-05-26 07:00:53.02062	7
470	26	16	2025-05-26 07:00:53.026313	7
471	26	18	2025-05-26 07:00:53.032396	7
472	26	19	2025-05-26 07:00:53.03897	7
473	26	20	2025-05-26 07:00:53.046438	7
474	26	21	2025-05-26 07:00:53.051775	7
475	26	22	2025-05-26 07:00:53.057331	7
476	26	23	2025-05-26 07:00:53.062698	7
477	26	24	2025-05-26 07:00:53.070092	7
478	26	25	2025-05-26 07:00:53.075588	7
479	26	26	2025-05-26 07:00:53.080813	7
480	26	39	2025-05-26 07:00:53.085765	7
481	26	27	2025-05-26 07:01:19.660322	7
482	26	28	2025-05-26 07:01:19.666821	7
483	26	29	2025-05-26 07:01:19.672457	7
484	26	97	2025-05-26 07:01:19.680402	7
485	26	30	2025-05-26 07:01:19.69001	7
486	26	32	2025-05-26 07:01:19.697514	7
487	26	33	2025-05-26 07:01:19.7042	7
488	26	98	2025-05-26 07:01:19.710803	7
489	26	34	2025-05-26 07:01:19.720135	7
490	26	35	2025-05-26 07:01:19.727648	7
491	26	36	2025-05-26 07:01:19.735073	7
492	26	99	2025-05-26 07:01:19.742438	7
493	26	37	2025-05-26 07:01:19.752696	7
494	26	38	2025-05-26 07:01:19.761525	7
495	26	40	2025-05-26 07:01:19.771837	7
496	26	100	2025-05-26 07:01:19.780703	7
497	26	41	2025-05-26 07:01:49.789366	7
498	26	43	2025-05-26 07:01:49.795552	7
499	26	44	2025-05-26 07:01:49.80145	7
500	26	103	2025-05-26 07:01:49.807365	7
501	26	80	2025-05-26 07:01:49.812958	7
502	26	47	2025-05-26 07:01:49.822024	7
503	26	49	2025-05-26 07:01:49.827855	7
504	26	104	2025-05-26 07:01:49.833375	7
505	26	81	2025-05-26 07:01:49.84019	7
506	26	50	2025-05-26 07:01:49.849001	7
507	26	52	2025-05-26 07:01:49.855008	7
508	26	105	2025-05-26 07:01:49.861366	7
509	26	82	2025-05-26 07:01:49.867855	7
510	26	58	2025-05-26 07:01:49.874974	7
511	26	53	2025-05-26 07:01:49.881211	7
512	26	54	2025-05-26 07:01:49.887113	7
513	26	84	2025-05-26 07:01:49.892178	7
514	26	55	2025-05-26 07:02:04.266692	7
515	26	56	2025-05-26 07:02:04.272115	7
516	26	110	2025-05-26 07:02:04.278299	7
517	26	83	2025-05-26 07:02:04.284675	7
518	26	57	2025-05-26 07:02:04.292009	7
519	26	115	2025-05-26 07:02:04.304589	7
520	26	85	2025-05-26 07:02:04.313377	7
521	26	59	2025-05-26 07:02:04.323961	7
522	26	60	2025-05-26 07:02:04.332326	7
523	26	116	2025-05-26 07:02:04.340547	7
524	26	86	2025-05-26 07:02:04.348851	7
525	26	61	2025-05-26 07:02:04.357574	7
526	26	120	2025-05-26 07:02:04.365547	7
527	26	87	2025-05-26 07:02:04.371756	7
528	26	63	2025-05-26 07:02:20.148655	7
529	26	64	2025-05-26 07:02:20.154859	7
530	26	121	2025-05-26 07:02:20.162193	7
531	26	88	2025-05-26 07:02:20.168855	7
532	26	65	2025-05-26 07:02:20.177161	7
533	26	66	2025-05-26 07:02:20.18287	7
534	26	122	2025-05-26 07:02:20.189558	7
535	26	89	2025-05-26 07:02:20.195165	7
536	26	67	2025-05-26 07:02:20.202209	7
537	26	68	2025-05-26 07:02:20.208666	7
538	26	125	2025-05-26 07:02:20.21491	7
539	26	90	2025-05-26 07:02:20.220982	7
540	26	69	2025-05-26 07:02:20.22859	7
541	26	70	2025-05-26 07:02:20.235323	7
542	26	126	2025-05-26 07:02:20.242013	7
543	26	91	2025-05-26 07:02:20.248717	7
544	26	71	2025-05-26 07:02:39.569869	7
545	26	72	2025-05-26 07:02:39.575677	7
546	26	127	2025-05-26 07:02:39.581909	7
547	26	92	2025-05-26 07:02:39.587167	7
548	26	73	2025-05-26 07:02:39.59349	7
549	26	74	2025-05-26 07:02:39.598624	7
550	26	128	2025-05-26 07:02:39.60439	7
551	26	75	2025-05-26 07:02:39.610951	7
552	26	76	2025-05-26 07:02:39.617845	7
553	26	129	2025-05-26 07:02:39.623183	7
554	26	93	2025-05-26 07:02:39.628893	7
555	26	77	2025-05-26 07:02:39.635373	7
556	26	78	2025-05-26 07:02:39.64214	7
557	26	130	2025-05-26 07:02:39.648514	7
558	26	94	2025-05-26 07:02:39.654106	7
559	26	79	2025-05-26 07:03:31.475035	7
560	26	164	2025-05-26 07:03:31.480588	7
561	26	131	2025-05-26 07:03:31.485725	7
562	26	132	2025-05-26 07:03:31.490747	7
563	26	165	2025-05-26 07:03:31.499601	7
564	26	166	2025-05-26 07:03:31.506742	7
565	26	133	2025-05-26 07:03:31.513819	7
566	26	95	2025-05-26 07:03:31.52029	7
567	26	167	2025-05-26 07:03:31.525844	7
568	26	168	2025-05-26 07:03:31.5305	7
569	26	134	2025-05-26 07:03:31.535786	7
570	26	135	2025-05-26 07:03:31.540647	7
571	26	169	2025-05-26 07:03:31.546497	7
572	26	170	2025-05-26 07:03:31.551333	7
573	26	136	2025-05-26 07:03:31.556849	7
574	26	96	2025-05-26 07:03:31.561492	7
575	26	172	2025-05-26 07:03:58.142714	7
576	26	173	2025-05-26 07:03:58.161492	7
577	26	158	2025-05-26 07:03:58.168591	7
578	26	176	2025-05-26 07:03:58.18215	7
579	26	178	2025-05-26 07:03:58.199165	7
580	30	1	2025-06-24 08:10:36.585775	7
581	30	2	2025-06-24 08:10:36.596413	7
582	30	3	2025-06-24 08:10:36.604042	7
583	30	5	2025-06-24 08:10:36.611018	7
584	30	11	2025-06-24 08:10:36.618051	7
585	30	12	2025-06-24 08:10:36.626812	7
586	30	6	2025-06-24 08:10:36.637099	7
587	30	7	2025-06-24 08:10:36.645686	7
588	30	8	2025-06-24 08:10:36.655586	7
589	30	9	2025-06-24 08:10:36.664806	7
590	30	13	2025-06-24 08:10:36.672038	7
591	30	14	2025-06-24 08:10:36.67978	7
592	30	10	2025-06-24 08:10:36.689167	7
593	30	15	2025-06-24 08:10:36.696547	7
594	30	16	2025-06-24 08:10:36.704974	7
595	30	17	2025-06-24 08:10:36.711939	7
596	30	18	2025-06-24 08:10:36.719669	7
597	30	19	2025-06-24 08:10:36.728148	7
598	30	20	2025-06-24 08:10:36.735408	7
599	30	21	2025-06-24 08:10:36.742599	7
600	30	22	2025-06-24 08:10:36.748818	7
601	30	23	2025-06-24 08:10:58.950323	7
602	30	24	2025-06-24 08:10:58.957452	7
603	30	25	2025-06-24 08:10:58.962434	7
604	30	26	2025-06-24 08:10:58.967289	7
605	30	27	2025-06-24 08:10:58.973914	7
606	30	28	2025-06-24 08:10:58.978945	7
607	30	29	2025-06-24 08:10:58.983944	7
608	30	30	2025-06-24 08:10:58.988752	7
609	30	32	2025-06-24 08:10:58.994568	7
610	30	34	2025-06-24 08:10:58.999338	7
611	30	35	2025-06-24 08:10:59.003947	7
612	30	36	2025-06-24 08:10:59.008884	7
613	30	37	2025-06-24 08:10:59.015473	7
614	30	38	2025-06-24 08:10:59.020424	7
615	30	39	2025-06-24 08:10:59.025291	7
616	30	43	2025-06-24 08:10:59.03001	7
617	30	44	2025-06-24 08:11:15.858882	7
618	30	46	2025-06-24 08:11:15.87739	7
619	30	47	2025-06-24 08:11:15.891314	7
620	30	48	2025-06-24 08:11:15.896305	7
621	30	49	2025-06-24 08:11:15.902272	7
622	30	50	2025-06-24 08:11:15.907026	7
623	30	51	2025-06-24 08:11:15.91722	7
624	30	52	2025-06-24 08:11:15.922242	7
625	30	58	2025-06-24 08:11:15.92789	7
626	30	53	2025-06-24 08:11:15.932616	7
627	30	54	2025-06-24 08:11:15.937278	7
628	30	55	2025-06-24 08:11:15.941991	7
629	30	56	2025-06-24 08:11:15.94779	7
630	30	57	2025-06-24 08:11:15.952606	7
631	30	59	2025-06-24 08:11:15.957421	7
632	30	60	2025-06-24 08:11:15.962062	7
633	29	32	2025-08-30 13:05:37.189448	1
634	29	34	2025-08-30 13:05:37.189451	1
635	29	36	2025-08-30 13:05:37.189452	1
636	29	37	2025-08-30 13:05:37.189452	1
637	29	4	2025-08-30 13:05:37.189453	1
638	29	39	2025-08-30 13:05:37.189453	1
639	29	12	2025-08-30 13:05:37.189453	1
640	29	17	2025-08-30 13:05:37.189454	1
641	29	178	2025-08-30 13:05:37.189454	1
642	29	51	2025-08-30 13:05:37.189455	1
643	29	20	2025-08-30 13:05:37.189455	1
644	29	21	2025-08-30 13:05:37.189455	1
645	29	22	2025-08-30 13:05:37.189456	1
646	29	53	2025-08-30 13:05:37.189456	1
647	29	25	2025-08-30 13:05:37.189456	1
648	29	26	2025-08-30 13:05:37.189457	1
649	29	29	2025-08-30 13:05:37.189457	1
650	31	1	2025-09-12 15:10:48.490514	1
651	31	2	2025-09-12 15:10:48.490515	1
652	31	3	2025-09-12 15:10:48.490516	1
653	31	5	2025-09-12 15:10:48.490516	1
654	31	6	2025-09-12 15:10:48.490516	1
655	31	7	2025-09-12 15:10:48.490517	1
656	31	8	2025-09-12 15:10:48.490517	1
657	31	9	2025-09-12 15:10:48.490517	1
658	31	206	2025-09-12 15:10:48.490517	1
659	31	207	2025-09-12 15:10:48.490518	1
660	31	208	2025-09-12 15:10:48.490518	1
661	31	209	2025-09-12 15:10:48.490518	1
\.


--
-- Data for Name: webinar; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.webinar (id, title, url, date, is_programming, is_manual, is_excel, homework_number, category, for_beginners, for_basic, for_advanced, for_expert, for_mocks, for_practice, for_minisnap, created_by_id, cover_url, academic_year, for_summer, exam_type, for_oge_part1, for_oge_part2, for_oge_hard) FROM stdin;
206	Комбинаторика. Задание 8	https://3.shkolkovo.online/lesson/34243	2025-09-15	f	f	f	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2015.09__7e8f8.jpg	2026	f	ege	f	f	f
209	Электронные таблицы. Задания 3 и 18	https://3.shkolkovo.online/lesson/34240	2025-09-22	f	f	t	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2022.09__7e8n0.jpg	2026	f	ege	f	f	f
211	Программирование. Задания 9 и 17	https://3.shkolkovo.online/lesson/34238	2025-09-25	t	f	f	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2025.09__7e8n3.jpg	2026	f	ege	f	f	f
212	Программирование. Задание 8. Модуль itertools	https://3.shkolkovo.online/lesson/34237	2025-09-29	t	f	f	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2029.09__7e8ne.jpg	2026	f	ege	f	f	f
213	Задание 13. IP-адресация в сети интернет	https://3.shkolkovo.online/lesson/34236	2025-09-30	f	t	f	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2030.09__7e8n5.jpg	2026	f	ege	f	f	f
216	Базовые задания ЕГЭ. Задания 1, 4, 10	https://3.shkolkovo.online/lesson/34216	2025-10-14	f	t	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
220	Программирование. Задание 24. Регулярные выражения	https://3.shkolkovo.online/lesson/34220	2025-10-23	t	f	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
6	(ролик) Python для начинающих. Занятие 5: Вложенные циклы	https://3.shkolkovo.online/lesson/27746	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(56)%20(1)__57l3n.jpg	2026	f	ege	f	f	f
225	Практика программирования. Динамическое программирование	https://3.shkolkovo.online/lesson/34244	2025-09-27	f	f	f	\N	\N	f	f	t	f	f	f	f	1		2026	f	ege	f	f	f
226	Практика программирования. Использование списков	https://3.shkolkovo.online/lesson/34224	2025-10-04	f	f	f	\N	\N	f	f	t	f	f	f	f	1		2026	f	ege	f	f	f
231	Вся теория по системам счисления, необходимая для ОГЭ по информатике	https://3.shkolkovo.online/lesson/34987	2025-09-21	f	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2021.09__7czcw.jpg	2026	f	oge	t	f	f
235	Вся теория по графам, необходимая для ОГЭ по информатике	https://3.shkolkovo.online/lesson/34995	2025-10-05	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
237	Графы. Дополнительная практика. Решаем задачи №4 из ОГЭ по информатике.	https://3.shkolkovo.online/lesson/34999	2025-10-12	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
248	Как написать свою первую программу на Python? Типы данных, арифметические выражения, ввод-вывод в Python	https://3.shkolkovo.online/lesson/34985	2025-09-16	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2016.09__7czct.jpg	2026	f	oge	f	f	f
251	Циклы. Цикл с условием (цикл while) в Python	https://3.shkolkovo.online/lesson/34997	2025-10-07	t	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	f	f	f
256	ХАРД ПРОГА - 2. Углубление в программирование	https://3.shkolkovo.online/lesson/34990	2025-09-26	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2026.09__7czcy.jpg	2026	f	oge	f	f	t
207	Кодирование информации. Задание 7	https://3.shkolkovo.online/lesson/34242	2025-09-16	f	t	f	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2016.09__7e8mu.jpg	2026	f	ege	f	f	f
208	Кодирование информации. Задания 7, 11	https://3.shkolkovo.online/lesson/34241	2025-09-18	f	t	f	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2018.09__7e8mz.jpg	2026	f	ege	f	f	f
210	Электронные таблицы. Задание 9	https://3.shkolkovo.online/lesson/34239	2025-09-23	f	f	t	\N	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%93%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BA%D1%83%D1%80%D1%81%2025-26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%98%D0%BD%D1%84%D0%91%D0%A3%20-%20%D0%95%D0%93%D0%AD-%2023.09__7e8n2.jpg	2026	f	ege	f	f	f
214	Программирование. Алгоритмы. Задания 5, 12	https://3.shkolkovo.online/lesson/34214	2025-10-02	t	f	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
224	Практика программирования. Теория чисел	https://3.shkolkovo.online/lesson/34245	2025-09-20	f	f	f	\N	\N	f	f	t	f	f	f	f	1		2026	f	ege	f	f	f
229	Задания 26. Основы построения моделей	https://3.shkolkovo.online/lesson/34227	2025-11-01	t	f	f	\N	\N	f	f	t	f	f	f	f	1		2026	f	ege	f	f	f
233	Системы счисления. Дополнительная практика. Решаем задачи №10 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/34991	2025-09-28	f	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2028.09__7czcz.jpg	2026	f	oge	t	f	f
236	Графы. Решаем задание №4 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/34996	2025-10-07	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
238	Графы. Решаем задание №9 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/35000	2025-10-21	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
249	Ветвление в Python. Операторы выбора if-else	https://3.shkolkovo.online/lesson/34989	2025-09-23	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2023.09__7czcx.jpg	2026	f	oge	f	f	f
253	Условия в циклах. Поиск количества, суммы, максимума и минимума в Python	https://3.shkolkovo.online/lesson/35005	2025-10-28	t	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	f	f	f
254	Весь базовый Python необходимый для ОГЭ по информатике за вебинар. Закрепление пройденного материала и решение задач	https://3.shkolkovo.online/lesson/35008	2025-11-04	t	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	f	f	f
257	ХАРД ПРОГА - 3. Углубление в программирование. Решаем задачи уровня по проге ОГЭ и выше	https://3.shkolkovo.online/lesson/34994	2025-10-03	t	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	f	f	t
215	Алгебра логики. Задание 15	https://3.shkolkovo.online/lesson/34215	2025-10-13	f	t	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
217	Базовая прога. Задания 6 (черепаха) и 14 (системы счисления)	https://3.shkolkovo.online/lesson/34217	2025-10-16	t	f	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
222	Программирование. Теория игр. Рекурсия. Задания 19-21	https://3.shkolkovo.online/lesson/34222	2025-10-28	t	f	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
227	Базовые задания 26. Программирование	https://3.shkolkovo.online/lesson/34225	2025-10-18	t	f	f	\N	\N	f	f	t	f	f	f	f	1		2026	f	ege	f	f	f
228	Базовые задания 26. Программирование	https://3.shkolkovo.online/lesson/34226	2025-10-25	t	f	f	\N	\N	f	f	t	f	f	f	f	1		2026	f	ege	f	f	f
232	Системы счисления. Решаем задание №10 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/34988	2025-09-23	f	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2023.09__7czch.jpg	2026	f	oge	t	f	f
239	Кодирование информации. Изучение с самого нуля для ОГЭ по информатике 2026	https://3.shkolkovo.online/lesson/35004	2025-10-28	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
240	Графы. Дополнительная практика. Решаем задачи №9 из ОГЭ по информатике.	https://3.shkolkovo.online/lesson/35003	2025-10-26	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
245	Кодирование информации. Решаем задание №2 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/35013	2025-11-14	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
246	Программирование. Дополнительная практика. Решаем №6 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/35016	2025-11-16	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
247	Кодирование информации. Дополнительная практика. Решаем №2 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/35015	2025-11-16	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
219	Программирование. Задание 24. Метод двух указателей	https://3.shkolkovo.online/lesson/34219	2025-10-21	t	f	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
218	Программирование. Задание 25	https://3.shkolkovo.online/lesson/34218	2025-10-20	t	f	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
221	Программирование. Рекурсия. Задания 16 и 23	https://3.shkolkovo.online/lesson/34221	2025-10-27	t	f	f	\N	\N	f	t	f	f	f	f	f	1		2026	f	ege	f	f	f
230	Системы счисления. Изучение с самого нуля для ОГЭ по информатике 2026. Теория	https://3.shkolkovo.online/lesson/34984	2025-09-16	f	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2016.09%20(1)__7czfs.jpg	2026	f	oge	t	f	f
234	Графы. Изучение с самого нуля для ОГЭ по информатике 2026. Теория	https://3.shkolkovo.online/lesson/34992	2025-09-30	f	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2030.09__7czcj.jpg	2026	f	oge	t	f	f
241	Вся теория по кодированию информации, необходимая для ОГЭ по информатике	https://3.shkolkovo.online/lesson/35007	2025-11-02	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
242	Кодирование информации. Решаем задание №1 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/35009	2025-11-04	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
243	Решаем задание №6 из ОГЭ по информатике. Анализ программы с условным оператором	https://3.shkolkovo.online/lesson/35012	2025-11-11	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
244	Кодирование информации. Дополнительная практика. Решаем №1 из ОГЭ по информатике	https://3.shkolkovo.online/lesson/35011	2025-11-09	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	t	f	f
250	Вложенное ветвление в Python	https://3.shkolkovo.online/lesson/34993	2025-09-30	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2016.09-1__7czd3.jpg	2026	f	oge	f	f	f
252	Цикл со счётчиком. Цикл for в Python	https://3.shkolkovo.online/lesson/35001	2025-10-21	t	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	f	f	f
255	ХАРД ПРОГА - 1. Посмотрел летник полностью? Вообще все там понимаешь? Тебе сюда! Вебинар быстрое подробное повторение	https://3.shkolkovo.online/lesson/34986	2025-09-19	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/26%20-%20%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20-%20%D0%9E%D0%93%D0%AD%20-%20%D0%98%D0%BD%D1%84%20-%2019.09__7czcp.jpg	2026	f	oge	f	f	t
258	ХАРД СИСТЕМЫ СЧИСЛЕНИЯ - 1. Посмотрел все уроки по системам счисления и всё понял? Тебе сюда! Углубляемся в системы счисления	https://3.shkolkovo.online/lesson/34998	2025-10-10	f	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	f	f	t
259	ХАРД КОМБО - 1. Прога + системы счисления	https://3.shkolkovo.online/lesson/35002	2025-10-24	t	f	f	\N	\N	f	f	f	f	f	f	f	1		2026	f	oge	f	f	t
137	Кластеризация. DBSCAN	https://3.shkolkovo.online/lesson/29852	2025-04-18	t	f	f	\N	2	f	f	f	t	f	f	f	1		2025	\N	ege	\N	\N	\N
5	(ролик) Python для начинающих. Занятие 4: Цикл FOR	https://3.shkolkovo.online/lesson/27745	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(55)%20(1)__57l3s.jpg	2026	f	ege	f	f	f
1	(ролик) Python для начинающих. Занятие 1: Введение. Переменная, операторы, линейные алгоритмы.	https://3.shkolkovo.online/lesson/27742	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(52)%20(1)__57l41.jpg	2026	f	ege	f	f	f
2	(ролик) Python для начинающих. Занятие 2: Операторы условия	https://3.shkolkovo.online/lesson/27743	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(53)%20(1)__57l3z.jpg	2026	f	ege	f	f	f
3	(ролик) Python для начинающих. Занятие 3: Цикл WHILE	https://3.shkolkovo.online/lesson/27744	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(54)%20(1)__57l3v.jpg	2026	f	ege	f	f	f
4	(ролик) Что такое функция в Python?	https://3.shkolkovo.online/lesson/29276	2025-02-11	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%91%D0%A3_%D0%A0%D0%BE%D0%BB%D0%B8%D0%BA_11.02.2025__5stks.jpg	2026	f	ege	f	f	f
11	(№7) Кодирование информации. Изображения. Задание 7	https://3.shkolkovo.online/lesson/26083	2024-09-16	f	t	\N	1	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/2024-%D0%A1%D1%82%D0%B0%D1%80%D1%82%D0%93%D0%9A-%D0%95%D0%93%D0%AD-%D0%91%D1%83__4kl8p.jpg	2025	\N	ege	\N	\N	\N
12	(№7, №11) Кодирование информации. Звук и пароли. Задания 7 и 11	https://3.shkolkovo.online/lesson/26084	2024-09-17	f	t	\N	2	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-17__4iwnr.png	2025	\N	ege	\N	\N	\N
13	(№8) Комбинаторика. Подсчёт слов	https://3.shkolkovo.online/lesson/26085	2024-09-18	f	t	\N	3	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-18__4iwns.png	2025	\N	ege	\N	\N	\N
14	(№9) Электронные таблицы. Задание 9. Подсчёт количества строк	https://3.shkolkovo.online/lesson/26086	2024-09-23	f	f	t	4	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-23__4iwny.png	2025	\N	ege	\N	\N	\N
15	(№8) Комбинаторика. Программирование	https://3.shkolkovo.online/lesson/26087	2024-09-24	t	f	\N	5	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-24__4iwo1.png	2025	\N	ege	\N	\N	\N
16	(№3) Электронные таблицы. Задание 3.	https://3.shkolkovo.online/lesson/26088	2024-09-25	f	f	t	6	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-25__4iwo3.png	2025	\N	ege	\N	\N	\N
17	(ролик) Основы алгебры логики. Теория	https://3.shkolkovo.online/lesson/27486	2024-11-05	f	t	\N	7	1	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
18	(№15) Алгебра логики. Задание 15. Отрезки, множества, неравенства. Решение на бумаге	https://3.shkolkovo.online/lesson/26089	2024-09-30	f	t	\N	7	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-30__4iwoa.png	2025	\N	ege	\N	\N	\N
19	Анализ алгоритмов и поиск ошибок в программе. Анализ функций и системы счисления.	https://3.shkolkovo.online/lesson/26097	2024-10-23	t	f	\N	15	\N	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-16__4qxd9.jpg	2025	\N	ege	\N	\N	\N
20	(№19, 20, 21) Теория игр. Задания на камушки. 1 и 2 кучи. Решение на бумаге.	https://3.shkolkovo.online/lesson/26090	2024-10-01	f	t	\N	8	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-01__4qxcp.jpg	2025	\N	ege	\N	\N	\N
21	(№2, №5, №14) Программирование. Переборные решения. Задания 2, 5, 14.	https://3.shkolkovo.online/lesson/26091	2024-10-02	t	f	\N	9	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-02__4qxcs.jpg	2025	\N	ege	\N	\N	\N
22	(№1, №4, №13) Базовые задания. Задания 1 и 4. IP-адресация, задание 13.	https://3.shkolkovo.online/lesson/26092	2024-10-14	f	t	\N	10	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-10-07__4qxcw.jpg	2025	\N	ege	\N	\N	\N
23	(№24) Программирование. Задание 24. Решения проходом по строке.	https://3.shkolkovo.online/lesson/26093	2024-10-15	t	f	\N	11	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-08__4qxcy.jpg	2025	\N	ege	\N	\N	\N
24	(№14) Системы счисления. Свойства чисел и операции.	https://3.shkolkovo.online/lesson/26094	2024-10-16	f	t	\N	12	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-09__4qxd1.jpg	2025	\N	ege	\N	\N	\N
100	Динамическое программирование. Поиск количества пар / троек.	https://3.shkolkovo.online/lesson/26148	2024-09-25	t	f	\N	4	3	f	f	f	t	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
49	(№8, №12, №17) Плюшки и фишки в проге. Задания 8, 12, 17.	https://3.shkolkovo.online/lesson/26118	2024-12-25	t	f	\N	36	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-12-25__58p36.jpg	2025	\N	ege	\N	\N	\N
25	(№16, №23) Задания 16 и 23. Рекурсия и динамическое программирование.	https://3.shkolkovo.online/lesson/26095	2024-10-21	t	f	\N	13	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-14__4qxd5.jpg	2025	\N	ege	\N	\N	\N
26	(№19, 20, 21) Теория игр. Задания на камушки. Программное решение.	https://3.shkolkovo.online/lesson/26096	2024-10-22	t	f	\N	14	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-15__4qxd6.jpg	2025	\N	ege	\N	\N	\N
53	(№18, №22) Электронные таблицы. Задание 18 (нестандарт), задание 22.	https://3.shkolkovo.online/lesson/26123	2025-01-14	f	f	t	40	1	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
7	(ролик) Python для начинающих. Занятие 6: Переборные алгоритмы	https://3.shkolkovo.online/lesson/27747	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(57)%20(1)__57l3h.jpg	2026	f	ege	f	f	f
8	(ролик) Python для начинающих. Занятие 7: Списки	https://3.shkolkovo.online/lesson/27748	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(58)%20(1)__57l3g.jpg	2026	f	ege	f	f	f
9	(ролик) Python для начинающих. Занятие 8: Строки	https://3.shkolkovo.online/lesson/27749	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(59)%20(1)__57l3d.jpg	2026	f	ege	f	f	f
10	(ролик) Python для начинающих. Занятие 9: Генераторы списков	https://3.shkolkovo.online/lesson/27750	2024-11-01	t	f	f	\N	1	t	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/maxresdefault%20(60)%20(1)__57l3b.jpg	2026	f	ege	f	f	f
27	(№15) Задание 15. Программные решения. ДЕЛ, конъюнкция, неравенства, отрезки.	https://3.shkolkovo.online/lesson/26098	2024-10-23	t	f	\N	16	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-21__4qxdc.jpg	2025	\N	ege	\N	\N	\N
28	(№17) Задание 17: от простейших задач и до предела. Пары, тройки.	https://3.shkolkovo.online/lesson/26099	2024-10-29	t	f	\N	17	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-22__4qxdg.jpg	2025	\N	ege	\N	\N	\N
30	(№25) Программирование. Задание 25. Поиск делителей, маски.	https://3.shkolkovo.online/lesson/26101	2024-11-04	t	f	\N	19	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-28__4qxdo.jpg	2025	\N	ege	\N	\N	\N
32	(№6, №8) Программирование. Модули. Задание 8 (itertools). Задание 6 (turtle).	https://3.shkolkovo.online/lesson/26103	2024-11-06	t	f	\N	21	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-30__4qxdt.jpg	2025	\N	ege	\N	\N	\N
33	(ролик) Задание 15. Метод СКОВОРОДКИ! Уничтожаем ЕГЭ по информатике 2025	https://3.shkolkovo.online/lesson/27621	2024-11-14	f	t	f	\N	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/photo_2024-11-14_13-20-33__54e7i.jpg	2025	\N	ege	\N	\N	\N
34	(№3, №9) Прогон по электронным таблицам. Задания 3 и 9.	https://3.shkolkovo.online/lesson/26104	2024-11-24	f	f	t	24	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-11__4zvl9.png	2025	\N	ege	\N	\N	\N
36	(№1, №4, №10, №13) Прогон по базовым заданиям. Задания 1, 4, 10, 13.	https://3.shkolkovo.online/lesson/26106	2024-11-20	f	t	\N	23	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-13__4zvko.png	2025	\N	ege	\N	\N	\N
37	(№5, №12, №14) Программирование. Переборные решения. Задания 5, 12, 14.	https://3.shkolkovo.online/lesson/26107	2024-11-25	t	f	\N	25	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-18__4zvls.png	2025	\N	ege	\N	\N	\N
38	(№2, №8, №13) Программирование. Использование модулей. Задания 2, 8, 13.	https://3.shkolkovo.online/lesson/26108	2024-11-26	t	f	\N	26	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-19__4zvkt.png	2025	\N	ege	\N	\N	\N
39	Как переиграть и уничтожить теорию игр | Задания 19, 20, 21 | ЕГЭ по информатике	https://3.shkolkovo.online/lesson/27358	2024-10-27	t	t	\N	38	1	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
40	(№16, №19, 20, 21) Рекурсия и теория игр. Задания 16 и 19, 20, 21.	https://3.shkolkovo.online/lesson/26109	2024-11-27	t	t	\N	27	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-20__4zvn6.png	2025	\N	ege	\N	\N	\N
41	(№24) Программирование. Задание 24. Нестандартные приёмы и решения.	https://3.shkolkovo.online/lesson/26110	2024-12-09	t	f	\N	28	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-25__4zvo4.png	2025	\N	ege	\N	\N	\N
42	(№7) Кодирование информации. Задание 7. Изображения, звук, передача данных.	https://3.shkolkovo.online/lesson/26111	2024-12-10	f	t	\N	29	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-26__4zvm9.png	2025	\N	ege	\N	\N	\N
44	(№5, №6) Программирование. Задания 5 и 6.	https://3.shkolkovo.online/lesson/26113	2024-12-16	t	f	\N	31	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-12-16-01__58p2q.jpg	2025	\N	ege	\N	\N	\N
46	(№15) Алгебра логики. Задание 15. Решение на бумаге.	https://3.shkolkovo.online/lesson/26115	2024-12-18	f	t	\N	33	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-12-18-01__58p42.jpg	2025	\N	ege	\N	\N	\N
29	(№18, №22) Электронные таблицы. Задание 18: робот, ладья. Задание 22: процессы.	https://3.shkolkovo.online/lesson/26100	2024-10-30	f	f	t	18	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-23__4qxdk.jpg	2025	\N	ege	\N	\N	\N
35	(№18, №22) Прогон по электронным таблицам. Задания 18 и 22.	https://3.shkolkovo.online/lesson/26105	2024-11-19	f	f	t	22	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-12__4zvne.png	2025	\N	ege	\N	\N	\N
43	(№25) Программирование. Задание 25.	https://3.shkolkovo.online/lesson/26112	2024-12-11	t	f	f	30	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-11-27__4zvod.png	2025	\N	ege	\N	\N	\N
45	(№14) Системы счисления. Всё, что нужно знать для ЕГЭ.	https://3.shkolkovo.online/lesson/26114	2024-12-17	t	t	f	32	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-12-17__58p3s.jpg	2025	\N	ege	\N	\N	\N
47	(№8) Комбинаторика. Задание 8. Решение на бумаге + программирование.	https://3.shkolkovo.online/lesson/26116	2024-12-23	t	t	\N	34	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-12-21-01__58p32.jpg	2025	\N	ege	\N	\N	\N
50	(№13) IP-адреса. Задание 13. Решение на бумаге. Нестандартные задачи.	https://3.shkolkovo.online/lesson/26119	2025-01-06	f	t	\N	37	1	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
51	(№19, 20, 21) Теория игр. Разные методы решения одной задачи.	https://3.shkolkovo.online/lesson/26120	2025-01-07	f	t	\N	38	1	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
52	(№17) Программирование. Задание 17. Максимальный нестандарт.	https://3.shkolkovo.online/lesson/26121	2025-01-08	t	f	\N	39	2	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
54	(№24) Программирование. Задание 24. Сложные задачи проходом по строке.	https://3.shkolkovo.online/lesson/26124	2025-01-15	t	f	\N	41	1	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
55	(№ 2, №5, №6, №8) Прогон по базовой проге. Задания 2, 5, 6, 8.	https://3.shkolkovo.online/lesson/26125	2025-01-20	t	f	\N	42	3	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
58	(№12) Задание 12. Решение на бумаге. От простых задач до харда. Робот, чертёжник, редактор.	https://3.shkolkovo.online/lesson/26122	2025-01-27	f	t	\N	45	1	f	t	f	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
60	(№24) Программирование. Задание 24. Дополнительные методы решения.	https://3.shkolkovo.online/lesson/28313	2025-02-04	t	f	\N	47	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-04__5onti.jpg	2025	\N	ege	\N	\N	\N
71	(№15) Алгебра логики. Задание 15. Решение на бумаге сложных задач	https://3.shkolkovo.online/lesson/28977	2025-03-10	f	t	\N	58	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-10__5z8u1.png	2025	\N	ege	\N	\N	\N
59	(№9) Программирование. Задание 9.	https://3.shkolkovo.online/lesson/28312	2025-02-03	t	f	f	46	4	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-03__5ontf.jpg	2025	\N	ege	\N	\N	\N
66	(№9) Программирование. Задание 9	https://3.shkolkovo.online/lesson/28972	2025-02-18	t	f	f	53	4	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-18__5ontv.jpg	2025	\N	ege	\N	\N	\N
67	(№13) Программирование. Задание 13 (ipaddress)	https://3.shkolkovo.online/lesson/28973	2025-02-19	t	f	f	54	4	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-19__5onu3.jpg	2025	\N	ege	\N	\N	\N
73	(№24) Программирование. Задание 24.	https://3.shkolkovo.online/lesson/28979	2025-03-20	t	f	f	63	4	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-12__6c66d.png	2025	\N	ege	\N	\N	\N
62	(№8) Комбинаторика. Задание 8. Решение на бумаге	https://3.shkolkovo.online/lesson/28968	2025-02-10	f	t	f	49	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-10__5ontm.jpg	2025	\N	ege	\N	\N	\N
70	(№18, №22) Электронные таблицы. Задания 18 и 22	https://3.shkolkovo.online/lesson/28976	2025-03-05	f	f	t	57	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-26__5onud.jpg	2025	\N	ege	\N	\N	\N
65	(№3, №9) Электронные таблицы. Задания 3 и 9	https://3.shkolkovo.online/lesson/28971	2025-02-17	f	f	t	52	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-17__5ontq.jpg	2025	\N	ege	\N	\N	\N
57	(№7, №11) Кодирование информации. Приколы в заданиях 7 и 11.	https://3.shkolkovo.online/lesson/26127	2025-01-22	f	t	f	44	3	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
68	(№4, №11) Кодирование информации. Задания 4 и 11	https://3.shkolkovo.online/lesson/28974	2025-02-24	f	t	f	55	4	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-24__5onu7.jpg	2025	\N	ege	\N	\N	\N
69	(№7) Кодирование информации. Задание 7	https://3.shkolkovo.online/lesson/28975	2025-03-04	f	t	f	56	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-25__5onu9.jpg	2025	\N	ege	\N	\N	\N
61	(№15) Алгебра логики. Задание 15. Решение на бумаге.	https://3.shkolkovo.online/lesson/28314	2025-02-05	f	t	f	48	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-05__5ontl.jpg	2025	\N	ege	\N	\N	\N
64	(№19, 20, 21) Теория игр. Задания 19, 20, 21	https://3.shkolkovo.online/lesson/28970	2025-02-12	t	t	f	51	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-12__5onto.jpg	2025	\N	ege	\N	\N	\N
56	(№25) Программирование. Задание 25. Совмещённые задачи.	https://3.shkolkovo.online/lesson/26126	2025-01-21	t	f	f	43	2	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
63	(№16, №23) Программирование, рекурсия. Задания 16 и 23	https://3.shkolkovo.online/lesson/28969	2025-02-11	t	f	f	50	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-02-11__5ontn.jpg	2025	\N	ege	\N	\N	\N
72	(№8, №25) Переборные алгоритмы. Задания 8 и 25	https://3.shkolkovo.online/lesson/28978	2025-03-11	t	f	f	59	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-11__6c65r.png	2025	\N	ege	\N	\N	\N
80	(№26) Программирование. Задание 26. Элементарные задачи.	https://3.shkolkovo.online/lesson/26128	2024-10-24	f	f	t	1	1	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-10-18__4qxew.jpg	2025	\N	ege	\N	\N	\N
81	(№26) Программирование. Задание 26. Основы построения моделей	https://3.shkolkovo.online/lesson/26129	2024-10-25	t	f	f	2	1	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-10-23__4qxey.jpg	2025	\N	ege	\N	\N	\N
82	(№26) Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/26130	2024-11-01	t	f	f	3	1	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
83	(№26) Программирование. Задание 26. Современные задачи. Концертная площадка	https://3.shkolkovo.online/lesson/26135	2024-11-08	t	f	f	4	1	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
104	Звёзды и кластеры. Часть 2.	https://3.shkolkovo.online/lesson/26163	2024-10-16	t	f	\N	8	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-09__4qxe8.jpg	2025	\N	ege	\N	\N	\N
84	(№26) Программирование. Задание 26. Сложные модели. Парковки	https://3.shkolkovo.online/lesson/26131	2024-11-15	t	f	f	5	1	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
85	(№26) Программирование. Задание 26. Современные задачи. Lambda-функции	https://3.shkolkovo.online/lesson/26132	2024-11-22	t	f	f	6	1	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
86	(№26) Программирование. Задание 26. Магазины, покупатели, конференц-залы	https://3.shkolkovo.online/lesson/26139	2024-12-06	t	f	f	8	\N	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
87	(№26) Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/26141	2024-12-20	t	f	\N	8	\N	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
88	Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/26142	2025-01-10	t	f	\N	9	\N	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
89	Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/28320	2025-01-24	t	f	\N	10	\N	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
90	Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/28988	2025-02-14	t	f	f	13	3	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
91	Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/28989	2025-02-21	t	f	f	14	3	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
92	Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/28990	2025-03-01	t	f	f	15	2	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
93	Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/28991	2025-03-09	t	f	f	16	1	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
94	Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/29847	2025-03-14	t	f	t	17	\N	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
95	Программирование. Задание 26. Базовые задачи. Электронные таблицы	https://3.shkolkovo.online/lesson/29851	2025-03-19	f	f	t	18	\N	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
96	Программирование. Задание 26. Камеры хранения + кратность (задание 27)	https://3.shkolkovo.online/lesson/29849	2025-03-24	t	f	f	20	\N	f	f	t	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9F%D1%80%D0%BE%D0%B3%D0%B0-2024-11-01__4zvpy.png	2025	\N	ege	\N	\N	\N
97	Основы эффективных решений. Поиск макс / мин пары.	https://3.shkolkovo.online/lesson/26145	2024-09-16	t	f	\N	1	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-09-23__4iwnj.png	2025	\N	ege	\N	\N	\N
98	Основы эффективных решений. Поиск количества пар / троек.	https://3.shkolkovo.online/lesson/26146	2024-09-18	t	f	\N	2	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-09-25__4iwnl.png	2025	\N	ege	\N	\N	\N
78	(№3,№22) Электронные таблицы. Задания 3, 22	https://3.shkolkovo.online/lesson/29845	2025-03-25	f	f	t	65	3	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-25__6c66i.png	2025	\N	ege	\N	\N	\N
75	(№1, №6, №12) Базовые задачи + прога. Задания 1, 6, 12	https://3.shkolkovo.online/lesson/29842	2025-03-18	t	t	f	61	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-18__6c65y.png	2025	\N	ege	\N	\N	\N
76	(№13, №17) Программирование. Задания 13 (ipaddress), задание 17	https://3.shkolkovo.online/lesson/29843	2025-03-19	t	f	f	62	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-19__6c665.png	2025	\N	ege	\N	\N	\N
79	(№24) Программирование. Задание 24	https://3.shkolkovo.online/lesson/29846	2025-03-26	t	f	f	66	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-26__6c66j.png	2025	\N	ege	\N	\N	\N
177	(№13) Задание 13. IP-адреса. Программирование + решение на бумаге.	https://3.shkolkovo.online/lesson/30512	2025-04-28	t	f	f	\N	2	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
99	Динамическое программирование. Поиск макс / мин пары.	https://3.shkolkovo.online/lesson/26147	2024-09-23	t	f	\N	3	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-09-30__4iwnm.png	2025	\N	ege	\N	\N	\N
101	Динамическое программирование. Использование списков. Время.	https://3.shkolkovo.online/lesson/26149	2024-09-30	t	f	\N	5	3	f	f	f	t	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
102	Динамическое программирование. Использование списков. Часть 2.	https://3.shkolkovo.online/lesson/26150	2024-10-02	t	f	\N	6	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-02__4qxe5.jpg	2025	\N	ege	\N	\N	\N
103	Звёзды и кластеры. Часть 1.	https://3.shkolkovo.online/lesson/26162	2024-10-14	t	f	\N	7	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-07__4qxe7.jpg	2025	\N	ege	\N	\N	\N
105	Звезды и кластеры. Часть 3.	https://3.shkolkovo.online/lesson/26164	2024-10-21	t	f	\N	9	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-14__4qxea.jpg	2025	\N	ege	\N	\N	\N
106	Динамическое программирование. Поиск подпоследовательностей.	https://3.shkolkovo.online/lesson/26151	2024-10-23	t	f	\N	10	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-16__4qxef.jpg	2025	\N	ege	\N	\N	\N
107	Пары и тройки чисел. Задачи на поиск некратной суммы.	https://3.shkolkovo.online/lesson/26152	2024-10-28	t	f	\N	11	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-21__4qxeg.jpg	2025	\N	ege	\N	\N	\N
108	Пары чисел. Задачи на поиск кратной суммы.	https://3.shkolkovo.online/lesson/26153	2024-10-30	t	f	\N	12	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-23__4qxel.jpg	2025	\N	ege	\N	\N	\N
109	Динамическое программирование. Задания на время.	https://3.shkolkovo.online/lesson/26154	2024-11-04	t	f	\N	13	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-28__4qxeo.jpg	2025	\N	ege	\N	\N	\N
110	Задания на кластеризацию.	https://3.shkolkovo.online/lesson/26627	2024-11-06	t	f	\N	14	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-10-30__4qxep.jpg	2025	\N	ege	\N	\N	\N
111	Задания на круговое движение. Часть 1.	https://3.shkolkovo.online/lesson/26157	2024-11-20	t	f	\N	15	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-13__4zvsn.png	2025	\N	ege	\N	\N	\N
112	Тройки чисел. Нестандартные задачи.	https://3.shkolkovo.online/lesson/26156	2024-11-24	t	f	\N	16	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-11__4zvsh.png	2025	\N	ege	\N	\N	\N
113	Задания на круговое движение. Часть 2.	https://3.shkolkovo.online/lesson/26158	2024-11-25	t	f	\N	17	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-18__4zvsu.png	2025	\N	ege	\N	\N	\N
114	Задания на линейное движение	https://3.shkolkovo.online/lesson/26159	2024-11-27	t	f	\N	18	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-20__4zvsz.png	2025	\N	ege	\N	\N	\N
115	Задания на кластеризацию.	https://3.shkolkovo.online/lesson/26628	2024-12-09	t	f	\N	19	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-25__4zvt4.png	2025	\N	ege	\N	\N	\N
116	Задания на кластеризацию.	https://3.shkolkovo.online/lesson/26629	2024-12-11	t	f	\N	20	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-27__4zvt6.png	2025	\N	ege	\N	\N	\N
117	Нестандартные задания. Задачи прошлых лет.	https://3.shkolkovo.online/lesson/26160	2024-12-16	t	f	\N	21	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-12-16-02__58p67.jpg	2025	\N	ege	\N	\N	\N
118	Пары и тройки чисел. Задачи на поиск кратной суммы.	https://3.shkolkovo.online/lesson/26161	2024-12-18	t	f	\N	22	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-12-18-02__58p6c.jpg	2025	\N	ege	\N	\N	\N
119	Динамическое программирование. Двумерные списки.	https://3.shkolkovo.online/lesson/26165	2024-12-23	t	f	\N	23	3	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-12-21-02__58p6i.jpg	2025	\N	ege	\N	\N	\N
120	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28322	2025-01-06	t	f	\N	24	2	f	f	f	t	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
121	Задания на кластеризацию. Метод dbscan.	https://3.shkolkovo.online/lesson/28323	2025-01-08	t	f	f	25	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-03-17__6c66r.png	2025	\N	ege	\N	\N	\N
122	Задания на кластеризацию. Функции.	https://3.shkolkovo.online/lesson/28325	2025-01-15	t	f	\N	26	1	f	f	f	t	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
123	Динамическое программирование. Пары и тройки.	https://3.shkolkovo.online/lesson/28326	2025-01-20	t	f	\N	27	3	f	f	f	t	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
124	Динамическое программирование. Префиксные суммы.	https://3.shkolkovo.online/lesson/28327	2025-01-22	t	f	\N	28	3	f	f	f	t	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
125	Задания на кластеризацию. Метод dbscan (дополнительный вебинар)	https://3.shkolkovo.online/lesson/29075	2025-02-02	t	f	f	29	1	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-03-17__6c66r.png	2025	\N	ege	\N	\N	\N
126	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28328	2025-02-03	t	f	\N	30	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-03__5onuj.jpg	2025	\N	ege	\N	\N	\N
127	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28329	2025-02-05	t	f	\N	31	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-05__5onuk.jpg	2025	\N	ege	\N	\N	\N
128	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28980	2025-02-10	t	f	\N	32	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-10__5onul.jpg	2025	\N	ege	\N	\N	\N
129	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28981	2025-02-12	t	f	\N	33	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-12__5onup.jpg	2025	\N	ege	\N	\N	\N
130	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28982	2025-02-17	t	f	\N	34	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-17__5onuq.jpg	2025	\N	ege	\N	\N	\N
131	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28983	2025-02-19	t	f	\N	35	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-19__5onus.jpg	2025	\N	ege	\N	\N	\N
132	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28984	2025-02-24	t	f	\N	36	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-24__5onut.jpg	2025	\N	ege	\N	\N	\N
133	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28985	2025-03-05	t	f	\N	37	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-26__5onuv.jpg	2025	\N	ege	\N	\N	\N
134	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28986	2025-03-10	t	f	\N	38	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-03-10__5z8u5.png	2025	\N	ege	\N	\N	\N
135	Задания на кластеризацию. Повторение материала.	https://3.shkolkovo.online/lesson/28987	2025-03-20	t	f	\N	40	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-02-12__5onup.jpg	2025	\N	ege	\N	\N	\N
136	Кластеризация. DBSCAN	https://3.shkolkovo.online/lesson/29850	2025-03-17	t	f	f	39	2	f	f	f	t	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2025-03-17__6c66r.png	2025	\N	ege	\N	\N	\N
138	Кластеризация. Функции	https://3.shkolkovo.online/lesson/29853	2025-04-25	t	f	f	\N	2	f	f	f	t	f	f	f	1		2025	\N	ege	\N	\N	\N
139	Разбор пробника №1	https://3.shkolkovo.online/lesson/26167	2024-09-28	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-28__4iwo9.png	2025	\N	ege	\N	\N	\N
140	Разбор пробника №2	https://3.shkolkovo.online/lesson/26169	2024-10-12	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-12__566gb.jpg	2025	\N	ege	\N	\N	\N
141	Разбор пробника №3	https://3.shkolkovo.online/lesson/26171	2024-10-26	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-26__566g0.jpg	2025	\N	ege	\N	\N	\N
142	Разбор пробника №4	https://3.shkolkovo.online/lesson/26173	2024-11-09	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-09__4zvty.png	2025	\N	ege	\N	\N	\N
143	Разбор пробника №5	https://3.shkolkovo.online/lesson/26175	2024-11-23	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-23__4zvub.png	2025	\N	ege	\N	\N	\N
144	Разбор пробника №6	https://3.shkolkovo.online/lesson/26177	2024-12-07	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2024-12-07__58p6t.jpg	2025	\N	ege	\N	\N	\N
145	Разбор пробника №7	https://3.shkolkovo.online/lesson/26179	2024-12-21	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2024-12-21__58p70.jpg	2025	\N	ege	\N	\N	\N
146	Разбор пробника №9	https://3.shkolkovo.online/lesson/28316	2025-01-18	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2025-01-18__5egtq.png	2025	\N	ege	\N	\N	\N
147	Разбор пробника №10	https://3.shkolkovo.online/lesson/28318	2025-02-08	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2025-02-08__5onve.jpg	2025	\N	ege	\N	\N	\N
148	Разбор пробника №11	https://3.shkolkovo.online/lesson/28993	2025-02-22	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2025-02-22__5onvi.jpg	2025	\N	ege	\N	\N	\N
149	Разбор пробника №14	https://3.shkolkovo.online/lesson/28995	2025-03-15	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-09__4zvty.png	2025	\N	ege	\N	\N	\N
150	Разбор пробника №15	https://3.shkolkovo.online/lesson/29854	2025-03-22	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-23__4zvub.png	2025	\N	ege	\N	\N	\N
151	Разбор пробника	https://3.shkolkovo.online/lesson/29855	2025-03-29	f	f	\N	\N	\N	f	f	f	f	t	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2024-12-07__58p6t.jpg	2025	\N	ege	\N	\N	\N
152	(№7) Большая нарешка. Задание 7.	https://3.shkolkovo.online/lesson/26166	2024-09-21	f	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-09-21__4iwnw.png	2025	\N	ege	\N	\N	\N
153	(№8) Большая нарешка. Задание 8.	https://3.shkolkovo.online/lesson/26168	2024-10-05	t	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-2024-10-05__566gg.jpg	2025	\N	ege	\N	\N	\N
154	(№3, №9, №18, №22) Большая нарешка. Задания 3, 9, 18, 22.	https://3.shkolkovo.online/lesson/26170	2024-10-19	f	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-19__566g9.jpg	2025	\N	ege	\N	\N	\N
155	(№4, №11) Большая нарешка. Кодирование. Задания 4 и 11.	https://3.shkolkovo.online/lesson/26172	2024-11-02	f	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-04__4zvtv.png	2025	\N	ege	\N	\N	\N
156	(№15) Большая нарешка. Алгебра логики. Задание 15.	https://3.shkolkovo.online/lesson/26174	2024-11-16	f	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-16__4zvu5.png	2025	\N	ege	\N	\N	\N
157	(№17) Большая нарешка. Задание 17.	https://3.shkolkovo.online/lesson/26176	2024-11-30	t	f	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-27-2024-11-30__4zvuf.png	2025	\N	ege	\N	\N	\N
158	(№24, №25) Большая нарешка. Задания 24 и 25.	https://3.shkolkovo.online/lesson/26178	2024-12-14	t	f	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2024-12-14__58p6x.jpg	2025	\N	ege	\N	\N	\N
159	(№11) Большая нарешка. Задание 11. Часть 1.	https://3.shkolkovo.online/lesson/28274	2024-12-19	f	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/2024-%D0%95%D0%93%D0%AD-%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%D0%92%D0%B5%D0%B1-19.12__5db65.jpg	2025	\N	ege	\N	\N	\N
160	(№13) Большая нарешка. Задание 13.	https://3.shkolkovo.online/lesson/28315	2025-01-11	f	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2025-01-11__5egto.png	2025	\N	ege	\N	\N	\N
161	(№8) Большая нарешка. Задание 8.	https://3.shkolkovo.online/lesson/28317	2025-01-25	t	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2025-01-25__5egtv.png	2025	\N	ege	\N	\N	\N
162	(№15) Большая нарешка. Задание 15.	https://3.shkolkovo.online/lesson/28992	2025-02-15	f	t	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2025-02-15__5onvg.jpg	2025	\N	ege	\N	\N	\N
163	(№9) Большая нарешка. Задание 9.	https://3.shkolkovo.online/lesson/28994	2025-03-08	t	f	\N	\N	\N	f	f	f	f	f	t	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%92%D0%B5%D0%B1-2025-03-08__5z8ty.png	2025	\N	ege	\N	\N	\N
164	Базовые задания ЕГЭ по информатике. 1, 3, 4, 10, 13.	https://3.shkolkovo.online/lesson/30085	2025-04-01	f	t	\N	\N	\N	f	f	f	f	f	f	t	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9C%D0%B8%D0%BD%D0%B8-%D1%89%D0%B5%D0%BB%D1%87%D0%BE%D0%BA-%D0%95%D0%93%D0%AD-%D0%98%D0%9D%D0%A4-01__69y07.jpg	2025	\N	ege	\N	\N	\N
165	Базовые задания ЕГЭ по информатике. 7, 8, 11. Алгебра логики, задание 15	https://3.shkolkovo.online/lesson/30086	2025-04-02	f	t	\N	\N	\N	f	f	f	f	f	f	t	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9C%D0%B8%D0%BD%D0%B8-%D1%89%D0%B5%D0%BB%D1%87%D0%BE%D0%BA-%D0%95%D0%93%D0%AD-%D0%98%D0%9D%D0%A4-02__69y3j.jpg	2025	\N	ege	\N	\N	\N
166	Программирование. Переборные алгоритмы. Задания 2, 5, 6, 8, 12, 14.	https://3.shkolkovo.online/lesson/30087	2025-04-03	t	f	\N	\N	\N	f	f	f	f	f	f	t	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9C%D0%B8%D0%BD%D0%B8-%D1%89%D0%B5%D0%BB%D1%87%D0%BE%D0%BA-%D0%95%D0%93%D0%AD-%D0%98%D0%9D%D0%A4-03__69y3k.jpg	2025	\N	ege	\N	\N	\N
167	Электронные таблицы. Задания 3, 9, 18, 22.	https://3.shkolkovo.online/lesson/30088	2025-04-04	f	f	t	\N	\N	f	f	f	f	f	f	t	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9C%D0%B8%D0%BD%D0%B8-%D1%89%D0%B5%D0%BB%D1%87%D0%BE%D0%BA-%D0%95%D0%93%D0%AD-%D0%98%D0%9D%D0%A4-04__69y3m.jpg	2025	\N	ege	\N	\N	\N
168	Программирование. Задания 9, 17, 24, 25	https://3.shkolkovo.online/lesson/30089	2025-04-05	t	f	\N	\N	\N	f	f	f	f	f	f	t	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9C%D0%B8%D0%BD%D0%B8-%D1%89%D0%B5%D0%BB%D1%87%D0%BE%D0%BA-%D0%95%D0%93%D0%AD-%D0%98%D0%9D%D0%A4-05__69y3q.jpg	2025	\N	ege	\N	\N	\N
169	Программирование. Задания 16, 23. Теория игр, задания 19, 20, 21	https://3.shkolkovo.online/lesson/30090	2025-04-06	t	f	\N	\N	\N	f	f	f	f	f	f	t	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9C%D0%B8%D0%BD%D0%B8-%D1%89%D0%B5%D0%BB%D1%87%D0%BE%D0%BA-%D0%95%D0%93%D0%AD-%D0%98%D0%9D%D0%A4-06__69y3u.jpg	2025	\N	ege	\N	\N	\N
170	Программирование. Задания 26, 27	https://3.shkolkovo.online/lesson/30091	2025-04-07	t	f	\N	\N	\N	f	f	f	f	f	f	t	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9C%D0%B8%D0%BD%D0%B8-%D1%89%D0%B5%D0%BB%D1%87%D0%BE%D0%BA-%D0%95%D0%93%D0%AD-%D0%98%D0%9D%D0%A4-07__69y3w.jpg	2025	\N	ege	\N	\N	\N
183	(№26) Задание 26. Современные задачи. Кратность суммы	https://3.shkolkovo.online/lesson/30522	2025-04-14	t	f	f	\N	\N	f	f	t	f	f	f	f	1		2025	\N	ege	\N	\N	\N
186	(№26) Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/30525	2025-04-23	t	f	f	\N	\N	f	f	t	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
187	(№26) Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/30526	2025-04-28	t	f	f	\N	\N	f	f	t	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
188	(№26) Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/30527	2025-04-30	t	f	f	\N	\N	f	f	t	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
189	(№26) Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/30528	2025-05-05	t	f	f	\N	\N	f	f	t	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
190	(№26) Программирование. Задание 26. Современные задачи.	https://3.shkolkovo.online/lesson/30529	2025-05-07	t	f	f	\N	\N	f	f	t	f	f	f	f	1	\N	2025	\N	ege	\N	\N	\N
185	(№26) Задание 26. Современные задачи. Координаты и матрешки	https://3.shkolkovo.online/lesson/30524	2025-04-21	t	f	f	\N	\N	f	f	t	f	f	f	f	1		2025	\N	ege	\N	\N	\N
184	(№26) Задание 26. Современные задачи. Столбы и координаты.	https://3.shkolkovo.online/lesson/30523	2025-04-16	t	f	f	\N	\N	f	f	t	f	f	f	f	1		2025	\N	ege	\N	\N	\N
171	(№3, №18) Электронные таблицы. Задания 3 и 18.	https://3.shkolkovo.online/lesson/30506	2025-04-14	f	f	t	\N	3	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
173	(№9, №17) Программирование. Задания 9 и 17.	https://3.shkolkovo.online/lesson/30508	2025-04-16	t	f	f	\N	4	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
174	(№22) Задание 22. Стандартные задачи и диаграммы Ганта.	https://3.shkolkovo.online/lesson/30509	2025-04-21	f	f	t	\N	1	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
179	(№24) Программирование. Задание 24. Арифметические выражения.	https://3.shkolkovo.online/lesson/30514	2025-04-30	t	f	f	\N	4	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
172	(№7, №11) Кодирование информации. Задания 7 и 11.	https://3.shkolkovo.online/lesson/30507	2025-04-15	f	t	f	\N	2	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
176	(№15) Программирование. Задание 15.	https://3.shkolkovo.online/lesson/30511	2025-04-23	t	f	f	\N	2	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
178	(№19-21) Программирование. Теория игр. Неудачный ход.	https://3.shkolkovo.online/lesson/30513	2025-04-29	t	f	f	\N	1	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
181	(№24) Программирование. Задание 24. Арифметические выражения.	https://3.shkolkovo.online/lesson/30516	2025-05-06	t	f	f	\N	4	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
182	(№23) Программирование. Задание 23. Усложненные задания.	https://3.shkolkovo.online/lesson/30517	2025-05-07	t	f	f	\N	4	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
48	(№24, №25) Программирование. Пишем однострочники. Задания 24 и 25.	https://3.shkolkovo.online/lesson/26117	2024-12-24	t	f	f	35	4	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-12-24__58p54.jpg	2025	\N	ege	\N	\N	\N
77	(№2, №5, №10) Программирование. Задания 2, 5, 10	https://3.shkolkovo.online/lesson/29844	2025-03-24	t	f	f	64	4	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-24__6c66f.png	2025	\N	ege	\N	\N	\N
31	Программирование. Задание 25. Нестандартные задачи.	https://3.shkolkovo.online/lesson/26102	2024-11-05	t	f	f	20	1	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2024-10-29__4qxdq.jpg	2025	\N	ege	\N	\N	\N
175	(№24) Программирование. Задание 24. Проход по строке. Арифметические выражения.	https://3.shkolkovo.online/lesson/30510	2025-04-22	t	f	f	\N	4	f	t	f	f	f	f	f	1		2025	\N	ege	\N	\N	\N
74	(№16, №23) Программирование. Рекурсия. Задания 16, 23	https://3.shkolkovo.online/lesson/29841	2025-03-17	t	f	f	60	2	f	t	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/%D0%95%D0%93%D0%AD-%D0%91%D0%A3-%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D0%B9-2025-03-17__6c65w.png	2025	\N	ege	\N	\N	\N
193	Основы программирования. Цикл FOR 	https://3.shkolkovo.online/lesson/32874	2025-07-12	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-hd/2025-Летник-Закрытые-ЕГЭ-Инф-12.07__6yrak.png	2026	t	ege	\N	\N	\N
195	Основы переборных решений. Часть 2	https://3.shkolkovo.online/lesson/32876	2025-07-20	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-20.07__6yrah.png	2026	t	ege	\N	\N	\N
192	Основы программирования. Цикл WHILE	https://3.shkolkovo.online/lesson/32873	2025-07-08	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-08.07__6yral.png	2026	t	ege	\N	\N	\N
199	Обработка строк. Простейшие задания 24	https://3.shkolkovo.online/lesson/32880	2025-08-05	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-05.08__6yra8.png	2026	t	ege	\N	\N	\N
200	Пользовательские функции в Python	https://3.shkolkovo.online/lesson/32881	2025-08-09	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/%D0%91%D0%A3_%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%B9%20%D0%BA%D1%83%D1%80%D1%81-09-08__70s4q.png	2026	t	ege	\N	\N	\N
201	Основы заданий 27. Разбиение на кластеры. Это должен уметь каждый	https://3.shkolkovo.online/lesson/32882	2025-08-13	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-13.08__6yra6.png	2026	t	ege	\N	\N	\N
202	Основы заданий 27. Работа с кластерами	https://3.shkolkovo.online/lesson/32883	2025-08-17	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-17.08__6yra5.png	2026	t	ege	\N	\N	\N
203	Базовые задания 26. Основы построения моделей. Продвинутое программирование	https://3.shkolkovo.online/lesson/32884	2025-08-21	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-21.08__6yra0.png	2026	t	ege	\N	\N	\N
204	Базовые задания 26. Основы построения моделей, часть 2	https://3.shkolkovo.online/lesson/32885	2025-08-25	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-25.08__6yr9z.png	2026	t	ege	\N	\N	\N
205	ТОПОВЫЕ ЛАЙФХАКИ в программировании. Сделай решение задач ПРОЩЕ!	https://3.shkolkovo.online/lesson/32886	2025-08-26	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/%D0%91%D0%A3_%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%B9%20%D0%BA%D1%83%D1%80%D1%81-26-08__70s4u.png	2026	t	ege	\N	\N	\N
197	Улучшаем навыки. Генераторы списков. То, что сделает жизнь проще	https://3.shkolkovo.online/lesson/32878	2025-07-28	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/%D0%91%D0%A3_%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%B9%20%D0%BA%D1%83%D1%80%D1%81-28-07__70s4k.png	2026	t	ege	\N	\N	\N
198	Электронные таблицы в программировании. Задание 9	https://3.shkolkovo.online/lesson/32879	2025-08-01	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-01.08__6yraa.png	2026	t	ege	\N	\N	\N
191	Что такое программа. Линейные алгоритмы и условия. Прога для самых маленьких	https://3.shkolkovo.online/lesson/32872	2025-07-04	t	f	f	\N	\N	f	f	f	f	f	f	f	1	https://3.shkolkovo.online/st/5/v-thumb/2025-%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%BA-%D0%97%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5-%D0%95%D0%93%D0%AD-%D0%98%D0%BD%D1%84-04.07__6yran.png	2026	t	ege	\N	\N	\N
194	Как решаются задания ЕГЭ. Основы переборных решений	https://3.shkolkovo.online/lesson/32875	2025-07-16	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/%D0%91%D0%A3_%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%B9%20%D0%BA%D1%83%D1%80%D1%81-16-07__70s41.png	2026	t	ege	\N	\N	\N
196	Важная база проги. Работа со списками в Python. Задание 17	https://3.shkolkovo.online/lesson/32877	2025-07-24	t	f	f	\N	\N	f	f	f	f	f	f	f	11	https://3.shkolkovo.online/st/5/v-hd/%D0%91%D0%A3_%D0%9B%D0%B5%D1%82%D0%BD%D0%B8%D0%B9%20%D0%BA%D1%83%D1%80%D1%81-24-07__70s4c.png	2026	t	ege	\N	\N	\N
\.


--
-- Data for Name: webinar_comment; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.webinar_comment (id, text, created_at, webinar_id, user_id) FROM stdin;
6	РОЛИК	2025-04-03 23:24:59.010561	17	1
7	таблицы	2025-04-03 23:24:59.047259	29	1
9	таблицы	2025-04-03 23:24:59.062332	34	1
10	таблицы	2025-04-03 23:24:59.065843	35	1
11	13-е прогой	2025-04-03 23:24:59.079793	38	1
12	ОТКРЫТЫЙ ВЕБ, таблицы	2025-04-03 23:24:59.083268	39	1
13	таблицы	2025-04-03 23:24:59.121162	51	1
14	таблицы	2025-04-03 23:24:59.126464	53	1
15	9-е прогой	2025-04-03 23:24:59.176597	59	1
16	таблицы	2025-04-03 23:24:59.196007	65	1
17	9-е прогой	2025-04-03 23:24:59.202361	66	1
18	13-е прогой	2025-04-03 23:24:59.20506	67	1
19	таблицы	2025-04-03 23:24:59.218111	70	1
20	таблицы	2025-04-03 23:24:59.258964	78	1
22	кластеры	2025-04-03 23:24:59.365275	103	1
23	кластеры	2025-04-03 23:24:59.371824	104	1
24	кластеры	2025-04-03 23:24:59.373842	105	1
25	кластеры	2025-04-03 23:24:59.388607	110	1
26	кластеры	2025-04-03 23:24:59.399287	115	1
27	кластеры	2025-04-03 23:24:59.404337	116	1
28	кластеры	2025-04-03 23:24:59.412519	120	1
29	кластеры	2025-04-03 23:24:59.414556	121	1
30	кластеры	2025-04-03 23:24:59.418509	122	1
31	кластеры	2025-04-03 23:24:59.424565	125	1
32	кластеры	2025-04-03 23:24:59.426981	126	1
33	кластеры	2025-04-03 23:24:59.429809	127	1
34	кластеры	2025-04-03 23:24:59.432107	128	1
35	кластеры	2025-04-03 23:24:59.437002	129	1
36	кластеры	2025-04-03 23:24:59.439169	130	1
37	кластеры	2025-04-03 23:24:59.441125	131	1
38	кластеры	2025-04-03 23:24:59.44356	132	1
39	кластеры	2025-04-03 23:24:59.4466	133	1
40	кластеры	2025-04-03 23:24:59.448618	134	1
41	кластеры	2025-04-03 23:24:59.459029	135	1
42	кластеры	2025-04-03 23:24:59.46214	136	1
43	кластеры	2025-04-03 23:24:59.464984	137	1
44	кластеры	2025-04-03 23:24:59.472237	138	1
45	1. Определить среднее арифметическое абсцисс центров кластеров, а также среднее арифметическое ординат центров кластеров.	2025-04-07 05:46:32.533775	103	7
46	здесь появляется понятие "мусорные данные"  1.  Определить среднее арифметическое абсцисс центров кластеров, а также среднее арифметическое ординат центров кластеров.	2025-04-07 05:50:35.752606	104	7
47	1. Определить среднее арифметическое абсцисс центров кластеров, а также среднее арифметическое ординат центров кластеров.	2025-04-07 05:51:05.064158	105	7
52	~2:08:15 №24 указателями \t-Полина	2025-04-11 11:29:04.704022	168	1
53	теоретическая базовая база - если ребенок только приступает к изучению номеров 2 и 15, то пусть начинает свое изучение с данного ролика \t-Катерина Бриль	2025-04-11 11:29:44.680585	17	1
54	❗️ Здесь основной принцип решения №15 руками.  В ролике  🔗https://3.shkolkovo.online/lesson/27621  та же самая информация, что на этом вебинаре, поэтому его даём только если ученик с первого раза не понял ❗️ Поразрядная конъюнкция не разбирается \t-Muslima Khorinova 🔺 Теория: 1. Раскрытие импликации 2. Закон де Моргана 3. Метод сковородки (время: 0:14:28) 4. Дистрибутивный закон (время: 0:35:23) \t-Muslima Khorinova 🔺 Задачи: *ДЕЛЕНИЕ* 1️⃣ Для какого наибольшего натурального числа А формула (¬ДЕЛ(x, A) ∧ ДЕЛ(x, 6)) → ¬ДЕЛ(x, 4) тождественно истинна? *ОТРЕЗКИ* 2️⃣ На числовой прямой даны два отрезка: P = [3, 13] и Q = [7, 17]. Выберите такой отрезок А, что формула ((x ∈ A) → (x ∈ P)) ∨ ¬(x ∈ Q) тождественно истинна, то есть принимает значение 1 при любом значении переменной х 3️⃣ На числовой прямой даны два отрезка: P = [10, 20] и Q = [15, 25]. Выберите такой отрезок A, что формула ((x ∈ P) → (x ∈ Q)) ∨ (x ∈ A) тождественно истинна при любом значении х? 4️⃣ На числовой прямой даны два отрезка: P = [8, 39] и Q = [23, 58]. Выберите из предложенных вариантов такой отрезок A, что логическое выражение ((x ∈ P) ∧ (x ∈ A)) → ((x ∈ Q) ∧ (x ∈ A)) тождественно истинно при любом значении x. -МНОЖЕСТВА- 5️⃣ Элементами множества A являются натуральные числа. Известно, что выражение ¬(x ∈ {2, 4, 6, 8, 10, 12}) ∨ (¬(x ∈ {3, 6, 9, 12, 15}) → (x ∈ A)) истинно (т. е. принимает значение 1) при любом значении переменной x. Определите наименьшее возможное значение произведения элементов множества А. \t-Muslima Khorinova 6️⃣ Элементами множеств A, и Q являются натуральные числа, причём P = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20} и Q = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30}. Известно, что выражение ((x ∈ A) → ¬(x ∈ P)) ∧ (¬(x ∈ Q) → ¬(x ∈ A)) истинно (т. е. принимает значение 1) при любом значении переменной x. Определите наибольшее возможное количество элементов множества A. *НЕРАВЕНСТВА* 7️⃣ Известно, что для некоторого отрезка A формула ((x ∈ A) → (x 2 ≤ 100)) ∧ ((x 2 ≤ 16) → (x ∈ A)) тождественно истинна (то есть принимает значение 1 при всех вещественных значениях переменной x). Какую наибольшую длину может иметь отрезок A? 8️⃣Сколько существует целых значений A, при которых формула ((x ≥ 15) → (x · x > A)) ∧ ((y · y ≥ A) → (y > 11)) тождественно истинна (то есть принимает значение 1 при любых целых неотрицательных значениях переменных x и y)? 9️⃣ Укажите наименьшее целое значение A, при котором выражение (y + 3x < A) ∨ (x > 20) ∨ (y > 40) истинно для любых целых положительных значений x и y. 🔟Укажите наименьшее целое значение A, при котором выражение (x ≥ 10) ∨ (x < y) ∨ (x · y < A) истинно для любых целых положительных значений x и y. \t-Muslima Khorinova	2025-04-11 11:30:20.06964	18	1
55	Может не стоит включать в планы учеников с нуля? А то 3 из 4х часов в неделю, которые они готовы заниматься, не рационально на задачи прошлых лет тратить \t-Полина	2025-04-11 11:30:57.980222	19	1
56	1. Что из себя представляет теория игр. 2. Суть решения задачи: выигрышные и проигрышные позиции. 3. *Основы программного решения*: представление в экселе для наглядности. ❗️ В 4 примере неудачный ход	2025-04-11 11:31:32.850991	20	1
57	🔺 Теория: 1. что такое бит 2. как устроено изображение 3. формула Хартли 4. в какую сторону округлять при дробном ответе 5. сжатые изображения (время: 01:00:00-01:10:00) 6. dpi(ppi) (время 01:11:00-01:27:00) 7. степень прозрачности	2025-04-11 11:34:21.306235	11	1
58	№7 🔺 Теория:  кодирование звуковой информации 	2025-04-11 11:36:12.043146	12	1
59	№11 🔺 Теория для решения номера дана на первом вебинаре по №7. 	2025-04-11 11:36:20.53461	12	1
60	Комментарий: 🔺Теория (стоит законспектировать) 1. Размещение с повторениями 2. Размещения без повторений 3. Перестановки 4. Сочетания (оливье и селедка под шубой)  ❗️ 0:28:25 - Почему нужно уметь решать №8 руками	2025-04-11 11:37:57.397689	13	1
87	🔺 Теория: Кодирование звука, информация та же, что на вебе: https://3.shkolkovo.online/lesson/26084   🔺 Задачи: базовые на изображение, степень прозрачности, сжатые изображения, классические на звук, передача файлов по каналам	2025-04-11 12:22:41.551612	42	1
61	СУПЕРБАЗА ДЛЯ EXCEL 🔺Теория 1. Разница между интерфейсами Excel и LibreOffice. Настройка интерфейса Libre под Excel. 2. Вводная информация про работу с электронными таблицы: как работаю формулы, как растянуть значения, таблицы.  3. Функции в эксель: Математические: СУММ, МАКС, МИН, НАИБОЛЬШИЙ, КОРЕНЬ, ПРОИЗВЕД, ОСТАТ Логические: ЕСЛИ, СУММЕСЛИ, СЧЁТЕСЛИ	2025-04-11 11:39:31.40586	14	1
62	🔺  Способы решения: 1. Вложенные циклы 2. Подключение стандартных библиотек: itertools 3. Комбинаторика + прога. Прогноз от БУ на ЕГЭ 2024.   📎 Использование set() 📎 Ответ на вопрос "почему БУ?"	2025-04-11 11:41:22.653758	15	1
63	🔺Теория 1. ВПР - принцип работы 2. Конкатенация ячеек (сцепление)	2025-04-11 11:43:06.128894	16	1
64	Теория: 🔹32:32 - Функция перевода в любую с.с. прогой (на примере перевода в 3 с.с.) 🔹54:39 - Как работают срезы?	2025-04-11 11:55:18.458701	21	1
65	Теория (чуть-чуть теории): 🔹 Условие Фано 🔹Алгоритм Хаффмана	2025-04-11 11:57:30.388784	22	1
66	Теория: 🔹IP-адресация 🔹Суть поразрядной конъюнкции	2025-04-11 11:57:42.088603	22	1
67	Теория: 🔹Как работает функция map 🔹Функция eval 🔹Решение задач через функции replace и split	2025-04-11 12:00:00.786563	23	1
68	Теория: 🔹Системы счисления (основная теория, суть, виды: позиционные системы счисления) 🔹11:57 - Как перевести число любой с.с. в 10 с.с. (суть метода) 🔹19:11 - Как быстро перевести число из 10 с.с. в 2 с.с.	2025-04-11 12:01:02.022089	24	1
69	Теория: 🔹Динамическое программирование (суть метода) 🔹8:05 - Что такое ряд Фибоначчи? 🔹9:36 - Рекурсивная функция 🔹12:38 - Библиотека lru_cash ⠀⠀⠀⠀– 19:46 - применение 🔹13:38 - Решение задачи по поиску чисел Фибоначчи ⠀⠀⠀⠀– 13:35 - через рекурсию ⠀⠀⠀⠀– 22:56 - методом ⠀⠀⠀⠀⠀⠀⠀⠀динамического ⠀⠀⠀⠀⠀⠀⠀⠀программирования 	2025-04-11 12:02:18.014365	25	1
70	❗️ Этот вебинар даём в связке с первым вебинаром 🔗https://3.shkolkovo.online/lesson/26090  Повторение идеи программного решения -> представление в экселе -> код	2025-04-11 12:03:17.22596	26	1
71	❗️ Программирование отрезков и почему это плохо -1. Идея решения №15 программированием: флаг 2. Поразрядная конъюнкция руками. 	2025-04-11 12:04:24.073883	27	1
72	ТЕОРИИ В ВЕБЕ НЕТ Перед просмотром данного веба очень желательно просмотреть 4-ый веб из основ проги по спискам и строкам.  🔹Поиск среднеарифметического списка	2025-04-11 12:05:37.17921	28	1
73	Теория: [снова теории нет] 🔹29:47 - Условное форматирование 🔹1:06.00 - Фиксация ячеек 🔹Решение задания 22 в libreoffice	2025-04-11 12:08:17.393694	29	1
74	🔺Теория: 1. Как подключать модуль itertools. Разные способы 2. Prodeuct, permutations 3. Метод join()  📎На вебинаре в целом разбирались нестандартные идеи для решения задачи	2025-04-11 12:09:36.062908	32	1
75	🔺 Теория: 1. Подключение модуля turtle 2. Функции модуля turtle: up, down, done, fd, left, fight, tracer 3. Разница между пересечением и объединением.	2025-04-11 12:09:49.937396	32	1
76	основа принципа ручного решения	2025-04-11 12:11:28.595139	33	1
77	❗️ ВПР разбирается очень подробно, поэтому отправляем ребенка сюда, если проблемы с ВПР.	2025-04-11 12:12:14.233818	34	1
78	№ 18 - прогон по заданиям.  Решение методом динамического программирования в excel 🔹20:00 - применение специальной вставки  №22 - разбор условия задачи 🔹1:18:36 - Построение диаграммы Ганта	2025-04-11 12:13:17.215479	35	1
79	🔻Веб зеленый только из-за №10. Если ребенок умеет решать №10, этот веб можно пропускать.🔻	2025-04-11 12:14:27.498871	36	1
80	📍Замечание: В этом вебинаре просто нарешка заданий 1, 4 и 13 (теории по ним тут почти нет). БУ в вебинаре проговаривает, что обязательно необходимо смотреть предыдущий вебинар по этим заданиям!	2025-04-11 12:15:45.299672	36	1
81	Теория к № 5: 🔹5:03 - Как работают срезы? 🔹16:15 - метод zfill 🔹17:12 - Как сделать инверсию бит с помощью функции replace? 🔹30:24 - Как перевести число из 10с.с. в любую с.с. при помощи функции?	2025-04-11 12:16:11.870673	37	1
82	№2 и №8 - просто нарешка, без новой информации №13 - здесь прогой, но БУ говорит, что №13 нужно решать на бумаге (прога на всякий)  🔹Модуль itertools в №2 и №8 🔹Модуль ipaddress в №13 🔹25:50 - Методы join и split	2025-04-11 12:17:38.323064	38	1
83	13 прогой	2025-04-11 12:17:58.474521	38	1
84	❗️ Первый час вебинара: ручное решение, идея программного решения, код для решения задачи. Если ученик с первых двух вебов по решению задачи всё понял, то информативными будут только последние 30 минут вебинара и *стоит об этом сказать* Важное: 1. *2 кучи*  2. Задача с ограничением сверху (время: 1:16:09) 3. Кэширование	2025-04-11 12:18:58.16056	39	1
85	❗️ Повторение принципа решения 	2025-04-11 12:20:27.165331	40	1
86	В вебинаре повторение стандартных решений + разбор нестандартных. Теория: 🔹23:16 - Функция map	2025-04-11 12:21:40.898339	41	1
88	🔹0:25 - Обсуждение №25 с предыдущего вебинара	2025-04-11 12:22:56.664452	44	1
89	❗️ Поразрядная конъюнкция руками подробно	2025-04-11 12:23:52.069744	46	1
90	Задачи решаются сначала руками, потом прогой: вложенными циклами/ с itertools	2025-04-11 12:25:50.569192	47	1
91	Теории в вебе нет. Есть нестандартные и стандартные задачки, их нарешка.  🔹Из интересного: 1:15:10 - БУ показывает график зависимости % выполнения от каждого из заданий ЕГЭ по икт.	2025-04-11 12:27:03.319057	49	1
92	Теория: 🔹7:06 - Что такое адрес сети. Для чего нужна маска? subnet, net (просто адрес) и broadcast (широковещательный адрес) 🔹22:46 - Поразрядная конъюнкция. 🔹1:13:56 - применение zfill	2025-04-11 12:28:22.087656	50	1
93	Решения, представленные на вебинаре больше для того, чтобы в случае новой задачи по теории игр быть готовым её решить. При решении 19-21 БУ не рекомендует применять эти способы. ❗️ Чем заменить кэширование: будет полезно и для №16	2025-04-11 12:29:18.46982	51	1
94	🔹В вебе разбираются как базовые задания по №18, так и сложные прототипы. 🔹№22 разбирается с нуля 🔹Решение №22 через функцию ВПР 🔹1:39:35 - Диаграмма Ганта	2025-04-11 12:45:35.065885	53	1
95	📍Как будто бы этот веб самый информативный из всех вебов по №18,22. Хотя базовых заданий разбирается не так много. Можно делать его самым главным вебом по данным задачам.	2025-04-11 12:46:34.278252	53	1
96	Важный веб для понимания №12 (руками)	2025-04-11 12:48:19.406639	58	1
97	🔹13:43 - Что такое регулярные выражения? 🔹20:37 - Шаблоны 🔹49:47 - Группировки	2025-04-11 12:50:24.77307	60	1
98	Теория с нуля + задачи руками	2025-04-11 12:51:16.617677	62	1
99	Метод двух указателей	2025-04-11 12:51:50.828742	79	1
100	Метод 2х указателей	2025-04-11 12:52:16.495452	79	1
101	Задачи:  1. Демо 2025 2. ЕГЭ 2024 3. ЕГЭ 2023 4. Прототипы: базовые на изображения, ppi(dpi), кодирование звука передача файлов, сжатие изображения	2025-04-11 12:52:56.251072	152	1
102	омментарий: 📎 Здесь разбирается №8, который решается руками через системы счисления 📎 Все три способа решения: комбинаторика, вложенные циклы, itertools	2025-04-11 12:53:11.757766	153	1
103	Задания, которые разбираются на вебинаре - мостик между простыми заданиями первой части и реальными 26.	2025-04-11 12:55:00.986747	80	1
104	регулярки	2025-04-11 12:55:52.474328	60	1
105	солвер	2025-04-11 12:57:02.877394	77	1
106	тройная система	2025-04-13 09:33:55.040721	132	1
107	Смешарикам, которые только приступают к 26	2025-04-15 16:00:43.14444	80	1
108	lambda, map, filter + сортировка в массивах (в том числе и в двумерном) 	2025-04-15 16:01:22.06904	85	1
109	повторение lambda	2025-04-15 16:01:57.749293	88	1
110	просто закрепление	2025-04-15 16:02:22.807275	86	1
111	повторение простых заданий, но прогой	2025-04-15 16:02:36.068372	87	1
112	последняя задача – 23-я на кол-во различных значений	2025-04-16 10:10:07.323414	107	1
113	двойная система	2025-04-16 10:50:01.547477	128	1
114	треугольник с максимальным периметром в каждом кластере	2025-04-16 10:50:38.098003	129	1
115	двойная система, красный гигант, красный карлик	2025-04-16 10:51:23.639358	130	1
116	нейтронная звезда, черная дыра	2025-04-16 10:52:18.173347	131	1
117	три оси: x, y, z	2025-04-16 10:53:11.793133	133	1
118	три оси: x, y, z	2025-04-16 10:54:06.201729	134	1
119	Базовые задания №8 и задания №25 на делители.  Теория: 🔹5:30 - Модуль itertools 🔹6:35 - Что такое картежи? 🔹 24:31 - Небольшой практикум по срезам 🔹58:05 - ОТА (основная теорема арифметики) 🔹1:07:10 - Написание функции, которая определяет, что число простое	2025-04-20 17:57:49.750994	72	7
120	Теории практически нет. Нарешка задания №13 прогой. Стандартные задачи №17 и их нестандартные решения.	2025-04-20 18:04:41.850797	76	7
121	Теории в вебинаре нет.  🔹3:05 - ipaddress, функция ip_network 🔹25:43 - Как выглядит маска?	2025-04-20 18:07:16.576574	67	7
122	Одна стандартная задача + далее нестандартные решения	2025-04-20 18:09:47.333866	52	7
123	🔹Способы перебора и нахождения делителей числа. 🔹Задачи на маски: через срезы и перебор 🔹1:17:28 - Модуль fnmatch 🔹23:30 - множество set() 🔹24:35 - функция sorted()	2025-04-20 18:12:28.660933	30	7
125	Аналогичные задачи + задачки посложнее: 🔹Способы перебора и нахождения делителей числа. 🔹Задачи на маски: через срезы и перебор 🔹4:05 - множество set() 🔹5:40 - функция sorted() 🔹1:08:06 – решение через модуль fnmatch 🔹1:18:37 - построения ряда Фибоначчи в питоне	2025-04-20 18:19:53.886301	43	7
126	Альтернативные (сложные) решения задач. На экзамене не актуально, но для общего развития и тренировки полезно.	2025-04-20 18:23:40.980331	48	7
127	 🔹9:27 - Теория по делителям числа, делители полных квадратов  🔹30:39 - модуль fnmatch	2025-04-20 18:25:44.815372	56	7
128	•\tЗадание №14 с нуля. Теория: 🔹2:38 - Системы счисления 🔹5:55 - Примеры перевода чисел из 10с.с. и обратно РУКАМИ 🔹12:40 - Свойства систем счисления 🔹17:35 - Операции в разных системах счисления 🔹48:43 - hex-редактор 🔹1:01:58 - Быстрый перевод чисел	2025-04-20 18:30:39.595847	45	7
129	Вебы только для тех, кто уже хорошо программирует и нацелен на высокий балл.  🔹4:50 - подключение файла csv в питоне 🔹22:13 - функция any()	2025-04-20 18:33:29.530336	59	7
130	Теория по комбинаторике: 🔹4:10 - Размещения с повторениями 🔹7:40 - Размещения без повторений 🔹12:04 - Перестановки 🔹13:10 - Факториалы 🔹19:02 - Сочетания 🔹1:17:27 - Комбинаторика в теории вероятности Веб подойдет для тех, у кого проблемы с данным номером, и надо разобрать комбинаторику с нуля.	2025-04-20 18:40:24.700198	62	7
131	Теория: 🔹2:35 - Что такое рекурсия? 🔹8:25 - @lru_cache 🔹13:40 - модуль sys 🔹31:35 - Взаимная рекурсия	2025-04-20 18:42:26.621266	63	7
132	Теории в вебе нет. Нарешка уже пройденных заданий.	2025-04-20 18:48:02.672677	65	7
133	🔹№22: разбирается базовая задача и ‼️задача с полным решением через диаграмму Ганта‼️ 🔹№18: робот, ладья (в основном просто нарешка)	2025-04-20 18:53:46.322609	70	7
134	Разбор нестандартного подхода к решению задач №24	2025-04-20 18:57:09.335897	73	7
135	Просто нарешка задач: 🔹№16: Решение рекурсией и динамикой 🔹№23: Решение рекурсией	2025-04-20 19:01:13.106201	74	7
136	Нарешка базовых задач + интересные задачки. 🔹6:13 - Требования к тех.оснащению на ППЭ	2025-04-20 19:06:03.613729	75	7
137	метод двух указателей	2025-04-20 19:54:44.856562	168	7
138	Задача на разбивку чисел и нахождение НОД + маски 🔹7:57 - Что такое срезы? 🔹13:55 - алгоритм Евклида	2025-05-10 08:33:00.695942	31	7
139	Нарешка заданий №3 + пример №22‎ через диаграммы Ганта 🔹Прототип №3 про города, про инвестиционные счета 🔹№3: Функции ВПР, СЧЕТЕСЛИ, СЦЕПИТЬ	2025-05-10 18:49:46.693194	78	7
140	Нарешка электронных таблиц 🔹№3: инвестиционные счета‎, треки 🔹№18: робот, ладья	2025-05-10 18:52:23.074427	171	7
141	 \tНарешка задач №9,17 прогой по большей части для продвинутых деток (Генераторы списков)	2025-05-10 18:59:23.398056	173	7
142	Как базовые, так и сложные задачи, теория с нуля 🔹36:55 - построение диаграммы Ганта	2025-05-10 19:04:20.54261	174	7
143	🔹4:00 - ‎‎Регулярные выражения 🔹7:45 - Экранирование строк 🔹12:00 - функция finditer модуля re 🔹13:40 - Метод group 🔹1:09:43 - Функция eval	2025-05-10 19:14:03.135248	175	7
144	Продолжение решения стандартных задач через регулярные выражения‎ 🔹48:15 - Пример, когда регулярные выражения не всегда будут просто работать	2025-05-10 19:21:42.473765	179	7
146	Нарешка стандартных задачек 🔹28:20 - Бит прозрачности 🔹1:14:49 - Авторская задача БУ - решение прогой (расчет значения в питоне)	2025-05-10 19:30:40.407024	57	7
147	Нестандартные задачки №4 Теория по №4: 🔹20:43 - Алгоритм RLE (алгоритм кодирования длин серий) 🔹27:40 -Управляющие разряды 🔹38:10 - Алгоритм Хаффмана	2025-05-10 19:36:01.707704	68	7
148	Разбор задания №7 с нуля Теория: 🔹2:54 - Кодирование изображений (Что такое дискретно-квантованный сигнал, палитра цветов RGB, альфа-канал) 🔹1:13:51 - Кодирование звука (Что такое частота дискретизации)	2025-05-10 19:40:47.349805	69	7
149	Нарешка как базовых, так и непростых задач 🔹№7: Задачи на определение степени прозрачности	2025-05-10 19:44:18.784107	172	7
150	Нарешка стандартных заданий: ДЕЛ, отрезки, множества, поразрядная конъюнкция  Теория: 🔹3:25 - Закон преобразования импликации 🔹5:13 - Закон де Моргана 🔹6:20 - Метод сковородки 🔹56:30 - Поразрядная конъюнкция	2025-05-10 19:49:25.6299	61	7
151	 ‎Разбор задачек с нуля 🔹1 куча камней, 2 хода (руками) 🔹1 куча камней, 3 хода (руками и прогой) 🔹2 кучи камней, 2 хода (прогой)	2025-05-10 19:52:40.831657	64	7
152	Нарешка задач разного уровня: отрезки, множества, неравенства, поразрядная конъюнкция.	2025-05-10 19:54:51.707865	71	7
153	Нарешка задач разного уровня: пора‎зрядная конъюнкция, ДЕЛ, неравенства, отрезки 🔹20:43 - Поразрядная дизъюнкция	2025-05-10 19:57:49.05025	176	7
155	Веб больше для продвинутых деток, кто освоил все вебы по ТИ прогой до этого. 🔹‎25:30 - Суть неудачного хода	2025-05-10 20:00:18.173168	178	7
156	 Нарешка стандартных задач: 🔹Метод двух указателей и регулярные выражения	2025-05-10 20:02:38.55512	181	7
157	Решение стандартных задач нестандартными методами. 🔹13:58 - Словари 🔹15:22 - Функция zip	2025-05-10 20:04:57.704168	77	7
158	Нарешка стандартных задач двумя способами: руками и прогой	2025-05-10 20:19:48.671795	177	7
159	Нестандартные задачи и их разные способы решения: рекурсия, комбинаторика. 🔹Добавление списка в качестве аргумента.	2025-05-10 20:21:55.769399	182	7
162	🔹4:36 - Установка среды для программирования Ссылка на установку PyCharm Community: https://disk.yandex.ru/d/RlJAv-MrTmF_0g 	2025-07-06 11:38:42.301289	191	11
163	🔹5:52 - Типы языков программирования 	2025-07-06 11:38:56.353335	191	11
164	Теория:                                🔹13:24 - Что такое программа?                              🔹15:49 - Операторы                          🔹21:58 - Переменная                                             🔹27:33 - Оператор присваивания  	2025-07-06 11:39:40.095258	191	11
165	Настройка программ: 🔹31:30 - Запуск PyCharm 🔹33:00 - Запуск IDLE 🔹34:21 - Интерфейс PyCharm  	2025-07-06 11:40:07.364975	191	11
166	Работа в PyCharm: 🔹36:54 - Вывод данных 🔹39:12 - Моделирование мини-игры (применение базовых операторов) 🔹42:19 - Переменная-счетчик 🔹44:01 - Линейный алгоритм 🔹44:48 - Комментарии в коде	2025-07-06 11:40:11.529463	191	11
167	🔹46:18 - Ввод данных с клавиатуры input() 🔹49:19 - Типы данных, конкатенация строк 🔹51:03 - Функция int 🔹1:08:29 - Оператор условия 🔹1:16:03 - Отступы в ветвлении   	2025-07-06 11:42:35.988703	191	11
\.


--
-- Data for Name: webinar_oge_topic_association; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.webinar_oge_topic_association (webinar_id, oge_topic_id) FROM stdin;
230	1
231	1
232	1
233	1
234	2
235	2
236	2
237	2
238	2
239	3
240	2
241	3
242	3
243	6
244	3
245	3
246	6
247	3
248	6
249	6
250	6
251	6
252	6
253	6
254	6
258	1
259	1
\.


--
-- Data for Name: webinar_task; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.webinar_task (id, text, webinar_id, created_at, created_by_id) FROM stdin;
1	За один ход игрок может\r\nдобавить в кучу два камня или увеличить количество камней в куче в два раза.\r\nНапример, имея кучу из 15 камней, за один ход можно получить кучу из 17 или\r\n30 камней. У каждого игрока, чтобы делать ходы, есть неограниченное количество\r\nкамней. Игра завершается в тот момент, когда количество камней в куче становится\r\nне менее 25. Победителем считается игрок, сделавший последний ход, то есть первым\r\nполучивший кучу, в которой будет 25 или больше камней.\r\nВ начальный момент в куче было S камней, 1 ≤ S ≤ 24.\r\n1. При каких S: 1а) Петя выигрывает первым ходом; 1б) Ваня выигрывает первым ходом?\r\n2. Назовите три значения S, при которых Петя может выиграть своим вторым\r\nходом?\r\n3. При каком S Ваня выигрывает своим первым или вторым ходом?	20	2025-04-11 11:31:48.224544	1
2	За один ход игрок может добавить в кучу два камня, добавить в кучу три камня или увеличить\r\nколичество камней в куче в два раза. Например, имея кучу из 15 камней, за один\r\nход можно получить кучу из 17, 18 или 30 камней. У каждого игрока, чтобы делать\r\nходы, есть неограниченное количество камней. Игра завершается в тот момент, когда количество камней в куче становится не менее 30. Победителем считается игрок,\r\nсделавший последний ход, то есть первым получивший кучу, в которой будет 30 или\r\nбольше камней. В начальный момент в куче было S камней, 1 ≤ S ≤ 29.\r\n1. При каких S: 1a) Петя выигрывает первым ходом; 1б) Ваня выигрывает первым ходом?\r\n2. Назовите четыре значения S, при которых Петя может выиграть своим вторым\r\nходом.\r\n3. Назовите два значения S, при которых Ваня выигрывает своим первым или\r\nвторым ходом.	20	2025-04-11 11:31:56.208554	1
3	За один ход игрок\r\nможет\r\na) добавить в одну из куч (по своему выбору) один камень или\r\nб) увеличить количество камней в куче в два раза.\r\nПобедителем считается игрок, сделавший последний ход, т.е. первым получивший\r\nтакую позицию, что в обеих кучах всего будет 38 камней или больше.\r\nЗадание 1. Для каждой из начальных позиций (7, 15),(9, 14) укажите, кто из\r\nигроков имеет выигрышную стратегию.\r\nЗадание 2. Для каждой из начальных позиций (7, 14),(8, 14),(9, 13) укажите, кто\r\nиз игроков имеет выигрышную стратегию.\r\nЗадание 3. Для начальной позиции (8, 13) укажите, кто из игроков имеет выигрышную стратегию.\r\nПостройте дерево всех партий, возможных при указанной выигрышной стратегии.	20	2025-04-11 11:32:08.558075	1
4	За один ход игрок может\r\na) добавить в любую кучу два камня;\r\nб) увеличить количество камней в любой куче в два раза.\r\nИгра завершается в тот момент, когда суммарное количество камней в двух кучах\r\nстановится не менее 75. Победителем считается игрок, сделавший последний ход,\r\nт.е. первым получивший такую позицию, при которой в кучах будет 75 камней или\r\nбольше. В начальный момент в первой куче было 9 камней, а во второй – S камней,\r\n1 ≤ S ≤ 65.\r\nЗадание 1. а) При каких значениях числа S Петя может выиграть в один ход?\r\nУкажите все такие значения и соответствующие ходы Пети.\r\nб) Известно, что Ваня выиграл своим первым ходом после неудачного первого\r\nхода Пети. Укажите минимальное значение S, когда такая ситуация возможна	20	2025-04-11 11:32:16.039731	1
5	Два игрока, Петя и Ваня, играют в игру. Перед игроками лежит две кучи камней.\r\nИгроки ходят по очереди, первый ход делает Петя. За один ход игрок может\r\na) добавить в любую кучу два камня;\r\nб) увеличить количество камней в любой куче в два раза.\r\nИгра завершается в тот момент, когда суммарное количество камней в двух кучах\r\nстановится не менее 75. Победителем считается игрок, сделавший последний ход,\r\nт.е. первым получивший такую позицию, при которой в кучах будет 75 камней или\r\nбольше. В начальный момент в первой куче было 9 камней, а во второй – S камней,\r\n1 ≤ S ≤ 65.\r\nЗадание 1. а) При каких значениях числа S Петя может выиграть в один ход?\r\nУкажите все такие значения и соответствующие ходы Пети.\r\nб) Известно, что Ваня выиграл своим первым ходом после неудачного первого\r\nхода Пети. Укажите минимальное значение S, когда такая ситуация возможна.	20	2025-04-11 11:32:22.324038	1
6	Определить объем памяти для хранения изображения размером m*n с палитрой из К цветов.	11	2025-04-11 11:34:33.630796	1
7	Изображение размером m*n занимает в памяти I Кбайт. Определить количество цветов в палитре	11	2025-04-11 11:34:39.176236	1
8	Документы сканируются с разрешением dpi и палитрой из K цветов, размер документа - I Мбайт. Затем изменили параметры сканирования. Определить объем изображения с измененными параметрами.	11	2025-04-11 11:34:44.907717	1
564	№7. Определить количество цветов в палитре без учета степени прозрачности.	172	2025-05-10 19:44:52.952413	7
9	Для хранения изображения размером m*n отведено I Кбайт. При кодировании используется i бит для определения степени прозрачности. Определить количество цветов в палитре.	11	2025-04-11 11:34:51.539013	1
10	Файл с двухканальной звукозаписью с частотой дискретизации f кГц и i-битным разрешением занимает в памяти I Мбайт. Определить длительность записи\r\nОдноканальная звукозапись, частота дискретизации f Гц и i уровней дискретизации, длительность звукового файла t минут. Определить объем файла.	12	2025-04-11 11:36:31.955623	1
11	Звуковой файл был передан в город А за t1 с. Затем его оцифровали и передали в Б. Пропускная способность канала связи с Б в 3 раза ниже. Определить время передачи файла в город Б	12	2025-04-11 11:36:36.795286	1
12	В системе хранятся пароли пользователей. Определить объем памяти, необходимый для хранения К паролей\r\n	12	2025-04-11 11:36:41.422392	1
13	В системе хранятся пароли пользователей и доп сведения. Определить объем памяти, необходимый для хранения данных об N пользователях.	12	2025-04-11 11:36:46.266392	1
14	В системе хранятся пароли пользователей и доп сведения. Определить объем памяти, необходимый для хранения доп сведений об одном пользователе.	12	2025-04-11 11:36:50.752161	1
15	Определить максимальное количество пользователей, чьи данные можно сохранить при I байт памяти.	12	2025-04-11 11:36:58.157549	1
16	Составляются 6-буквенные слова, из букв КРОТ. Буква О используется в каждом слове ровно 1/2/3 раза. Сколько слов можно составить?	13	2025-04-11 11:38:13.601617	1
17	Составляются 6-буквенные слова, из букв КРОТ. Буквы О и У можно использовать ровно по 1 разу.  Сколько слов можно составить?	13	2025-04-11 11:38:18.461544	1
18	Составляются 4-буквенные слова из букв ЛЕТО. Буква Е используется в каждом слове хотя бы 1 раз. Сколько слов может быть составлено?	13	2025-04-11 11:38:22.80217	1
19	Составляются 5-буквенные слова из букв МУХА, буква может использовать не более 3 раз. Сколько существует таких слов, которые можно написать?	13	2025-04-11 11:38:28.347277	1
20	Составляются 5-буквенные слова из букв СЛОН. Буква О используется, но не более трёх раз. 	13	2025-04-11 11:38:33.22898	1
21	Составляются слова перестановкой букв слова АДЖИКА, избегая слов с двумя подряд одинаковыми буквами. 	13	2025-04-11 11:38:37.098465	1
22	Сколько существует чисел, делящихся на 5, десятичная запись которых содержит 6 цифр, причем все цифры различны и никакие две четные и две четные цифры не стоят рядом.	13	2025-04-11 11:38:41.418882	1
23	В колоде 36 карт. Какова вероятность того, если вытащить две карты из колоды, то эту будут две черные дамы?	13	2025-04-11 11:38:46.7583	1
24	В колоде 36 карта. Какова вероятность того, что если вытащить 6 карта из колоды, то это будут 6 козырей?	13	2025-04-11 11:38:51.68036	1
25	Монету подбросили 10 раз. Сколькими способами может выпасть орел?	13	2025-04-11 11:38:56.847997	1
26	(Демо-2022) Откройте файла электронной таблицы, содержащий в каждой строке три натуральных числа. Выясните, какое количество троек чисел может являться сторонами треугольника, то есть удовлетворяет неравенству треугольника. 	14	2025-04-11 11:39:53.433187	1
27	В файле электронной таблицы в каждой строке записаны 6 натуральных чисел. Определите количество строк таблицы, для которых выполнены оба условия:\r\n1. В строке есть как повторяющиеся, так и неповторяющиеся числа;\r\n2. Среднее арифметическое всех неповторяющихся чисел строки больше, чем среднее арифметическое всех повторяющихся чисел этой строки.\r\nПри вычислении средних значений каждое число учитывается столько раз, сколько оно встречается в строке. 	14	2025-04-11 11:39:58.916986	1
28	(Демо-2025) В файле электронной таблицы в каждой строке записаны шесть натуральных чисел. Определите количество строк таблицы, содержащих числа, для которых выполнены оба условия:\r\n1. В строке только одно число повторяется трижды, остальные числа различны;\r\n2. Квадрат суммы всех повторяющихся чисел строки больше квадрата суммы всех её неповторяющихся чисел. В ответе запишите только число.	14	2025-04-11 11:40:07.922402	1
29	Вася составляет 6-буквенные слова, в которых есть только буквы КРОТ, причем буква О используется в каждом слове ровно 1 раз. Каждая из других допустимых букв может встречаться в слове любое количество раз или не встречаться совсем. 	15	2025-04-11 11:41:33.084726	1
30	Вася составляет 6-буквенные слова из букв ШАНЕЛЬ. Каждую букву нужно использовать ровно 1 раз, при этом код не может начинаться с буквы Ь и не может содержать сочетания ЕАЬ.	15	2025-04-11 11:41:38.969831	1
31	Сколько существует чисел, восьмеричная запись которых содержит 6 цифр, причем все цифры различны и никакие две четные и две нечетные цифры не стоят рядом.	15	2025-04-11 11:41:43.412461	1
32	Рассматриваются числа, восьмеричная запись которых содержит ровно 12 знаков. Определите количество таких чисел, в восьмеричной записи которых ровно пять нечетных цифр, причем никакие две нечетные цифры не стоят рядом. 	15	2025-04-11 11:41:49.011009	1
33	Все 5-буквенные слова, составленные из букв АКРУ, записаны в алфавитном порядке. Укажите номер первого слова, которое начинается с буквы К.	15	2025-04-11 11:41:56.208106	1
34	Маша составляет коды из букв, входящих в слово МОДЕСТ. Каждая буква должна входить в код ровно один раз. Всевозможные коды Маша записывает в алфавитном порядке и нумерует. Какой код будет записан под номером 377	15	2025-04-11 11:42:01.383054	1
35	Все пятибуквенные слова, составленные из букв ФОКУС записаны в алфавитном порядке и пронумерованы. Под каким номеров в списке идет последнее слово, которое не содержит букв Ф и содержит ровно две буквы У?	15	2025-04-11 11:42:06.770419	1
36	Используя информацию из приведенной базы данных, определите на сколько увеличилось количество упаковок яиц диетических, имеющихся  наличии в магазинных Заречного района, за период с 1 по 10 июня включительно. В ответе запишите только число.	16	2025-04-11 11:43:18.508876	1
37	Используя информацию из базы данных в файле определите общую массу (в кг) всех видов зефира, полученных магазинами, расположенными на проспекте Революции, за период со 2 по 10 августа.	16	2025-04-11 11:43:23.018824	1
38	Используя информацию из базы данных в файле определите среднее значение населения стран, у которых в столице проживает более 100000 человек, но не более 500000	16	2025-04-11 11:43:30.379443	1
39	Используя информацию из базы данных в файле, определите среднее население городов, расположенных в странах, население столицы которых превышает 1 000 000 человека одним из официальных языков является английский. В ответ запишите только целую часть числа.	16	2025-04-11 11:43:36.525702	1
40	Используя информацию из приведенной базы данных, определите разницу между суммой на счете с максимальным суммарным поступлениями и суммой на счете с минимальным суммарным поступлением за указанный период. Сумму поступлений следует вычислять в рублях, считая, что обмен валюты производится в момент поступления. В ответе укажите только целую часть полученного значения. 	16	2025-04-11 11:43:43.51205	1
41	Используя информацию из базы данных в файле, определите суммарный бюджет в миллионах долларов всех фильмов в жанре Триллер, снятых режиссерами из Великобритании в период с 2000 года по 2012 год? В ответ запишите только целую часть числа. 	16	2025-04-11 11:43:48.398631	1
42	Используя информацию из базы данных в файле, определите долю окупившихся фильмов в процентах среди всех фильмов режиссера Мартина Скорсезе. 	16	2025-04-11 11:43:53.314743	1
43	Используя информацию из базы данных, определите количество городов с населением не менее 100 000 человек, которые являются столицами стран, в которых распространены несколько языков с процентом более 10 каждый.	16	2025-04-11 11:43:58.511425	1
44	Для какого наибольшего натурального числа А формула (¬ДЕЛ(x, A) ∧ ДЕЛ(x, 6)) → ¬ДЕЛ(x, 4) тождественно истинна?	18	2025-04-11 11:54:07.417443	1
45	На числовой прямой даны два отрезка: P = [3, 13] и Q = [7, 17]. Выберите такой отрезок А, что формула ((x ∈ A) → (x ∈ P)) ∨ ¬(x ∈ Q) тождественно истинна, то есть принимает значение 1 при любом значении переменной х	18	2025-04-11 11:54:12.296601	1
46	На числовой прямой даны два отрезка: P = [10, 20] и Q = [15, 25]. Выберите такой\r\nотрезок A, что формула ((x ∈ P) → (x ∈ Q)) ∨ (x ∈ A) тождественно истинна при любом значении х?	18	2025-04-11 11:54:17.253663	1
47	На числовой прямой даны два отрезка: P = [8, 39] и Q = [23, 58]. Выберите из\r\nпредложенных вариантов такой отрезок A, что логическое выражение\r\n((x ∈ P) ∧ (x ∈ A)) → ((x ∈ Q) ∧ (x ∈ A))\r\nтождественно истинно при любом значении x.	18	2025-04-11 11:54:21.185989	1
48	Элементами множества A являются натуральные числа. Известно, что выражение\r\n¬(x ∈ {2, 4, 6, 8, 10, 12}) ∨ (¬(x ∈ {3, 6, 9, 12, 15}) → (x ∈ A))\r\nистинно (т. е. принимает значение 1) при любом значении переменной x. Определите\r\nнаименьшее возможное значение произведения элементов множества А.	18	2025-04-11 11:54:26.625325	1
74	Определить максимальное количество идущих подряд троек символов ZXY или ZYX. \r\n🔹этот пример можно решить методом замены через replace, однако в вебинаре рассматривается решение методом прохода по строке	23	2025-04-11 12:00:20.014661	1
49	Элементами множеств A, и Q являются натуральные числа, причём\r\nP = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20} и Q = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30}. Известно, что выражение\r\n((x ∈ A) → ¬(x ∈ P)) ∧ (¬(x ∈ Q) → ¬(x ∈ A))\r\nистинно (т. е. принимает значение 1) при любом значении переменной x. Определите\r\nнаибольшее возможное количество элементов множества A.	18	2025-04-11 11:54:33.905579	1
50	Известно, что для некоторого отрезка A формула\r\n((x ∈ A) → (x\r\n2 ≤ 100)) ∧ ((x\r\n2 ≤ 16) → (x ∈ A))\r\nтождественно истинна (то есть принимает значение 1 при всех вещественных значениях переменной x). Какую наибольшую длину может иметь отрезок A?	18	2025-04-11 11:54:38.427383	1
51	Сколько существует целых значений A, при которых формула\r\n((x ≥ 15) → (x · x > A)) ∧ ((y · y ≥ A) → (y > 11))\r\nтождественно истинна (то есть принимает значение 1 при любых целых неотрицательных значениях переменных x и y)?	18	2025-04-11 11:54:43.248661	1
52	Укажите наименьшее целое значение A, при котором выражение\r\n(y + 3x < A) ∨ (x > 20) ∨ (y > 40)\r\nистинно для любых целых положительных значений x и y.	18	2025-04-11 11:54:48.05519	1
53	Укажите наименьшее целое значение A, при котором выражение\r\n(x ≥ 10) ∨ (x < y) ∨ (x · y < A)\r\nистинно для любых целых положительных значений x и y.	18	2025-04-11 11:54:53.503682	1
54	Дана таблица истинности логической функции F. Определить, какому столбцу таблицы соответствует каждая из переменных выражения.\r\n🔹Решение руками	21	2025-04-11 11:56:10.402191	1
55	Дана таблица истинности логической функции F. Определить, какому столбцу таблицы соответствует каждая из переменных выражения.\r\n🔹Решение руками	21	2025-04-11 11:56:14.295523	1
56	Дана таблица истинности логической функции F. Определить, какому столбцу таблицы соответствует каждая из переменных выражения.\r\n🔹Решение прогой	21	2025-04-11 11:56:17.92111	1
57	Дана таблица истинности логической функции F. Определить, какому столбцу таблицы соответствует каждая из переменных выражения.	21	2025-04-11 11:56:24.257876	1
58	Алгоритм строит по входному числу N новое - R: строится троичная запись N; дописываются разряды по правилу. Определить максимальное N, после обработки которого получается R<199.\r\n	21	2025-04-11 11:56:28.831263	1
59	Алгоритм строит по входному числу N новое - R: строится двоичная запись N; дописываются и убираются разряды по правилу. Определить количество N, при обработке которых получается R=58.	21	2025-04-11 11:56:33.602417	1
60	Значение выражения записали в 6 с.с. Определить наименьшее х, при котором количество нулей в значении выражения, записанного в 6 с.с. равно 202. 	21	2025-04-11 11:56:38.126085	1
61	Операнды выражения записаны в 130 с.с. Определить наименьшее х, при котором значение выражения кратно 23.	21	2025-04-11 11:56:41.385144	1
62	Найти кратчайший путь из пункта Б в пункт Ж. 	22	2025-04-11 11:57:54.724473	1
63	Определить, какие номера населённых пунктов в таблице могут соответствовать населённым пунктам Б и Е на схеме.	22	2025-04-11 11:57:59.224971	1
64	🔻Повышенный уровень сложности: симметричная схема. \r\nОпределите длину кратчайшего пути между пунктами Ж и Г.\r\n	22	2025-04-11 11:58:03.57746	1
65	Указать кратчайшее возможное кодовое слово для буквы З, при котором код будет допускать однозначное декодирование.	22	2025-04-11 11:58:06.903809	1
66	Укажите кратчайшее возможное кодовое слово для буквы Ж, при котором код будет допускать однозначное декодирование.	22	2025-04-11 11:58:10.093643	1
67	🔻Повышенный уровень сложности: в ЕГЭ такого еще не было, но появление на экзамене вполне возможно. \r\n🔹Решение с помощью Алгоритма Хаффмана.\r\n\r\nВ сообщении встречается 50 букв А, 30 букв Б, 20 букв В и 5 букв Г. При его передаче использован неравномерный двоичный префиксный код, который позволил получить минимальную длину закодированного сообщения. Какова она в битах?	22	2025-04-11 11:58:17.053515	1
68	Та же задача, но немного усложняем условие: увеличиваем алфавит.	22	2025-04-11 11:58:21.618872	1
69	По заданным IP-адресу и адресу сети определить третий слева байт маски.	22	2025-04-11 11:58:27.160138	1
70	Для скольких значений маски возможны заданные IP-адрес и адрес сети?	22	2025-04-11 11:58:31.04931	1
71	Два узла, находящиеся в разных подсетях, имеют заданные IP-адреса. Определить наибольшее количество единиц в масках этих подсетей. 	22	2025-04-11 11:58:34.067364	1
72	В заданной сети определить количество IP-адресов, для которых сумма единиц в двоичной записи не кратна 2.	22	2025-04-11 11:59:44.627109	1
73	Определить длину самой длинной подцепочки, состоящей из одинаковых символов.\r\n	23	2025-04-11 12:00:14.855398	1
173	Определить минимальное число N, при обработке получается R=516.	44	2025-04-11 12:23:18.060675	1
75	Определить максимальное количество идущих подряд троек символов АВС, ВАС, САВ, СВА, стоящих одна за другой и пересекающихся с соседними тройками одной буквой.\r\n🔹Решение методом прохода по строке	23	2025-04-11 12:00:24.160633	1
76	🔻Повышенный уровень сложности:\r\nОпределить максимальную длину подстроки, в которой символ Y встречается не более 150 раз. \r\n🔹Решение через split\r\n\r\n🔹Как работает функция map	23	2025-04-11 12:00:29.472638	1
77	Определить значение заданного выражения.\r\n🔹Решение через eval\r\n🔹Решение через replace и split\r\n🔹Решение методом прохода по строке	23	2025-04-11 12:00:34.071375	1
78	Определить максимальную длину подстроки, которая может являться частью числа в 16 с.с. \r\n🔹Решение методом прохода по строке	23	2025-04-11 12:00:39.842532	1
79	Значение выражения записали в 2 с.с. Определить количество 1 и 0 в этой записи.	24	2025-04-11 12:01:13.475668	1
80	Значение выражения записали в 5 с.с. Определить количество 4 в этой записи.	24	2025-04-11 12:01:17.133496	1
81	Значение выражения записали в 6 с.с. Определить количество 5 в этой записи.\r\n	24	2025-04-11 12:01:21.396198	1
82	Значение выражения записали в 5 с.с. Определить количество 4 в этой записи.\r\n	24	2025-04-11 12:01:25.628526	1
83	В саду 100 деревьев: 14 яблонь и 42 груши. Определить основание с.с., в которой указаны числа.	24	2025-04-11 12:01:30.414874	1
84	Определить основания с.с., в которых запись числа 23 оканчивается на 1.	24	2025-04-11 12:01:34.425455	1
85	В с.с. с некоторым основанием десятичное число 83 записывается как 123. Определить основание с.с.	24	2025-04-11 12:01:39.523001	1
86	В некоторой с.с. записи десятичных чисел 41 и 63 заканчиваются на 8. Определить основание с.с.	24	2025-04-11 12:01:44.284734	1
87	Алгоритм вычисления функции F(n) задан соотношениями. Определить значение F(19).\r\n🔹Решение рекурсией и динамикой	25	2025-04-11 12:02:29.200828	1
88	Алгоритм вычисления функции F(n) задан соотношениями. Определить значение F(2023)/F(2020).\r\n🔹Решение руками\r\n	25	2025-04-11 12:02:32.199748	1
89	Алгоритм вычисления функций F(n) и G(n) задан соотношениями. Определить значение F(14)+G(14).\r\n🔹Решение рекурсией и динамикой	25	2025-04-11 12:02:36.102727	1
90	У исполнителя имеются две команды. Определить количество программ, преобразующих число 1 в 8.\r\n🔹Решение рекурсией	25	2025-04-11 12:02:39.663658	1
91	У исполнителя имеются три команды. Определить количество программ, преобразующих число 2 в 60, траектория вычислений которых содержит 16 и не содержит 21.\r\n🔹Решение рекурсией	25	2025-04-11 12:02:43.933693	1
92	У исполнителя имеются три команды. Определить количество программ, преобразующих число 2 в 51, траектория вычислений которых содержит 18 и не содержит 33. Также программа не содержит двух команд №3 подряд.\r\n🔹Решение рекурсией	25	2025-04-11 12:02:48.445797	1
93	У исполнителя имеются три команды. Определить количество программ, преобразующих число 2 в 20 и не содержащих двух команд №2 подряд.\r\n🔹Решение рекурсией	25	2025-04-11 12:02:52.055062	1
94	За один ход игрок может\r\nдобавить в кучу четыре камня или увеличить количество камней в куче в три раза.\r\nНапример, имея кучу из 10 камней, за один ход можно получить кучу из 14 или\r\n30 камней. У каждого игрока, чтобы делать ходы, есть неограниченное количество\r\nкамней. Игра завершается в тот момент, когда количество камней в куче становится\r\nне менее 70. Победителем считается игрок, сделавший последний ход, то есть первым\r\nполучивший кучу, в которой будет 70 или больше камней.\r\nВ начальный момент в куче было S камней, 1 ≤ S ≤ 69.\r\n1. При каких S: 1а) Петя выигрывает первым ходом; 1б) Ваня выигрывает первым ходом?\r\n2. Назовите два значения S, при которых Петя может выиграть своим вторым\r\nходом.\r\n3. При каком S Ваня выигрывает своим первым или вторым ходом?	26	2025-04-11 12:03:29.902077	1
95	Обозначим через ДЕЛ(n, m) утверждение «натуральное число n делится без\r\nостатка на натуральное число m». Для какого наибольшего натурального числа A\r\nформула\r\n(¬ДЕЛ(x, A) ∧ ДЕЛ(x, 6)) → ¬ДЕЛ(x, 4)\r\nтождественно истинна?	27	2025-04-11 12:04:37.07733	1
96	Обозначим через ДЕЛ(n, m) утверждение «натуральное число n делится без\r\nостатка на натуральное число m». Для какого наибольшего натурального числа A\r\nформула\r\nДЕЛ(x, A) → (ДЕЛ(x, A) → ДЕЛ(x, 34) ∧ ДЕЛ(x, 51))\r\nтождественно истинна?	27	2025-04-11 12:04:41.049891	1
97	Определите наименьшее натуральное число A, такое что выражение\r\n(X&56 6= 0) → ((X&48 = 0) → (X&A 6= 0))\r\nтождественно истинно (то есть принимает значение 1 при любом натуральном значении переменной X)?	27	2025-04-11 12:04:45.669442	1
174	Сколько значений R может получиться на заданном отрезке в результате работы автомата?	44	2025-04-11 12:23:22.534755	1
98	Укажите наименьшее целое значение A, при котором выражение\r\n(2y + 5x < A) ∨ (2x + 4y > 100) ∨ (3x − 2y > 70)\r\nистинно для любых целых положительных значений x и y.	27	2025-04-11 12:04:50.843194	1
99	На числовой прямой даны два отрезка: P = [43; 49] и Q = [44; 53]. Укажите\r\nнаибольшую возможную длину такого отрезка A, что формула\r\n((x ∈ A) → (x ∈ P)) ∨ (x ∈ Q)\r\nтождественно истинна, то есть принимает значение 1 при любом значении переменной x.	27	2025-04-11 12:04:55.628284	1
100	Определить количество пар, в которых один элемент меньше, чем среднее арифметическое всех чисел, а второй больше, чем среднее арифметическое всех чисел.\r\n🔹Решение двумя способами	28	2025-04-11 12:05:48.46371	1
101	Определить количество пар, в которых хотя бы один элемент меньше, чем среднее арифметическое всех чисел, и десятичная запись хотя бы одного элемента содержит цифру 7.\r\n🔹Решение двумя способами	28	2025-04-11 12:05:51.914679	1
102	Определить количество троек, в которых хотя бы один элемент больше, чем среднее арифметическое всех чисел.	28	2025-04-11 12:05:55.187482	1
103	Определить количество троек, в которых хотя бы один элемент меньше, чем среднее арифметическое всех чисел, и десятичная запись хотя бы двух элементов оканчивается на 4.\r\n	28	2025-04-11 12:05:58.445607	1
104	Определить количество пар, в которых хотя бы один элемент больше, чем наибольшее из всех чисел, делящихся на 19.	28	2025-04-11 12:06:02.395428	1
105	Определить количество пар, в которых хотя бы один элемент больше, чем наибольшее из всех чисел, делящихся на 107, и в семеричной записи хотя бы одного элемента содержится сочетание 36.\r\n	28	2025-04-11 12:06:06.691464	1
106	Определить количество пар, в которых оба элемента больше, чем сумма цифр всех чисел, делящихся на 37.\r\n🔹Решение в одну строку	28	2025-04-11 12:06:10.681492	1
107	Выбрать несколько подряд идущих чисел так, чтобы каждое следующее число отличалось от предыдущего не более чем на 8. Определить максимальную сумму выбранных чисел.	29	2025-04-11 12:08:34.544762	1
108	Определить максимальную и минимальную денежную сумму, которую может собрать робот.	29	2025-04-11 12:08:39.715192	1
109	Робот двигается по квадрату со стенами. Определить максимальную и минимальную денежную сумму, которую может собрать робот.	29	2025-04-11 12:08:48.049837	1
110	Определить максимально возможный уровень заряда батареи самокатика в конечной точке, если пассажиру: 1. запрещено спешиваться; 2. разрешено спешиваться.	29	2025-04-11 12:08:57.416484	1
111	Определить максимальную и минимальную сумму чисел в клетках, в которых может остановиться ладья.	29	2025-04-11 12:09:03.945991	1
112	Определить минимальное время, черед которое завершится выполнение всей совокупности процессов.\r\n🔹Решение в libreoffice	29	2025-04-11 12:09:08.4447	1
113	Сколько существует различных символьных последовательностей длины 5 в трехбуквенном алфавите КОТ, которые содержат ровно две буквы О?	32	2025-04-11 12:10:00.537478	1
114	Вася составляет слова из букв слова ВЕРЕТЕНО. Код должен состоять из 8 букв и каждая буква в нём должна встречаться столько же раз, сколько в заданном слове. Кроме того, в коде не должны стоять рядом две гласные и две согласные буквы. Сколько различных слов может составить Вася?	32	2025-04-11 12:10:06.197176	1
115	Сколько различных слов длины 5, начинающихся с согласной буквы и заканчивающихся гласной буквой, можно составить из букв КУМА? Каждая буква может входить с слово несколько раз. Слова не обязательно должны быть осмысленными.	32	2025-04-11 12:10:11.059726	1
116	(Демо-2025) Определите количество 12-ричных пятизначных чисел, в записи которых ровно одна цифра 7 и не более трех цифр с числовым значением, превышающим 8. 	32	2025-04-11 12:10:17.942748	1
117	(ЕГЭ-2024) Сколько существует чисел, девятеричная запись которых состоит из пяти цифр, содержит ровно один ноль, причем ни одна нечетная цифра не стоит рядом с нулем?	32	2025-04-11 12:10:23.126935	1
118	Ася составляет 7-буквенные слова из букв АПЕЛЬСИН. Буква Ь, если встречается, стоит между двумя согласными. Сколько таких слов составит Ася?	32	2025-04-11 12:10:27.448026	1
119	Алгоритм:\r\nПовтори 2 [Вперед 5 Направо 90 Вперед 9 Направо 90]\r\nПоднять хвост\r\nВперед 2 Направо 90 Вперед 4 Налево 90\r\nОпустить хвост\r\nПовтори 2 [Вперед 4 Направо 90 Вперед 9 Направо 90]\r\nВыполняя этот алгоритм, Черепаха рисует одну за другой две фигуры. Определите сколько точек с целочисленными координатами будут находиться внутри области, полученной при объединении двух фигур. Точки на границах указанной области следует учитывать.	32	2025-04-11 12:11:03.478391	1
561	Определить длительность звукозаписи.	69	2025-05-10 19:42:06.33468	7
120	Используя информацию из базы данных в файле, определите на сколько увеличилось количество упаковок кефира всех сортов, имеющихся в наличии в магазинах Первомайского района с период с 1 по 5 июня включительно. 	34	2025-04-11 12:12:27.236464	1
121	Используя информацию из базы данных в файле, определите количество городов, расположенных в странах, расположенных в странах с населением более 100 000 000. 	34	2025-04-11 12:12:31.785506	1
122	Используя информацию из базы данных в файле, определите страну с максимальной площадью стран Азии, в которой имеется официальный язык, который использует более 70% населения. В ответ запишите название страны всеми заглавными буквами.	34	2025-04-11 12:12:35.956723	1
123	(ЕГЭ-2024) В файле электронной таблицы в каждой строке записаны четыре натуральных числа. Определите количество строк таблицы, в которых все числа различны, и при этом сумма наибольшего и наименьшего чисел больше суммы двух оставшихся. В ответе запишите только число. 	34	2025-04-11 12:12:41.075912	1
124	В файле электронной таблицы в каждой строке записаны 6 натуральных чисел. Определите количество строк таблицы, в которых выполнены оба условия:\r\n- в строке есть как повторяющиеся, так и неповторяющиеся числа;\r\n- среднее арифметическое всех неповторяющихся чисел строки больше, чем среднее арифметическое всех повторяющихся чисел этой строки. \r\nПри вычислении средних значений каждое число учитывается столько раз, сколько раз оно встречается в строке. 	34	2025-04-11 12:12:45.479887	1
125	(ЕГЭ-2023) В файле электронной таблицы в каждой строке содержатся четыре натуральных числа. Определите количество строк таблицы, содержащих числа, для которых выполнены оба условия:\r\n- наибольшее из четырех чисел меньше суммы трех других;\r\n- четыре числа можно разбить на две пары чисел с равными суммами.	34	2025-04-11 12:12:49.969629	1
126	(ЕГЭ-2024) В файле электронной таблицы в каждой строке записаны шесть натуральных чисел. Определите количество строк таблицы, для которых выполнены оба условия:\r\n- в строке только одно число повторяется трижды, остальные числа различны;\r\n- квадрат суммы повторяющихся чисел строки больше квадрата суммы всех её повторяющихся чисел.	34	2025-04-11 12:12:54.67245	1
127	Исполнитель робот двигается по полю. Определить максимальную и минимальную сумму, которую может собрать робот.\r\n🔹Решение в excel: метод динамического программирования	35	2025-04-11 12:13:34.185516	1
128	Робот двигается по полю с внутренними стенами. Определить максимальную и минимальную сумму, которую может собрать робот.\r\n🔹Решение в excel: метод динамического программирования	35	2025-04-11 12:13:38.552822	1
129	Робот двигается по полю и берет монеты с тех клеток, где количество монет четно. Определить максимальную и минимальную сумму, которую может собрать робот.\r\n🔹Решение в excel: метод динамического программирования\r\n	35	2025-04-11 12:13:42.204672	1
130	Ладья двигается по квадрату. Определить максимальную и минимальную сумму чисел в клетках, в которых может остановиться ладья.\r\n🔹Как двигается ладья?\r\n🔹Решение в excel: метод динамического программирования\r\n🔹48:50 - Фиксация столбцов/строк	35	2025-04-11 12:13:50.744901	1
131	Змейка перемещается по квадрату. Определить максимальное и минимальное значение змейки в конце ее маршрута.\r\n🔹Решение в excel	35	2025-04-11 12:13:55.030648	1
132	Определить максимальную продолжительность отрезка времени, в течение которого возможно одновременное выполнение четырех процессов.\r\n🔹Решение в excel\r\n🔹1:18:36 - Построение диаграммы Ганта	35	2025-04-11 12:14:01.781109	1
133	Определить длину кратчайшего пути между пунктами Е и Л.	36	2025-04-11 12:14:39.01173	1
134	Определить сумму протяженностей дорог из пункта D в G и из пункта А в С.	36	2025-04-11 12:14:42.573125	1
135	Определить сумму протяженностей дорог из пункта С в G и из пункта G в Н.	36	2025-04-11 12:14:45.73709	1
136	Условие Фано. Даны коды для некоторых букв. Определить кратчайший код для буквы Ж.	36	2025-04-11 12:14:56.533487	1
137	Условие Фано. Даны коды для некоторых букв. Определить количество знаков, необходимых для кодирования слова КАСАТКА.\r\n🔹Алгоритм Хаффмана\r\n🔹Где используется алгоритм Хаффмана?	36	2025-04-11 12:15:04.29556	1
138	Определить, сколько раз встречается сочетание букв «все» в составе других слов.	36	2025-04-11 12:15:09.499562	1
139	Для заданных IP-адреса и адреса сети определить третий слева байт маски.\r\n	36	2025-04-11 12:15:14.026814	1
175	Определить минимальное число R>133, которое может получиться.	44	2025-04-11 12:23:28.841296	1
636	Найти площадь прямоугольного треугольника	191	2025-07-06 11:43:06.183311	11
140	Два узла, находящиеся в разных подсетях, имеют IP-адреса. В масках обеих подсетей одинаковое количество единиц. Определить наименьшее значение третьего слева байта маски.\r\n	36	2025-04-11 12:15:18.400875	1
141	Даны IP-адрес и адрес подсети. Определить количество значений третьего слева байта маски, если в сети не менее К узлов.	36	2025-04-11 12:15:23.379951	1
142	1. Алгоритм строит по входному числу N новое - R: строится двоичная запись N; дописываются разряды по правилу. Определить минимальное число N>100, при котором получается R=9.\r\n🔹Решение на python\r\n🔹5:03 - Как работают срезы?	37	2025-04-11 12:16:21.802809	1
143	2. Алгоритм строит по входному числу N новое - R: строится восьмибитная двоичная запись N; меняются разряды по правилу. Определить число N, при котором R=113.\r\n🔹Решение руками и на python\r\n🔹16:15 - метод zfill\r\n🔹17:12 - Как сделать инверсию бит с помощью функции replace?	37	2025-04-11 12:16:25.650744	1
144	Алгоритм строит по входному числу N новое - R: строится двоичная запись N; дописываются разряды по правилу. Определить минимальное N, для которого искомое число R>=120.\r\n🔹 Решение на python	37	2025-04-11 12:16:30.542004	1
145	Алгоритм строит по входному числу N новое - R: строится троичная запись N; дописываются разряды по правилу. Определить минимальное R>133, которое может получиться.\r\n🔹 Решение на python\r\n🔹30:24 - Как перевести число из 10с.с. в 3с.с. с помощью функции?	37	2025-04-11 12:16:34.794282	1
146	Определить максимальное N, для которого найдутся такие значения a и b, что после выполнения программы чертежник возвратится в исходную точку.\r\n🔹 Решение на python	37	2025-04-11 12:16:42.35767	1
147	Исполнитель редактор. Определить наименьшее количество единиц в исходной строке, если на выходе получилось 21.\r\n🔹 Решение на python	37	2025-04-11 12:16:46.728049	1
148	Исполнитель редактор. Определить наибольшую сумму цифр в выходной строке при заданной исходной.\r\n🔹Решение на python	37	2025-04-11 12:16:51.032175	1
149	Операнды выражения записаны в 17 с.с. Определить наименьшее Х, при котором значение выражения кратно 11.\r\n🔹Решение на python	37	2025-04-11 12:16:55.517671	1
150	Значение выражения записали в 3 с.с. Определить наибольшее Х, при котором в значении выражения содержится ровно пять нулей.\r\n🔹Решение на python	37	2025-04-11 12:16:59.559663	1
151	Значение выражения записали в 6 с.с. Определить наименьшее Х, при котором в значении выражения содержится 202 нуля.\r\n🔹Решение на python	37	2025-04-11 12:17:03.305592	1
152	Значение выражения записано в 25 с.с. Определить количество значащих нулей в этой записи. \r\n🔹Решение на python	37	2025-04-11 12:17:06.762185	1
153	Логическая функция F задается выражением. Дан фрагмент таблицы истинности. Определить, какому столбцу таблицы соответствует каждая из переменных.\r\n🔹Решение стандартным способом с помощью вложенных циклов\r\n🔹Решение с помощью модуля itertools	38	2025-04-11 12:18:10.359117	1
154	Логическая функция F задается выражением. Дан фрагмент таблицы истинности. Определить, какому столбцу таблицы соответствует каждая из переменных.	38	2025-04-11 12:18:14.410771	1
155	Сколько слов можно составить так, чтобы в каждом из них гласные буквы не повторялись?\r\n🔹Решение на python	38	2025-04-11 12:18:17.278176	1
156	Сколько существует шестнадцатеричных трехзначных чисел, в которых все цифры различны и никакие две нечетные и две нечетные цифры не стоят рядом?\r\n🔹Решение на python	38	2025-04-11 12:18:20.72457	1
157	Определить количество семизначных чисел, записанных в 9 с.с., в записи которых ровно одна цифра 2 и ровно три нечетные цифры. \r\n🔹Решение на python	38	2025-04-11 12:18:25.230275	1
158	Составленные слова записаны в алфавитном порядке. Определить номер последнего слова, которое не содержит Ф и содержит ровно две У.\r\n🔹Решение на python	38	2025-04-11 12:18:30.067229	1
159	Даны адрес сети и маска. Сколько в этой сети IP-адресов, для которых сумма единиц в двоичной записи IP-сети четна?\r\n🔹Решение на python	38	2025-04-11 12:18:33.857455	1
160	Даны адрес сети и маска. Сколько в этой сети IP-адресов, для которых количество единиц в двоичной записи IP-адреса не кратно 5?\r\n🔹Решение на python	38	2025-04-11 12:18:38.002715	1
176	Исполнитель черепаха. Определить, сколько точек с целочисленными координатами будут находиться внутри области, полученной при объединении двух фигур.\r\n🔹Решение на Python в IDLE	44	2025-04-11 12:23:34.549142	1
177	На числовой прямой даны два отрезка: P = [3,33] и Q = [22, 44]. Выберите такой\r\nотрезок A, что формула\r\n(x ∈ Q) → ((x ∈ P) → (x ∈ A))\r\nтождественно истинна, то есть принимает значение 1 при любом значении переменной x.	46	2025-04-11 12:24:29.505978	1
637	Найти сумму цифр трехзначного числа	191	2025-07-06 11:43:19.766556	11
161	За один ход игрок может добавить в одну из куч (по своему выбору) два камня или увеличить количество камней в куче в три раза. Для того, чтобы сделать ходы, у игрока есть неограниченное количество камней. Игра завершается в тот момент, когда суммарное количество камней. Игра завершается в тот момент, когда суммарное количество камней в кучах становится не менее 68. Победителей считается игрок, сделавший последний ход. то есть первым получивший такую позицию, что в кучах всего будет 68 или больше камней. В начальный момент в куче было 8 камней, во второй куче - S камней; 1<=S<=59.\r\n1. При каких S: 1а) Петя выигрывает первым ходом; 1б) Ваня выигрывает первым ходом?\r\n2. Назовите одно любое значение S, при котором Петя может выиграть своим вторым ходом. \r\n3. Назовите значение S, при котором Ваня выигрывает своим первым или вторым ходом.	39	2025-04-11 12:19:26.657212	1
162	За один ход игрок может\r\na) добавить в кучу один камень;\r\nb) увеличить количество камней в куче в два раза;\r\nc) увеличить количество камней в куче в три раза.\r\nИгра завершается в тот момент, когда количество камней в куче становится не менее 42. Если при этом в куче оказалось не более 72 камней, то победителем считается игрок, сделавший последний ход. В противном случае победителем становится противник. В начальный момент в куче было S камней, 1<=S<=41. Игра завершается в тот момент, когда количество камней в куче становится не менее 42. \r\nЗадание 1. \r\na) При каких значениях числа S Петя может выиграть в один ход?\r\nb) У кого из игроков есть выигрышная стратегия при S = 37, 38, 39\r\nЗадание 2. У кого из игроков есть выигрышная стратегия при S = 13?	39	2025-04-11 12:19:32.459051	1
163	За один ход игрок\r\nможет добавить в кучу один камень, добавить в кучу четыре камня или увеличить\r\nколичество камней в куче в два раза. Например, имея кучу из 15 камней, за один\r\nход можно получить кучу из 16, 19 или 30 камней. У каждого игрока, чтобы делать\r\nходы, есть неограниченное количество камней. Игра завершается в тот момент, когда количество камней в куче становится не менее 20. Победителем считается игрок,\r\nсделавший последний ход, то есть первым получивший кучу, в которой будет 20 или\r\nбольше камней. В начальный момент в куче было S камней, 1 ≤ S ≤ 19.\r\n1. При каких S:\r\n1а) Петя выигрывает первым ходом;\r\n1б) Ваня выигрывает первым ходом?\r\n2. Назовите два значения S, при которых Петя может выиграть своим вторым\r\nходом.\r\n3. Назовите два значения S, при которых Ваня выигрывает своим первым или\r\nвторым ходом.	40	2025-04-11 12:20:36.997252	1
164	За один ход игрок может\r\na) добавить в кучу три камня или\r\nб) увеличить количество камней в куче в три раза и убрать из кучи 1 камень.\r\nНапример, имея кучу из 10 камней, за один ход можно получить кучу из 13 или\r\n29 камней. У каждого игрока, чтобы делать ходы, есть неограниченное количество\r\nкамней. Игра завершается в тот момент, когда количество камней в куче становится\r\nне менее 50. Победителем считается игрок, сделавший последний ход, то есть первым\r\nполучивший кучу, в которой будет 50 или больше камней.\r\nВ начальный момент в первой куче было 5 камней, во второй куче было S камней,\r\n1 ≤ S ≤ 49.\r\n1. При каких S:\r\n1а) Петя выигрывает первым ходом;\r\n16) Ваня выигрывает первым ходом?\r\n2. Назовите все значения S, при которых Петя может выиграть своим вторым\r\nходом?\r\n3. Назовите все значения S, при которых Ваня выигрывает своим первым или\r\nвторым ходом	40	2025-04-11 12:20:45.019704	1
165	Найти длину самой длинной подцепочки, состоящей из символов С.\r\n🔹Решение стандартным способом\r\n🔹Решение через поиск (цикл while)\r\n🔹Решение проходом по строке (наиболее универсальный вариант)\r\n🔹Решение через генератор\r\n🔹23:16 - Функция map	41	2025-04-11 12:21:55.555109	1
166	Найти максимальную длину цепочки вида BAFEBAFE..\r\n🔹 Решение на python двумя способами\r\n	41	2025-04-11 12:22:02.320372	1
167	Определить максимальное количество идущих подряд символов, среди которых нет сочетания QW.	41	2025-04-11 12:22:06.109976	1
168	Определить максимальное количество идущих подряд символов NPO или PNO.\r\n	41	2025-04-11 12:22:09.918703	1
169	Найти максимальное количество подряд идущих четверок символов АВЕС, BDAC, CAFB, CFBA, стоящих одна за другой и пересекающихся с соседними одной буквой.	41	2025-04-11 12:22:14.820845	1
170	Определить максимальное количество идущих подряд символов, среди которых буква А встречается не более 5 раз.	41	2025-04-11 12:22:18.593659	1
171	Определить минимальное число N, при обработке которого получается R>184.	44	2025-04-11 12:23:08.686061	1
172	Определить наибольшее число N<100, при обработке которого получается четное R, не кратное 4.	44	2025-04-11 12:23:13.2772	1
178	На числовой прямой даны два отрезка: P = [20,70] и Q = [5,32]. Выберите из\r\nпредложенных вариантов такой отрезок A, что логическое выражение\r\n((x ∈ P) ∧ (x ∈ A)) → ((x ∈ Q) ∧ (x ∈ A))\r\nтождественно истинно, то есть принимает значение 1 при любом значении переменной x.	46	2025-04-11 12:24:35.073407	1
179	На числовой прямой даны два отрезка: P = [5; 30] и Q = [14; 23]. Укажите наибольшую возможную длину такого отрезка A, что формула\r\n((x ∈ P) ≡ (x ∈ Q)) → ¬(x ∈ A)\r\nтождественно истинна, то есть принимает значение 1 при любом значении переменной.	46	2025-04-11 12:24:43.065422	1
180	Элементами множеств A, P и Q являются натуральные числа, причём\r\nP = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20} и Q = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30}. Известно,\r\nчто выражение\r\n((x ∈ A) → ¬(x ∈ P)) ∧ (¬(x ∈ Q) → ¬(x ∈ A))\r\nистинно (т. е. принимает значение 1) при любом значении переменной . Определите\r\nнаибольшее возможное количество элементов множества A	46	2025-04-11 12:24:52.575198	1
181	Элементами множества A являются натуральные числа. Известно, что выражение\r\n¬(x ∈ A) → ¬((x ∈ {1, 2, 4, 8}) ∨ (x ∈ {1, 2, 3, 4, 5, 6}))\r\nистинно (т. е. принимает значение 1) при любом значении переменной x. Определите\r\nнаименьшее возможное количество элементов множества A.	46	2025-04-11 12:24:57.624132	1
182	Определите наибольшее натуральное число A, такое что выражение\r\n(X&A 6= 0) → ((X&30 = 0) → (X&20 6= 0))\r\nтождественно истинно (то есть принимает значение 1 при любом натуральном значении переменной X)?	46	2025-04-11 12:25:04.134393	1
183	Определите наименьшее натуральное число A, такое что выражение\r\n(X&25 6= 0) → ((X&17 = 0) → (X&A 6= 0))\r\nтождественно истинно (то есть принимает значение 1 при любом натуральном значении переменной X)?	46	2025-04-11 12:25:09.498468	1
184	Определите количество натуральных чисел A таких,\r\nчто выражение\r\n((x&7 6= 0) → ((x&A 6= 0) → (x&54 6= 0))) → ((x&27 = 0) ∧ (x&A 6= 0) ∧ (x&7 6= 0))\r\nтождественно ложно (то есть принимает значение 0 при любом натуральном значении переменной x)?	46	2025-04-11 12:25:13.799245	1
185	Ваня составляет коды перестановкой букв слова ВОДОПАД. Код должен состоять из 7 букв, каждая буква должна в нём встречаться столько же раз, сколько и в исходном слове. Кроме того, в коде две гласные не должны стоять рядом. Сколько различных слов может составить Ваня?	47	2025-04-11 12:26:07.458017	1
186	Добрыня составляем коды из букв, входящих в слово ДОБРЫНЯ. Код должен состоять из 6 букв, буквы в коде не должны повторяться, согласных в коде должно быть больше, чем гласных, две гласные буквы нельзя ставить рядом. Сколько различных кодов может составить Добрыня. 	47	2025-04-11 12:26:12.430721	1
187	Иван составляет 5-буквенные слова из букв А,Б,В,Г,Д,Я. Все буквы в четных позициях должны быть в алфавитном порядке. 	47	2025-04-11 12:26:16.701914	1
188	(ЕГЭ-2023) Сколько существует шестнадцатеричных трехзначных чисел, в которых все цифры различны и никакие две чётные и две нечётные цифры не стоят рядом?	47	2025-04-11 12:26:20.415941	1
189	Рассматриваются числа, восьмеричная запись которых содержит ровно 12 знаков. Определите количество таких чисел, в восьмеричной записи которых ровно пять нечетных цифр, причем никакие две нечетные и четные не стоят рядом.	47	2025-04-11 12:26:23.872301	1
190	Григорий придумывает 16-буквенные слова, состоящие из букв слова АНТИУТОПИЯ. Сколько различных слов, содержащих комбинацию АНТИУТОПИЯ, может составить Григорий, если все гласные, не входящие в искомую комбинацию, расположены в алфавитном порядке, а согласные - в обратном алфавитном порядке?	47	2025-04-11 12:26:28.088593	1
191	Вася составляет слова из букв слова ШАРЛАТАН. Код должен состоять из 8 букв и каждая буква в нем должна встречаться столько же раз, сколько в заданном слове. Кроме того, в коде должны стоять рядом две гласные или две согласные буквы. Сколько различных слов может составить Вася?	47	2025-04-11 12:26:33.428809	1
192	Определите количество 14-ричных пятизначных чисел, в записи которых ровно одна цифра 9 и не более трех цифр с числовым значением, превышающим 10.	47	2025-04-11 12:26:38.21798	1
193	Исполнитель редактор. Записать символы, которые имеют номера 20,80 и 120 в получившейся строке.\r\n🔹Решение на python	49	2025-04-11 12:27:35.680216	1
194	Исполнитель редактор. Определить минимально возможную длину исходной строки, при которой в результате работы программы получится строка, содержащая максимально возможное количество 1.\r\n🔹Решение на python	49	2025-04-11 12:27:39.00307	1
195	Исполнитель редактор. Определить, сколько различных строк, содержащих ровно 9 двоек, может получиться в результате применения программы к строкам, состоящим из 1 и 2.	49	2025-04-11 12:27:42.61662	1
638	Проверить четность числа	191	2025-07-06 11:43:31.063244	11
196	Сколько слов можно составить так, чтобы в каждом из них было не менее двух гласных, а между двумя гласными стояла хотя бы одна согласная?\r\n🔹Решение на python 	49	2025-04-11 12:27:46.50847	1
197	Определить количество шестизначных чисел, записанных в 42 с.с., в записи которых только одна 6, при этом никакая нечетная цифра не стоит рядом с 6.\r\n🔹Решение на python\r\n🔹Решение руками	49	2025-04-11 12:27:50.677785	1
198	Сколько чисел длиной 6 можно составить, если цифры идут в порядке убывания, при этом четные и нечетные цифры чередуются?\r\n🔹Решение на python	49	2025-04-11 12:27:55.612449	1
199	Определить количество пар, в которых хотя бы один элемент больше, чем наибольшее из всех чисел, делящихся на 133, и в восьмеричной записи хотя бы одного элемента содержится 3.	49	2025-04-11 12:28:01.687443	1
200	Определить количество пар, в которых запись только одного элемента заканчивается 3, а сумма квадратов элементов пары меньше, чем квадрат наименьшего из всех элементов, запись которых заканчивается на 3.	49	2025-04-11 12:28:05.992897	1
201	По заданным IP-адресу узла сети и маске определить адрес сети.	50	2025-04-11 12:28:36.082611	1
202	Даны IP-адрес и адрес сети. Определить третий слева байт маски.	50	2025-04-11 12:28:39.511152	1
203	Узлы с заданными IP-адресами находятся в одной сети. Определить наибольшее значение третьего слева байта маски.	50	2025-04-11 12:28:42.721339	1
204	Узлы с заданными IP-адресами находятся в одной сети. Определить наибольшее значение третьего слева байта маски.	50	2025-04-11 12:28:46.001196	1
205	Узлы с заданными IP-адресами находятся в разных подсетях. Определить наименьшее количество единиц в масках этих подсетей.	50	2025-04-11 12:28:49.35621	1
206	Сеть задана адресом и маской сети. Определить количество адресов в этой сети, для которых количество единиц в двоичной записи адреса не кратно 5.\r\n🔹Решение с прогой\r\n🔹1:13:56 - применение zfill	50	2025-04-11 12:28:52.927844	1
207	Сеть задана адресом и маской сети. Определить количество адресов в этой сети, для которых сумма единиц в двоичной записи адреса четна.	50	2025-04-11 12:28:56.497122	1
208	За один ход игрок может\r\nдобавить в кучу три камня или увеличить количество камней в куче в два раза.\r\nНапример, имея кучу из 15 камней, за один ход можно получить кучу из 18 или\r\n30 камней. У каждого игрока, чтобы делать ходы, есть неограниченное количество\r\nкамней. Игра завершается в тот момент, когда количество камней в куче становится\r\nне менее 33. Победителем считается игрок, сделавший последний ход, то есть первым\r\nполучивший кучу, в которой будет 33 или больше камней. В начальный момент в\r\nкуче было S камней, 1 ≤ S ≤ 32.\r\n1. При каких S: 1а) Петя выигрывает первым ходом; 1б) Ваня выигрывает первым\r\nходом?\r\n2. Назовите пять значений S, при которых Петя может выигрыть своим вторым\r\nходом?\r\n3. При каких S Ваня выигрывает своим первым или вторым ходом?	51	2025-04-11 12:29:35.768088	1
209	Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежат две\r\nкучи камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок\r\nможет\r\nа) добавить в одну из куч (по своему выбору) один камень или\r\nб) увеличить количество камней в куче в два раза.\r\nПобедителем считается игрок, сделавший последний ход, т.е. первым получивший\r\nтакую позицию, что в обеих кучах всего будет 38 камней или больше.\r\nЗадание 1. Для каждой из начальных позиций (7, 15), (9, 14) укажите, кто из\r\nигроков имеет выигрышную стратегию.\r\nЗадание 2. Для каждой из начальных позиций (7, 14), (8,14), (9, 13) укажите,\r\nкто из игроков имеет выигрышную стратегию.\r\nЗадание 3. Для начальной позиции (8,13) укажите, кто из игроков имеет выигрышную стратегию.	51	2025-04-11 12:31:47.100661	1
228	Определить минимальное время, через которое завершится выполнение всей совокупности процессов, при условии, что все независимые друг от друга процессы могут выполняться параллельно.\r\n🔹Решение через функцию ВПР	53	2025-04-11 12:46:11.035791	1
229	Определить максимальную продолжительность отрезка времени, в течение которого возможно одновременное выполнение четыре процессов, при условии, что все независимые друг от друга процессы могут выполняться параллельно.\r\n🔹1:39:35 - Диаграмма Ганта\r\n🔹Условное форматирование	53	2025-04-11 12:46:16.914615	1
230	Тест разбит на строки различной длины. Найти строку, содержащую наименьшее количество пар соседних букв, которые стоят в таком же порядке и в алфавите.\r\n5:35 - Решение на python	54	2025-04-11 12:46:57.704479	1
231	Определить количество подстрок длиной не менее К, которые начинаются буквой А, заканчиваются В и не содержат других букв А и В.\r\n28:30 - Решение на python\r\n	54	2025-04-11 12:47:01.728642	1
210	Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежат две\r\nкучи камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок\r\nможет добавить в одну из куч (по своему выбору) один камень или увеличить количество камней в куче в два раза. Для того чтобы делать ходы, у\r\nкаждого игрока есть неограниченное количество камней.\r\nИгра завершается в тот момент, когда суммарное количество камней в кучах становится не менее 47. Победителем считается игрок, сделавший последний ход, то\r\nесть первым получивший такую позицию, что в кучах всего будет 47 или больше\r\nкамней.\r\nВ начальный момент в первой куче было 4 камня, во второй куче — S камней;\r\n1 ≤ S ≤ 42.\r\n1. При каких S: 1а) Петя выигрывает первым ходом; 1б) Ваня выигрывает первым\r\nходом?\r\n2. Назовите одно любое значение S, при котором Петя может выиграть своим\r\nвторым ходом.\r\n3. Назовите значение S, при котором Ваня выигрывает своим первым или вторым\r\nходом.	51	2025-04-11 12:31:52.795243	1
211	За один ход игрок может\r\nа) добавить в кучу один камень или\r\nб) увеличить количество камней в куче в два раза.\r\nИгра завершается в тот момент, когда количество камней в куче становится не\r\nменее 28. Если при этом в куче оказалось не более 46 камней, то победителем считается игрок, сделавший последний ход. В противном случае победителем становится\r\nего противник. В начальный момент в куче было S камней, 1 ≤ S ≤ 27.\r\nЗадание 1. а) При каких значениях числа S Петя может выиграть в один ход?\r\nУкажите все такие значения и соответствующие ходы Пети.\r\nб) У кого из игроков есть выигрышная стратегия при S = 24, 25, 26? Опишите\r\nвыигрышные стратегии для этих случаев.\r\nЗадание 2. У кого из игроков есть выигрышная стратегия при S = 10, 11? Опишите соответствую-щие выигрышные стратегии.\r\nЗадание 3. У кого из игроков есть выигрышная стратегия при S = 8?	51	2025-04-11 12:31:57.703727	1
212	Определить количество пар, в которых хотя бы у одного элемента сумма цифр равна сумме цифр минимального элемента, кратного 37.	52	2025-04-11 12:44:32.555734	1
213	Определить количество пар и максимальную сумму элементов пар, в которых хотя бы одно число является палиндромом.	52	2025-04-11 12:44:36.341182	1
214	Определить количество пар и максимальную сумму элементов пар, в которых хотя бы одно число содержит четные цифры.	52	2025-04-11 12:44:39.912804	1
215	Определить количество пар и максимальную сумму элементов пар, в которых оба элемента содержат четные цифры.	52	2025-04-11 12:44:43.868182	1
216	Определить количество пар и максимальную сумму элементов пар, в которых хотя бы одно число содержит минимум две единицы.	52	2025-04-11 12:44:48.150821	1
217	Определить количество пар и максимальную сумму элементов пар, в которых хотя бы одно число кратно 6.\r\n	52	2025-04-11 12:44:52.196323	1
218	Определить количество троек и максимальную сумму элементов троек, в которых числа могут являться сторонами равнобедренного треугольника.	52	2025-04-11 12:44:55.906811	1
219	Определить количество соток и максимальную сумму элементов соток, в которых хотя бы 10 чисел в 3 с.с. являются палиндромами.	52	2025-04-11 12:44:59.211265	1
220	Определить количество четверок и максимальную сумму элементов четверок, в которых два числа являются простыми числами.	52	2025-04-11 12:45:02.589711	1
221	Определить количество десяток, в которых есть хотя бы 3 числа, которые равны сумме троичных цифр элементов последовательности, кратных 17.	52	2025-04-11 12:45:06.176048	1
222	Робот двигается по полю. Определить максимальную и мин. денежную сумму, которую может собрать робот.\r\n	53	2025-04-11 12:45:47.40981	1
223	Робот двигается по полю и собирает монеты с тех клеток, где количество монет четно. Определить максимальную и мин. денежную сумму, которую может собрать робот.\r\n	53	2025-04-11 12:45:51.294984	1
224	Робот двигается по полю с севера на юг. Робот собрал максимальную сумму на своем маршруте. Определить достоинства монет на первой и последней клетках маршрута.\r\n	53	2025-04-11 12:45:55.980426	1
225	Робот двигается по полю. Число в очередной клетке, через которую проходит робот, включается в сумму, если оно больше числа в предыдущей клетке маршрута. Определить мин. и макс. сумму, которую может получить робот.	53	2025-04-11 12:45:59.238154	1
226	Ладья двигается по полю. Определить минимальную и максимальную сумму чисел в клетках, в которых можно остановиться ладья.	53	2025-04-11 12:46:03.438466	1
227	Из последовательности выбрать несколько подряд идущих чисел так, чтобы каждое следующее число отличалось от предыдущего не более чем на 2. Определить макс. сумму выбранных чисел.	53	2025-04-11 12:46:07.137408	1
232	Убрать повторы одинаковых рядом стоящих букв в заданной строке.\r\n50:17 - Решение на python: способ 1\r\n53:04 - Решение на python: способ 2	54	2025-04-11 12:47:05.940215	1
233	Определить подстроку максимальной длины, состоящую только из букв и каких-нибудь символов.\r\n1:03:29 - Решение на python	54	2025-04-11 12:47:09.169419	1
234	Определить максимальное количество идущих подряд символов, среди которых нет сочетания символов QW.	54	2025-04-11 12:47:13.337539	1
235	Логическая функция F задается выражением. Определить, какому столбцу таблицы истинности функции F(n) соответствует каждая из переменных.\r\n	55	2025-04-11 12:47:28.650519	1
236	Логическая функция F задается выражением. Определить, какому столбцу таблицы истинности функции F(n) соответствует каждая из переменных.\r\n	55	2025-04-11 12:47:31.799441	1
237	Логические функции F1 и F2 задаются выражениями. Определить, какому столбцу таблицы истинности этих функций соответствует каждая из переменных.	55	2025-04-11 12:47:35.267618	1
238	Алгоритм строит по входному числу N новое - R: строится двоичная запись N; дописываются разряды по правилу. Определить наименьшее N, при обработке которого получается R>516.	55	2025-04-11 12:47:39.824264	1
239	Алгоритм строит по входному числу N новое - R: вычисляется S1 - сумма нечетных цифр числа; S2 - сумма цифр числа, стоящих в четных разрядах; вычисляется модуль разности S1 и S2. Определить наименьшее N, после обработки которого получается 29.	55	2025-04-11 12:47:43.227469	1
240	Исполнитель черепаха. Определить минимальное N, при котором черепаха оставит след в виде замкнутой ломаной линии.	55	2025-04-11 12:47:46.267781	1
241	Исполнитель черепаха. Определить количество точек фигуры, образованных пересечением отрезков.\r\n	55	2025-04-11 12:47:48.809347	1
242	Сколько слов можно составить так, чтобы в каждом из них Й использовалась не более 1 раза, и при этом не стояла на первом, последнем месте и рядом с Е.\r\n	55	2025-04-11 12:47:52.543574	1
243	Все составленные слова записаны в алфавитном порядке. Определить количество слов, находящихся между словами С1 и С2.	55	2025-04-11 12:47:56.797534	1
244	Исполнитель редактор. Какая строка получится в результате применения программы к исходной строке?	58	2025-04-11 12:49:32.409557	1
245	Исполнитель редактор. Какая строка получится в результате применения программы к исходной строке?	58	2025-04-11 12:49:38.321501	1
246	Исполнитель редактор. Какая строка получится в результате применения программы к исходной строке?	58	2025-04-11 12:49:40.055856	1
247	Исполнитель редактор. Определить сумму числовых значений цифр строки, получившейся в результате выполнения программы.	58	2025-04-11 12:49:44.905052	1
248	Исполнитель редактор. Какая строка получится в результате применения программы к исходной строке?\r\n	58	2025-04-11 12:49:48.039756	1
249	Исполнитель чертежник. Определить максимальное N, для которого найдутся такие a и b, что после выполнения программы чертежник вернется в исходную точку.\r\n	58	2025-04-11 12:49:51.656381	1
250	Исполнитель робот. Сколько клеток лабиринта соответствуют требованию, что, выполнив программу, робот уцелеет и остановится в той же клетке, с которой он начал?\r\n	58	2025-04-11 12:49:56.87858	1
251	Исполнитель робот. Сколько клеток лабиринта соответствуют требованию, что, выполнив программу, робот уцелеет и остановится в закрашенной клетке?\r\n	58	2025-04-11 12:50:01.887807	1
252	Исполнитель робот. Сколько клеток лабиринта соответствуют требованию, что, выполнив программу, робот уцелеет и остановится в закрашенной клетке?\r\n	58	2025-04-11 12:50:06.093423	1
253	Найти самую длинную подстроку, начинающуюся с символа С, заканчивающуюся символом D, и не содержащую других символов С и D.	60	2025-04-11 12:50:33.101817	1
254	Найти самую длинную подстроку, начинающуюся и оканчивающуюся на один и тот же символ, и не содержащую этот символ на других позициях.	60	2025-04-11 12:50:37.051106	1
255	Найти самую длинную подстроку, состоящую из комбинации ABCD, последний фрагмент может быть неполным.\r\n	60	2025-04-11 12:50:41.060157	1
256	Определить максимальное количество символов в непрерывной последовательности, являющейся корректным арифметическим выражением с целыми неотрицательными числами, значение которого не равно 0.	60	2025-04-11 12:50:57.323322	1
257	Вася составляет 5-буквенные коды из букв КАЛИЙ. Каждую букву нужно использовать ровно 1 раз, при этом код не может начинаться с буквы Й и не может содержать сочетания ИАК. Сколько различных кодов может составить Вася?	153	2025-04-11 12:53:20.867429	1
565	№7. Сколько времени потребуется для передачи изображения?	172	2025-05-10 19:45:01.8368	7
258	Петя составляет шестибуквенные слова с перестановкой букв слова КАБАЛА. При этом он избегает слов с двумя подряд одинаковыми буквами. Сколько всего различных слов может составить Петя?	153	2025-04-11 12:53:24.511786	1
259	(Демо-2025) Определите количество 12-ричных пятизначных чисел, в записи которых ровно одна цифра 7 и не более трёх цифр с числовым значением, превышающим 8. 	153	2025-04-11 12:53:28.57034	1
260	Добрыня составляет коды из букв, входящих в слово ДОБРЫНЯ. Код должен состоять из 6 букв, буквы в коде не должны повторяться, согласных в коде должно быть больше, чем гласных, две гласные буквы нельзя ставить рядом. Сколько различных кодом может составить Добрыня.	153	2025-04-11 12:53:34.259839	1
261	Определите количество шестизначных чисел, записанных в системе счисления с основанием 42, в записи которых только одна цифра 6, при этом никакая нечетная цифра не стоит рядом с цифрой 6. 	153	2025-04-11 12:53:39.705125	1
262	Вася составляет слова из букв слова ШАРЛАТАН. Код должен состоять из 8 букв, и каждая буква в нем должна встречаться столько же раз, сколько в заданном слове. Кроме того, в коде должны стоять рядом две гласные или две согласные буквы. 	153	2025-04-11 12:53:46.973096	1
263	Леся составляет слова, содержащие ровно 3 буквы М, из буквы Ч,О,А.Н,И,М,Е. Слово может иметь длину от 4 до 6 букв. Сколько различных слов может составить Леся?	153	2025-04-11 12:53:50.476724	1
264	Лида составляет слова из букв КРЫША. Каждая гласная буква встречается в слове не более двух раз. Каждая согласная может стоять в слове на первой позиции, либо не встречаться вовсе. Сколько различных слов длиною более двух символов может составить Лида?	153	2025-04-11 12:53:56.584328	1
265	Сколько существует чисел, восьмеричная запись которых содержит 8 цифр, причем все цифры различны и никакие две четные и две нечетные цифры не стоят рядом.	153	2025-04-11 12:54:01.561302	1
266	(ЕГЭ-2024) Все пятибуквенные слова, составленные из букв ФОКУС записаны в алфавитном порядке и пронумерованы. Дано начало списка. Под каким номеров в списке идет последнее слово, которое не содержит букв Ф и содержит ровно две буквы У?	153	2025-04-11 12:54:09.288701	1
267	Все четырехбуквенные слова, составленные из букв ВИНОГРАД записаны в алфавитном порядке и пронумерованы, начиная с 1. Под каким номеров в списке идет первое слово, которое начинается с ИР?	153	2025-04-11 12:54:16.188697	1
268	Все 5-буквенные слова, составленные из букв РОК, записаны в алфавитном порядке и пронумерованы. Запишите слово, которое стоит под номером 182. 	153	2025-04-11 12:54:20.335888	1
269	Все 5-буквенные слова, составленные из букв ДКМО записаны в алфавитном порядке и пронумерованы. Какое количество слов находится между словами ДОМОК и КОМОД (включая эти слова)?	153	2025-04-11 12:54:28.989197	1
270	(Досрочный ЕГЭ-2023) Входной файл содержит заявки пассажиров, желающих сдать свой багаж в камеру хранения. В заявке указаны время сдачи багажа и время освобождения ячейки (в минутах от начала суток). Багаж одного пассажира размещается в одной свободной ячейке с минимальным номером. Ячейки пронумерованы начиная с единицы. Размещение багажа в ячейке или её освобождение происходит в течение 1 мин. Багаж можно поместить в только что освобождённую ячейку начиная со следующей минуты. Если в момент сдачи багажа свободных ячеек нет, то пассажир уходит. Определите, сколько пассажиров сможет сдать свой багаж в течение 24 ч и какой номер будет иметь ячейка, которую займут последней. Если таких ячеек несколько, укажите минимальный номер ячейки.	81	2025-04-15 16:05:50.828025	1
271	(ЕГЭ-2023) На производстве штучных изделий N деталей должны быть отшлифованы и окрашены. Для каждой детали известно время её шлифовки и время окрашивания. Детали пронумерованы начиная с единицы. Параллельная обработка деталей не предусмотрена. На ленте транспортёра имеется N мест для каждой из N деталей. На ленте транспортёра детали располагают по следующему алгоритму:\r\n— все 2N чисел, обозначающих время окрашивания и шлифовки для N деталей, упорядочивают по возрастанию;\r\n— если минимальное число в этом упорядоченном списке — это время шлифовки конкретной детали, то деталь размещают на ленте транспортёра на первое свободное место от её начала;\r\n— если минимальное число — это время окрашивания, то деталь размещают на первое свободное место от конца ленты транспортёра;\r\n— если число обозначает время окрашивания или шлифовки уже рассмотренной детали, то его не принимают во внимание.\r\nЭтот алгоритм применяется последовательно для размещения всех N деталей. Определите номер последней детали, для которой будет определено её место на ленте транспортёра, и количество деталей, которые будут отшлифованы до неё.	81	2025-04-15 16:06:02.571316	1
341	Определите количество различных чисел, которые могут быть получены командами +1; +2; ·2 из числа 5 с помощью 8-ми различных команд.	107	2025-04-16 10:09:25.320224	1
342	Имеется набор данных, состоящий из пар положительных целых чисел. Необходимо выбрать из каждой пары ровно одно число так, чтобы сумма всех выбранных чисел делилась на 5 и при этом была максимально возможной. Гарантируется, что искомую сумму получить можно.	108	2025-04-16 10:10:35.431881	1
272	(ЕГЭ-2023) Система наблюдения ежеминутно фиксирует вход и выход посетителей магазина (в минутах, прошедших от начала суток). Считается, что в минуты фиксации входа и выхода посетитель находится в магазине. Нулевая минута соответствует моменту открытия магазина, который работает 24 ч в сутки без перерыва. Менеджер магазина анализирует данные системы наблюдения за прошедшие сутки и выявляет отрезки времени наибольшей длины, в течение которых число посетителей, находящихся в магазине, не изменялось. Далее менеджер выбирает пики посещаемости — промежутки времени, когда количество посетителей в магазине было наибольшим. Пиков посещаемости в течение суток может быть несколько. Входной файл содержит время входа и выхода каждого посетителя магазина. Определите, сколько пиков посещаемости было в течение суток, и укажите число посетителей в момент пика посещаемости.	81	2025-04-15 16:06:10.355559	1
273	(ЕГЭ-2023) Входной файл содержит сведения о заявках на проведение занятий в конференц-зале. В каждой заявке указаны время начала и время окончания мероприятия (в минутах от начала суток). Если время начала одного мероприятия меньше времени окончания другого, то провести можно только одно из них. Если время окончания одного мероприятия совпадает с временем начала другого, то провести можно оба. Определите максимальное количество мероприятий, которое можно провести в конференц-зале и самое позднее время окончания последнего мероприятия.	82	2025-04-15 16:09:16.268084	1
274	(ЕГЭ-2024) При онлайн-покупке билета на концерт известно, какие места в зале уже заняты. Необходимо купить два билета на такие соседние места в одном ряду, чтобы перед ними все кресла с такими же номерами были свободны, а ряд находился как можно дальше от сцены. Если в этом ряду таких пар мест несколько, найдите пару с наибольшими номерами мест. Нумерация рядов и мест ведётся с 1. Гарантируется, что хотя бы одна такая пара в зале есть. Определите наибольший номер ряда и наибольший номер места для найденной пары мест.	82	2025-04-15 16:09:26.999785	1
275	Системный администратор раз в неделю создает архив пользовательских файлов. Однако объем диска может быть меньше, чем суммарный объем файлов. Известно, какой объем занимает файл каждого пользователя. По заданной информации определите максимальное число пользователей, чьи файлы можно сохранить в архиве, а также максимальный размер файла, который может быть сохранен при этом.	80	2025-04-15 16:22:09.762033	1
276	Магазин предоставляет скидку: на каждый второй товар дороже 200 рублей — 30%. Общая сумма округляется вверх. Порядок определяет магазин — он минимизирует сумму скидки. Определите общую цену покупки с учетом скидки и цену самого дорогого товара, на который будет предоставлена скидка.	80	2025-04-15 16:22:16.678355	1
277	Организация купила все места в нескольких рядах. Известно, какие места заняты. Найдите ряд с наибольшим номером, где есть два соседних свободных места, окружённых с обеих сторон занятыми.	80	2025-04-15 16:22:23.503655	1
278	На закупку товаров Q и Z выделена сумма. Нужно купить как можно больше товаров обоих типов. При равном количестве — выбрать вариант с наибольшим числом Q. При равенстве — потратить как можно меньше. Определите количество купленных товаров Q и оставшиеся деньги.	80	2025-04-15 16:22:29.35722	1
279	Для перевозки грузов массой от 180 до 200 кг включительно приоритет — сначала их грузят по убыванию массы. Потом стараются добрать как можно больше легких грузов на оставшуюся грузоподъемность. При равенстве — выбирают вариант с наибольшим по массе грузом. Определите количество и общую массу вывезенных грузов.	80	2025-04-15 16:22:34.752614	1
280	При онлайн-покупке билета на концерт известно, какие места в зале уже заняты. Необходимо купить билет на такое место в ряду, чтобы перед ним как можно больше идущих подряд кресел с таким же номером было свободно. Если места, удовлетворяющие этому условию, есть в нескольких рядах, то нужно выбрать ряд, расположеннный как можно ближе к сцене. В ответе запишите два целых числа: искомый номер ряда и количество свободных кресел перед выбранным местом. Нумерация рядов и мест ведётся с 1. Гарантируется, что хотя бы одно такое место в зале есть.\r\nВходные данные\r\nВ первой строке входного файла находятся три числа: N — количество занятых мест в зале (целое положительное число, не превышаюшее 10 000), М — количество рядов (целое положительное число, не превышающее 100 000) и К — количество мест в каждом ряду (целое положительное число, не превышающее 100 000). В следующих N строках находятся пары натуральных чисел: номер ряда и номер места занятого кресла соответственно (первое число не превышает значения М, а второе — К ).\r\nВыходные данные\r\nДва целых положительных числа: искомый номер ряда и количество свободных кресел перед выбранным местом.	83	2025-04-15 16:23:44.987084	1
395	Сеть задана IP-адресом и маской сети. Определить кол-во IP-адресов, в записи которых имеется сочетание трех подряд идущих единиц.	67	2025-04-20 18:06:13.607884	7
396	Даны IP-адрес и адрес сети. Определить наим. количество единиц в двоичной записи маски подсети.	67	2025-04-20 18:06:19.28706	7
281	(ЕГЭ-2024) При онлайн-покупке билета на концерт известно, какие места в зале уже заняты. Необходимо купить два билета на такие соседние места в одном ряду, чтобы перед ними все кресла с такими же номерами были свободны, а ряд находился как можно дальше от сцены. Если в этом ряду таких пар мест несколько, найдите пару с наибольшими номерами мест. Нумерация рядов и мест ведётся с 1. Гарантируется, что хотя бы одна такая пара в зале есть. Определите наибольший номер ряда и наибольший номер места для найденной пары мест.\r\nВходные данные представлены в файле 26-150.txt следующим образом. В первой строке входного файла находятся три числа: N — количество занятых мест в зале (целое положительное число, не превышающее 10 000), М — количество рядов (целое положительное число, не превышающее 100 000) и К — количество, мест в каждом ряду (целое положительное число, не превышающее 100 000). В следующих N строках находятся пары натуральных чисел: номер ряда и номер места занятого кресла соответственно (первое число не превышает значения М, а второе — K ). Запишите в ответе два целых числа: искомый номер ряда и наибольший номер места в найденной паре.\r\nПример входного файла:\r\n7 7 8\r\n1 1\r\n6 6\r\n5 5\r\n6 7\r\n4 4\r\n2 2 \r\n3 3\r\nУсловию задачи удовлетворяют места 7 и 8 в ряду 5: перед креслами 7 и 8 нет\r\nзанятых мест и это последняя из двух возможных пар в этом ряду. В рядах 6 и 7 искомую пару найти нельзя. Ответ: 5 8.	83	2025-04-15 16:26:31.336646	1
282	На парковке имеется 80 мест для легковых автомобилей и 20 мест для микроавтобусов. Приезжающий на парковку автомобиль занимает любое свободное место соответствующего типа. При этом если свободных мест для легковых автомобилей нет, то легковой автомобиль занимает свободное место, предназначенное для микроавтобуса, но микроавтобус не может занять место, предназначенное для легкового автомобиля. Если подходящего места нет, автомобиль уезжает.\r\nВходные данные\r\nПервая строка входного файла содержит целое число N – общее количество автомобилей, в течение суток приехавших на парковку. Каждая из следующих N строк описывает один автомобиль и содержит 2 целых числа и букву. Первое число означает время в минутах с начала суток, когда автомобиль прибыл на парковку, второе – необходимую длительность стоянки в минутах. Буква означает тип автомобиля: A – легковой, B – микроавтобус. Гарантируется, что никакие два автомобиля не приезжают одновременно. Если время прибытия автомобиля совпадает со временем окончания стоянки другого автомобиля, вновь прибывший автомобиль может занять освободившееся место, если оно подходит ему по типу.\r\nВыходные данные\r\nВ ответе запишите два целых числа: сначала количество легковых автомобилей, которые смогут припарковаться, затем – общее количество автомобилей (как легковых, так и микроавтобусов), которые уедут из-за отсутствия мест.	84	2025-04-15 16:28:12.415707	1
283	(ЕГЭ-2023) Входной файл содержит сведения о заявках на проведение занятий в конференц-зале. В каждой заявке указаны время начала и время окончания мероприятия (в минутах от начала суток). Если время начала одного мероприятия меньше времени окончания другого, то провести можно только одно из них. Если время окончания одного мероприятия совпадает с временем начала другого, то провести можно оба. Определите максимальное количество мероприятий, которое можно провести в конференц-зале и самое позднее время окончания последнего мероприятия.\r\nВходные данные представлены в файле 26-128.txt следующим образом. Первая строка входного файла содержит натуральное число N (1 ≤ N ≤ 1000) – количество заявок на проведение мероприятий. Следующие N строк содержат пары чисел, обозначающих время начала и время окончания мероприятий. Каждое из чисел натуральное, не превосходящее 1440.\r\nЗапишите в ответе два числа: максимальное количество мероприятий, которое можно провести в конференц-зале и самое позднее время окончания последнего мероприятия (в минутах от начала суток).\r\nПример входного файла:\r\n5\r\n10 150\r\n100 110\r\n131 170\r\n131 180\r\n120 130\r\nПри таких исходных данных можно провести максимум три мероприятия, например, по заявкам 2, 3 и 5. Конференц-зал освободится самое позднее на 180-й минуте, если состоятся мероприятия по заявкам 2, 4, 5. Ответ: 3 180.	85	2025-04-15 16:31:16.965989	1
284	Входной файл содержит сведения о заявках на проведение занятий в конференц-зале. В каждой заявке указаны время начала и время окончания мероприятия (в минутах от начала суток). Если время начала одного мероприятия меньше времени окончания другого, то провести можно только одно из них. Если время окончания одного мероприятия совпадает с временем начала другого, то провести можно оба. Определите максимальное количество мероприятий, которое можно провести в конференц-зале и самое позднее время окончания последнего мероприятия.\r\nВходные данные представлены в файле 26-128.txt следующим образом. Первая строка входного файла содержит натуральное число N (1 ≤ N ≤ 1000) – количество заявок на проведение мероприятий. Следующие N строк содержат пары чисел, обозначающих время начала и время окончания мероприятий. Каждое из чисел натуральное, не превосходящее 1440. Запишите в ответе два числа: максимальное количество мероприятий, которое можно провести в конференц-зале и самое позднее время окончания последнего мероприятия (в минутах от начала суток).	86	2025-04-15 16:32:43.571698	1
285	Система наблюдения ежеминутно фиксирует вход и выход посетителей магазина (в минутах, прошедших от начала суток). Считается, что в минуты фиксации входа и выхода посетитель находится в магазине. Нулевая минута соответствует моменту открытия магазина, который работает 24 ч в сутки без перерыва. Менеджер магазина анализирует данные системы наблюдения за прошедшие сутки, и выявляет отрезки времени наибольшей длины, в течение которых число посетителей, находящихся в магазине, не изменялось. Далее менеджер выбирает пики посещаемости – промежутки времени, когда количество посетителей в магазине было наибольшим. Пиков посещаемости в течение суток может быть несколько.\r\nВходной файл содержит время входа и выхода каждого посетителя магазина. Определите, сколько пиков посещаемости было в течение суток, и укажите число посетителей в момент пика посещаемости.\r\nВходные данные представлены в файле 26-130.txt следующим образом. Первая строка входного файла содержит натуральное число N (1 ≤ N ≤ 10000) – количество посетителей магазина. Следующие N строк содержат пары чисел, обозначающих соответственно время входа и время выхода посетителя (все числа натуральные, не превышающие 1440). Запишите в ответе два натуральных числа: сначала найденное количество пиков посещаемости, а затем число посетителей в момент пика посещаемости.	86	2025-04-15 16:33:47.244251	1
286	В магазине есть N камер хранения. Номера камер начинаются с 1. В магазин приходят покупатели и оставляют свои вещи в камерах хранения. Покупатель занимает одну из камер с минимальным номером. Следующий покупатель может занять камеру хранения со следующей минуты после освобождения камеры. Освобождение камеры длится 3 минуты. Известно время сдачи вещей каждого покупателя и время выдачи вещей каждому покупателю. Если свободных камер нет, то покупатели уходят. Если осталась свободной только одна камера, а в один момент пришло несколько покупателей, то вещи в камеру положит клиент, у которого меньшее количество времени вещи будут находиться в камере.\r\nВходные данные: В первой строке файла находится натуральное число K, не превышающее 1000, – количество покупателей. Во второй строке файла находится натуральное число N, не превышающее 1000 – количество камер хранения в магазине. В последующих строках записано по два числа, не превышающих 1500: время прибытия клиента, время ухода клиента.\r\nЗапишите в ответ два числа через пробел: количество покупателей, которые смогли положить вещи в камеру хранения, и номер камеры, в которую положил вещи последний покупатель.	86	2025-04-15 16:34:52.121582	1
343	(А. Жуков) В вход программы поступают N ≤ 1000 натуральных чисел, каждое из которых не превышает 10000. Необходимо определить количество пар элементов (a_i, a_j) этого набора, в которых 1 ≤ i < j ≤ N, сумма элементов нечетна, произведение делится на 13, а номера чисел в последовательности отличаются МЕНЕЕ, чем на 5.	109	2025-04-16 10:10:52.700391	1
397	Даны IP-адрес и адрес сети. Определить третий слева байт маски.	67	2025-04-20 18:06:27.219869	7
287	(Демо-2021). Системный администратор раз в неделю создаёт архив пользовательских файлов. Однако объём диска, куда он помещает архив, может быть меньше, чем суммарный объём архивируемых файлов. Известно, кокой объём занимает файл каждого пользователя. По заданной информации об объёме файлов пользователей и свободном объёме на архивном диске определите максимальное число пользователей, чьи файлы можно сохранить в архиве, а также максимальный размер имеющегося файла, который может быть сохранён в архиве, при условии, что сохранены файлы максимально возможного числа пользователей.\r\nВходные данные. В первой строке входного файла 26-5.txt находятся два числа: S – размер свободного места на диске (натуральное число, не превышающее 100 000) и N – количество пользователей (натуральное число, не превышающее 10000). В следующих N строках находятся значения объёмов файлов каждого пользователя (все числа натуральные, не превышающие 100), каждое в отдельной строке. Запишите в ответе два числа: сначала наибольшее число пользователей, чьи файлы могут быть помещены в архив, затем максимальный размер имеющегося файла, который может быть сохранён в архиве, при условии, что сохранены файлы максимально возможного числа пользователей.	87	2025-04-15 16:36:13.645079	1
288	Магазин предоставляет оптовому покупателю скидку по следующим правилам: \r\n– на каждый второй товар ценой больше 100 рублей предоставляется скидка 10%; \r\n– общая цена покупки со скидкой округляется вверх до целого числа рублей;\r\n– порядок товаров в списке определяет магазин и делает это так, чтобы общая сумма скидки была наименьшей.\r\nВам необходимо определить общую цену закупки с учётом скидки и цену самого дорогого товара, на который будет предоставлена скидка.\r\nВходные данные. Первая строка входного файла 26-s1.txt содержит число N – общее количество купленных товаров. Каждая из следующих строк содержит одно целое число – цену товара в рублях. В ответе запишите два целых числа: сначала общую цену покупки с учётом скидки, затем цену самого дорогого товара, на который предоставлена скидка.\r\nПример входного файла\r\n7\r\n225\r\n160\r\n380\r\n95\r\n192\r\n310\r\n60\r\nВ данном случае товары с ценой 60 и 95 не участвуют в определении скидки, остальные товары магазину выгодно расположить в таком порядке цен: 380, 160, 225, 192, 310. Скидка предоставляется на товары ценой 160 и 192. Суммарная цена этих двух товаров со скидкой составит 316,8 руб., после округления – 317 руб. Общая цена покупки составит: 60 + 95 + 317 + 380 + 225 + 310 = 1387 руб. Самый дорогой товар, на который будет получена скидка, стоит 192 руб. В ответе нужно записать числа 1387 и 192.	87	2025-04-15 16:37:21.258361	1
289	Организация купила для своих сотрудников все места в нескольких подряд идущих рядах на концертной площадке. Известно, какие места уже распределены между сотрудниками. Найдите ряд с наибольшим номером, в котором есть два соседних места, таких что слева и справа от них в том же ряду места уже распределены (заняты). Гарантируется, что есть хотя бы один ряд, удовлетворяющий условию.\r\nВходные данные представлены в файле 26-59.txt следующим образом. В первой строке входного файла находится одно число: N – количество занятых мест (натуральное число, не превышающее 10 000). В следующих N строках находятся пары чисел: ряд и место выкупленного билета, не превышающие 100 000. В ответе запишите два целых числа: номер ряда и наименьший номер места из найденных в этом ряду подходящих пар.\r\nПример входного файла:\r\n10\r\n5 5\r\n5 9\r\n5 6\r\n16 9\r\n16 3\r\n16 6\r\n20 23\r\n20 28\r\n20 35\r\n20 40\r\nВ данном примере есть следующие свободные места, удовлетворяющие условию: 7 и 8 в ряду 5, 4 и 5 в ряду 16, а также 7 и 8 в ряду 16. Выбираем наибольший номер ряда: 16 и наименьший номер места: 4. В ответе нужно указать: 16 4.	87	2025-04-15 16:40:58.266248	1
290	На закупку товаров типов Q и Z выделена определённая сумма денег. Эти товары есть в продаже по различной цене. Необходимо на выделенную сумму закупить как можно больше товаров двух типов (по общему количеству). Если можно разными способами купить максимальное количество двух товаров, то нужно выбрать способ, при котором будет закуплено как можно больше товаров типа Q. Если при этих условиях есть несколько способов закупки, нужно потратить как можно меньше денег.\r\nОпределите, сколько будет закуплено товаров типа Q и сколько денег останется.\r\nВходные данные представлены в файле 26-62.txt следующим образом. Первая строка входного файла содержит два целых числа: N – общее количество товаров и M – сумма выделенных на закупку денег (в рублях). Каждая из следующих N строк содержит целое число (цена товара в рублях) и символ (латинская буква Q или Z), определяющий тип товара. Все данные в строках входного файла отделены одним пробелом.\r\nЗапишите в ответе два числа: сначала количество закупленных товаров типа Q, затем оставшуюся неиспользованной сумму денег.\r\nПример входного файла:\r\n6 110\r\n40 Z\r\n50 Q\r\n50 Z\r\n30 Z\r\n20 Q\r\n10 Z\r\nВ данном случае можно купить не более четырёх товаров, из них не более двух товаров типа Q. Минимальная цена такой покупки 110 рублей (покупаем товары 10 Z, 20 Q, 30 Z, 50 Q). Останется 0 рублей. Ответ: 2 0.	87	2025-04-15 16:41:43.54942	1
291	Входной файл содержит сведения о заявках на проведение занятий в конференц-зале. В каждой заявке указаны время начала и время окончания мероприятия (в минутах от начала суток). Если время начала одного мероприятия меньше времени окончания другого, то провести можно только одно из них. Если время окончания одного мероприятия совпадает с временем начала другого, то провести можно оба. Определите максимальное количество мероприятий, которое можно провести в конференц-зале и самое позднее время окончания последнего мероприятия.\r\nВходные данные представлены в файле 26-128.txt следующим образом. Первая строка входного файла содержит натуральное число N (1 ≤ N ≤ 1000) – количество заявок на проведение мероприятий. Следующие N строк содержат пары чисел, обозначающих время начала и время окончания мероприятий. Каждое из чисел натуральное, не превосходящее 1440. Запишите в ответе два числа: максимальное количество мероприятий, которое можно провести в конференц-зале и самое позднее время окончания последнего мероприятия (в минутах от начала суток).\r\nПример входного файла:\r\n5\r\n10 150\r\n100 110\r\n131 170\r\n131 180\r\n120 130\r\nПри таких исходных данных можно провести максимум три мероприятия, например, по заявкам 2, 3 и 5. Конференц-зал освободится самое позднее на 180-й минуте, если состоятся мероприятия по заявкам 2, 4, 5. Ответ: 3 180.	88	2025-04-15 16:48:58.524249	1
292	(Досрочный ЕГЭ-2023) Входной файл содержит заявки пассажиров, желающих сдать свой багаж в камеру хранения. В заявке указаны время сдачи багажа и время освобождения ячейки (в минутах от начала суток). Багаж одного пассажира размещается в одной свободной ячейке с минимальным номером. Ячейки пронумерованы начиная с единицы. Размещение багажа в ячейке или её освобождение происходит в течение 1 мин. Багаж можно поместить в только что освобождённую ячейку начиная со следующей минуты. Если в момент сдачи багажа свободных ячеек нет, то пассажир уходит. Определите, сколько пассажиров сможет сдать свой багаж в течение 24 ч и какой номер будет иметь ячейка, которую займут последней. Если таких ячеек несколько, укажите минимальный номер ячейки.\r\nВходные данные представлены в файле 26-111.txt следующим образом. В первой строке входного файла находится натуральное число K, не превышающее 1000, – количество ячеек в камере хранения. Во второй строке – натуральное число N (N ≤ 1000), обозначающее количество пассажиров, Каждая из следующих N строк содержит два натуральных числа, каждое из которых не превышает 1440: указанное в заявке время размещения багажа в ячейке и время освобождения ячейки (в минутах от начала суток). Запишите в ответе два числа: количество пассажиров, которые смогут воспользоваться камерой хранения, и номер последней занятой ячейки.\r\nПример входного файла:\r\n2\r\n5\r\n30 60\r\n40 1000\r\n59 60\r\n61 1000\r\n1010 1440\r\nПри таких исходных данных положить вещи в камеру хранения смогут первый, второй, четвёртый и пятый пассажиры. Последний пассажир положит вещи в ячейку 1, так как ячейки 1 и 2 будут свободны. Ответ: 4 1	88	2025-04-15 16:50:13.171045	1
344	(А. Жуков) Имеется набор данных, состоящий из положительных целых чисел. Необходимо определить количество пар элементов (a_i, a_j) этого набора, в которых 1 ≤ i + 5 ≤ j ≤ N, сумма элементов нечетна, а произведение делится на 13.	109	2025-04-16 10:10:58.003454	1
398	Даны IP-адрес и маска сети. Определить кол-во IP-адресов, не имеющих ни одного байта с нечет. значением.	67	2025-04-20 18:06:32.296422	7
293	(Демо-2021). Системный администратор раз в неделю создает архив пользовательских файлов. Однако объем диска, куда он помещает архив, может быть меньше, чем суммарный объем архивируемых файлов. Известно, какой объем занимает файл каждого пользователя. По заданной информации об объеме файлов пользователей и свободном объеме на архивном диске определите максимальное число пользователей, чьи файлы можно сохранить в архиве, а также максимальный размер имеющегося файла, который может быть сохранен в архиве, при условии, что сохранены файлы максимально возможного числа пользователей.\r\nВходные данные. В первой строке входного файла 26-5.txt находятся два числа: S ­ размер свободного места на диске (натуральное число, не превышающее 100000) и N ­ количество пользователей (натуральное число, не превышающее 10000). В следующих N строках находятся значения объемов файлов каждого пользователя (все числа натуральные, не превышающие 100), каждое в отдельной строке.\r\nЗапишите в ответе два числа: сначала наибольшее число пользователей, чьи файлы могут быть помещены в архив, затем максимальный размер имеющегося файла, который может быть сохранен в архиве, при условии, что сохранены файлы максимально возможного числа пользователей.\r\nПример входного файла:\r\n100 4\r\n80\r\n30\r\n50\r\n40\r\nПри таких исходных данных можно сохранить файлы максимум двух пользователей. Возможные объемы этих двух файлов 30 и 40, 30 и 50 или 40 и 50. Наибольший объем файла из перечисленных пар 50, поэтому ответ для приведенного примера: 2 50	89	2025-04-15 20:22:22.002906	1
294	Если нам нужно решить подобную задачу, но на диск нужно записывать файлы, разница между размерами которых не меньше двух.	89	2025-04-15 20:22:49.518234	1
295	Если нужно сгруппировать файлы пользователей по последней цифре их размера.	89	2025-04-15 20:22:58.252282	1
296	Предположим, что у нас есть 10 дисков. Объем каждого диска - 100 ед. На диски нужно записать как можно больше файлов. Чтобы записать максимальное количество файлов, нужно одновременно заполнять все диски (а не все маленькие файлы на первом, все большие на втором).	89	2025-04-15 20:23:05.403037	1
297	Магазин предоставляет оптовому покупателю скидку по следующим правилам:\r\nна каждый второй товар ценой больше 100 рублей предоставляется скидка 10%;\r\nобщая цена покупки со скидкой округляется вверх до целого числа рублей;\r\nпорядок товаров в списке определяет магазин и делает это так, чтобы общая сумма скидки была наименьшей. \r\nВам необходимо определить общую цену закупки с учетом скидки и цену самого дорогого товара, на который будет предоставлена скидка. \r\nВходные данные. Первая строка входного файла 26-s1.txt содержит число N ­ общее количество купленных товаров. Каждая из следующих N строк содержит одно целое число ­ цену товара в рублях. В ответе запишите два целых числа: сначала общую цену покупки с учетом скидки, затем цену самого дорогого товара, на который предоставлена скидка. \r\nПример входного файла: \r\n7 \r\n225 \r\n160 \r\n380 \r\n95 \r\n192 \r\n310 \r\n60 \r\nВ данном случае товары с ценой 60 и 95 не участвуют в определении скидки, остальные товары магазину выгодно расположить в таком порядке цен: 380, 160, 225, 192, 310. Скидка предоставляется на товары ценой 160 и 192. Суммарная цена этих двух товаров со скидкой составит 316,8 руб., после округления 317 руб. Общая цена покупки составит: 60 + 95 + 317 + 380 + 225 + 310 = 1387 руб. Самый дорогой товар, на который будет получена скидка, стоит 192 руб. В ответе нужно записать числа 1387 и 192.	89	2025-04-15 20:23:58.45039	1
298	(Досрочный ЕГЭ-2022) В лесополосе осуществляется посадка деревьев: саженцы высаживают рядами на одинаковом расстоянии. Спустя некоторое время с помощью аэросъемки выясняют, какие саженцы прижились. Необходимо определить ряд с максимальным номером, в котором есть подряд ровно К неприжившихся саженцев при условии, что справа и слева от них саженцы прижились.\r\nВ ответе запишите сначала наибольший номер ряда, затем наименьший номер неприжившегося саженца.\r\nВходные данные представлены в файле 26-79.txt следующим образом. В первой строке записаны два числа: N ­ количество занятых мест (натуральное число, не превышающее 10 000) и К ­ длина цепочки неприжившихся саженцев, которую нужно найти. Каждая из следующих N строк содержит сведения об одном прижившемся саженце ­ два натуральных числа, не превышающих 100000: номер ряда и номер саженца в ряду.\r\nПример входного файла:\r\n6 3\r\n40 30\r\n40 34\r\n50 125\r\n50 129\r\n50 64\r\n50 68\r\nВ примере требуется найти 3 подряд идущих неприжившихся саженца. Ответ: 50 65\r\n	89	2025-04-15 20:24:22.769075	1
299	Входной файл содержит сведения о заявках на проведение занятий в конференц-зале. В каждой заявке указаны время начала и время окончания мероприятия (в минутах от начала суток). Если время проведения двух или более мероприятий пересекается, то провести можно не более одного из них. Между окончанием одного мероприятия и началом следующего необходим перерыв не менее 10 минут. Определите максимальное количество мероприятий, которое можно провести в конференц-зале, и максимальный перерыв между двумя последними мероприятиями.\r\nВходные данные представлены в файле 26-142.txt следующим образом. Первая строка входного файла содержит натуральное число N (1≤N≤1000) ­ количество заявок на проведение мероприятий. Следующие N строк содержат пары чисел, обозначающих время начала и время окончания мероприятий. Каждое из чисел ­ натуральное, не превосходящее 1440.\r\nЗапишите в ответе два числа: максимальное количество мероприятий, которые можно провести в конференц-зале, и максимальный перерыв между последними мероприятиями (в минутах).	90	2025-04-15 20:25:15.254972	1
300	(Досрочный ЕГЭ-2023) Входной файл содержит заявки пассажиров, желающих сдать свой багаж в камеру хранения. В заявке указаны время сдачи багажа и время освобождения ячейки (в минутах от начала суток). Багаж одного пассажира размещается в одной свободной ячейке с минимальным номером. Ячейки пронумерованы начиная с единицы. Размещение багажа в ячейке или ее освобождение происходит в течение 1 мин. Багаж можно поместить в только что освобожденную ячейку начиная со следующей минуты. Если в момент сдачи багажа свободных ячеек нет, то пассажир уходит. Определите, сколько пассажиров сможет сдать свой багаж в течение 24 ч и какой номер будет иметь ячейка, которую займут последней. Если таких ячеек несколько, укажите минимальный номер ячейки.\r\nВходные данные представлены в файле 26-111.txt следующим образом. В первой строке входного файла находится натуральное число К, не превышающее 1000, ­ количество ячеек в камере хранения. Во второй строке ­ натуральное число N (N≤1000), обозначающее количество пассажиров. Каждая из следующих N строк содержит два натуральных числа, каждое из которых не превышает 1440: указанное в заявке время размещения багажа в ячейке и время освобождения ячейки (в минутах от начала суток).	90	2025-04-15 20:25:30.02467	1
301	(ЕГЭ-2023) На производстве штучных изделий N деталей должны быть отшлифованы и окрашены. Для каждой детали известно время ее шлифовки и время окрашивания. Детали пронумерованы начиная с единицы. Параллельная обработка деталей не предусмотрена. На ленте транспортера имеется M мест для каждой из N деталей. На ленте транспортера детали располагают по следующему алгоритму:\r\nвсе 2×N чисел, обозначающих время окрашивания и шлифовки для N деталей, упорядочивают по возрастанию;\r\nесли минимальное число в этом упорядоченном списке ­ это время шлифовки конкретной детали, то деталь размещают на ленте транспортера на первое свободное место от ее начала;\r\nесли минимальное число ­ это время окрашивания, то деталь размещают на первое свободное место от конца ленты транспортера;\r\nесли число обозначает время окрашивания или шлифовки уже рассмотренной детали, то его не принимают во внимание. Этот алгоритм применяется последовательно для размещения всех N деталей. \r\nОпределите номер последней детали, для которой будет определено ее место на ленте транспортера, и количество деталей, которые будут отшлифованы до нее. \r\nВходные данные представлены в файле 26-129.txt следующим образом. Первая строка входного файла содержит натуральное число N (1≤N≤1000) ­ количество деталей. Следующие N строк содержат пары чисел, обозначающих соответственно время шлифовки и время окрашивания конкретной детали (все числа натуральные, различные). \r\nЗапишите в ответе два натуральных числа: сначала номер последней детали, для которой будет определено ее место на ленте транспортера, затем количество деталей, которые будут отшлифованы до нее.	90	2025-04-15 20:26:18.58542	1
302	(ЕГЭ-2024) При онлайн-покупке билета на концерт известно, какие места в зале уже заняты. Необходимо купить два билета на такие соседние места в одном ряду, чтобы перед ними все кресла с такими же номерами были свободны, а ряд находился как можно дальше от сцены. Если в этом ряду таких пар мест несколько, найдите пару с наибольшими номерами мест. Нумерация рядов и мест ведётся с 1. Гарантируется, что хотя бы одна такая пара в зале есть. Определите наибольший номер ряда и наибольший номер места для найденной пары мест.\r\nВходные данные представлены в файле 26-150.txt следующим образом. В первой строке входного файла находятся три числа: N ­ количество занятых мест в зале (целое положительное число, не превышающее 10000), М ­ количество рядов (целое положительное число, не превышающее 100 000) и К ­ количество мест в каждом ряду (целое положительное число, не превышающее 100 000). В следующих N строках находятся пары натуральных чисел: номер ряда и номер места занятого кресла соответственно (первое число не превышает значения М, а второе К).\r\nПример входного файла:\r\n7 7 8\r\n1 1\r\n6 6\r\n5 5\r\n6 7\r\n4 4\r\n2 2\r\n3 3\r\nУсловию задачи удовлетворяют места 7 и 8 в ряду 5: перед креслами 7 и 8 нет занятых мест.\r\nЗапишите в ответе два целых числа: искомый номер ряда и наибольший номер места в найденной паре.	91	2025-04-15 20:27:33.578788	1
303	Во время сессии студенты сдают 4 экзамена, за каждый из которых можно по­лучить от 2 до 5 баллов. Студенты, получившие хотя бы одну «двойку», считаются не сдавшими сессию. Результаты сессии публикуются в виде рейтингового списка, в котором сначала указаны идентификационные номера студентов (ID), сдавших сес­сию, в порядке убывания среднего балла за сессию, а в случае равенства средних баллов в порядке возрастания ID. Затем располагаются ID студентов, не сдавших сессию: сначала получивших одну «двойку», затем две «двойки», потом ID сту­дентов с тремя «двойками» и, наконец, ID студентов, получивших по 2 балла за каждый из экзаменов. Если студенты имеют одинаковое количество «двоек», то их ID в рейтинге располагаются в порядке возрастания. Повышенную стипендию по­лучают студенты, занявшие в рейтинговом списке первые 25% мест, при условии отсутствия у них «двоек». Гарантируется, что без «двоек» сессию сдали не менее 25% студентов. Найдите ID студента, который занимает последнее место среди сту­дентов с повышенной стипендией, а также ID первого в рейтинговом списке студента, который имеет более двух «двоек». В ответе запишите два целых положительных числа: сначала ID студента, который занимает последнее место среди студентов с повышенной стипендией, затем ID первого в рейтинговом списке студента, который имеет более двух «двоек».\r\nВходные данные\r\nВ первой строке входного файла находится число N, обозначающее количество студентов (целое положительное число, не превышающее 10 000). Каждая из следу­ющих N строк содержит 5 чисел через пробел: ID студента (целое положительное число, не превышающее 100 000) и четыре оценки, полученные им за сессию. Гаран­тируется, что общее число студентов N кратно 4 и хотя бы один студент имеет более двух «двоек». Во входном файле все ID различны.\r\nВыходные данные\r\nДва натуральных числа: искомые ID студентов в порядке, указанном в условии задачи.\r\nТиповой пример организации данных во входном файле\r\n8\r\n10 3 4 4 5\r\n4 4 4 4 4\r\n1 4 4 4 3\r\n6 3 5 5 3\r\n7 5 5 5 2\r\n2 2 2 2 2\r\n13 2 2 2 3\r\n3 3 3 3 3	92	2025-04-15 20:29:23.049099	1
304	(ЕГЭ-2024) При онлайн-покупке билета на концерт известно, какие места в зале уже заняты. Необходимо купить два билета на такие соседние места в одном ряду, чтобы перед ними все кресла с такими же номерами были свободны, а ряд находился как можно дальше от сцены. Если в этом ряду таких пар мест несколько, найдите пару с наибольшими номерами мест. Нумерация рядов и мест ведётся с 1. Гарантируется, что хотя бы одна такая пара в зале есть. Определите наибольший номер ряда и наибольший номер места для найденной пары мест.\r\nВходные данные представлены в файле 26-150.txt следующим образом. В первой строке входного файла находятся три числа: N ­ количество занятых мест в зале (целое положительное число, не превышающее 10 000), М ­ количество рядов (целое положительное число, не превышающее 100 000) и К ­ количество мест в каждом ряду (целое положительное число, не превышающее 100 000). В следующих N стро­ках находятся пары натуральных чисел: номер ряда и номер места занятого кресла соответственно (первое число не превышает значения М, а второе - К).\r\nПример входного файла:\r\n7 7 8\r\n1 1\r\n6 6\r\n5 5\r\n6 7\r\n4 4\r\n2 2\r\n3 3\r\nУсловию задачи удовлетворяют места 7 и 8 в ряду 5: перед креслами 7 и 8 нет занятых мест и это последняя из двух возможных пар в этом ряду. В рядах 6 и 7 искомую пару найти нельзя. Ответ: 5 8.\r\nЗапишите в ответе два целых числа: искомый номер ряда и наибольший номер места в найденной паре.	92	2025-04-15 20:29:50.924561	1
305	Входной файл содержит заявки пассажиров, желающих сдать свой багаж в камеру хранения. В заявке указаны время сдачи багажа и время освобождения ячейки (в минутах от начала суток). Багаж одного пассажира размещается в одной свободной ячейке с минимальным номером. Ячейки пронумерованы начиная с единицы. Размещение багажа в ячейке или её освобождение происходит в течение 1 мин. Багаж можно поместить в только что освобожденную ячейку начиная со следующей минуты. Если в момент сдачи багажа свободных ячеек нет, то пассажир уходит.\r\nВходные данные представлены в файле 26-111.txt. В первой строке входного файла находится натуральное число К, не превышающее 1000, ­ количество ячеек в камере хранения. Во второй строке ­ натуральное число N (N ≤ 1000), обозначающее количество пассажиров. Каждая из следующих N строк содержит два натуральных числа, каждое из которых не превышает 1440: указанное в заявке время размещения багажа в ячейке и время освобождения ячейки (в минутах от начала суток).\r\nОпределите максимальную нечетную сумму двух промежутков времени, в течение которого багаж какого-либо пассажира находился в камере хранения.	93	2025-04-15 20:32:17.169481	1
306	Для задачи из примера 1 определите максимальную сумму двух времен сдачи багажа, кратную 60.	93	2025-04-15 20:32:26.773914	1
307	(Досрочный ЕГЭ-2022) В лесополосе осуществляется посадка деревьев: саженцы высаживают рядами на одинаковом расстоянии. Спустя некоторое время с помощью аэросъемки выясняют, какие саженцы прижились. Необходимо определить ряд с максимальным номером, в котором есть подряд ровно K неприжившихся саженцев при условии, что справа и слева от них саженцы прижились.\r\nВходные данные представлены в файле 26-79.txt следующим образом. . В первой строке записаны два числа: N – количество занятых мест (натуральное число, не превышающее 10 000) и K – длина цепочки неприжившихся саженцев, которую нужно найти. Каждая из следующих N строк содержит сведения об одном прижившемся саженце – два натуральных числа, не превышающих 100 000: номер ряда и номер саженца в ряду.\r\nВ ответе запишите сначала наибольший номер ряда, затем наименьший номер неприжившегося саженца.\r\nПример входного файла:\r\n6 3\r\n40 30 \r\n40 34 \r\n50 125 \r\n50 129 \r\n50 64 \r\n50 68\r\nВ примере требуется найти 3 подряд идущих неприжившихся саженца. Ответ: 50 65.	94	2025-04-15 20:33:57.428117	1
639	Проверить, является ли число двузначным и четным	191	2025-07-06 11:43:38.676794	11
308	На складе требуется разместить N контейнеров различного размера, каждый из которых имеет форму куба. Чтобы сэкономить место, контейнеры вкладывают друг в друга. Один контейнер можно вложить в другой, если размер стороны внешнего контейнера превышает размер стороны внутреннего на K и более условных единиц. Группу вложенных друг в друга контейнеров называют блоком. Количество контейнеров в блоке может быть любым. Каждый блок, независимо от количества и размера входящих в него контейнеров, а также каждый одиночный контейнер, не входящий в блоки, занимает при хранении одну складскую ячейку.\r\nОпределите минимальное количество ячеек, которые потребуются для хранения всех контейнеров, и максимальное количество контейнеров в одном блоке.\r\nВходные данные представлены в файле 26-101.txt следующим образом. В первой строке входного файла записано число N – количество контейнеров (натуральное число, не превышающее 20 000) и число K (1 ≤ K ≤ 1000) – наименьшая допустимая разница размеров вложенных соседних контейнеров. Каждая из следующих N строк содержит одно натуральное число, не превышающее 10000 – длину стороны очередного контейнера.\r\nПример входного файла:\r\n7 9\r\n2\r\n18\r\n47\r\n16\r\n38\r\n55\r\n48\r\nДля таких контейнеров можно составить три блока, удовлетворяющих условию: (55, 38, 18, 2), (48, 16) и (47). Наибольшее количество контейнеров – в первом блоке – 4. Ответ: 3 4.	94	2025-04-15 20:34:21.099324	1
309	На складе требуется разместить N контейнеров различного размера, каждый из которых имеет форму куба. Контейнеры имеют разные цвета, которые обозначаются латинскими буквами. Чтобы сэкономить место, контейнеры вкладывают друг в друга. Один контейнер можно вложить в другой, если а) размер стороны внешнего контейнера превышает размер стороны внутреннего на K и более условных единиц и б) цвета внешнего и внутреннего контейнеров различны. Группу вложенных друг в друга контейнеров называют блоком. Количество контейнеров в блоке может быть любым. Каждый блок, независимо от количества и размера входящих в него контейнеров, а также каждый одиночный контейнер, не входящий в блоки, занимает при хранении одну складскую ячейку. Блоки составляют следующим образом. Сначала выбирают наибольший контейнер. Затем вкладывают в него наибольший подходящий контейнер. Если таких контейнеров несколько, выбирают контейнер с наименьшим кодом цвета. Этот алгоритм повторяется, пока есть подходящие контейнеры. Затем так же составляется следующий блок и т. д.\r\nОпределите количество ячеек, которые потребуются для хранения всех контейнеров, и максимальное количество контейнеров в одном блоке.\r\nВходные данные представлены в файле 26-102.txt следующим образом. В первой строке входного файла записано число N – количество контейнеров (натуральное число, не превышающее 20 000) и число K (1 ≤ K ≤ 1000) – наименьшая допустимая разница размеров вложенных соседних контейнеров. Каждая из следующих N строк содержит натуральное число, не превышающее 10000 – длину стороны очередного контейнера, и латинскую букву, обозначающую цвет этого контейнера.\r\nПример входного файла:\r\n7 5\r\n2 A\r\n18 B\r\n47 A\r\n16 B\r\n38 A\r\n55 A\r\n48 B\r\nДля такого набора контейнеров можно составить два блока, удовлетворяющих условию: (55, 48, 38, 18, 2), (47, 16). Наибольшее количество контейнеров – в первом блоке – 5. Ответ: 2 5.	94	2025-04-15 20:34:40.968037	1
310	На закупку товаров типов Q и Z выделена определённая сумма денег. Эти товары есть в продаже по различной цене. Необходимо на выделенную сумму закупить как можно больше товаров двух типов (по общему количеству). Если можно разными способами купить максимальное количество двух товаров, то нужно выбрать способ, при котором будет закуплено как можно больше товаров типа Q. Если при этих условиях есть несколько способов закупки, нужно потратить как можно меньше денег.\r\nОпределите, сколько будет закуплено товаров типа Q и сколько денег останется.\r\nВходные данные представлены в файле 26-62.txt следующим образом. Первая строка входного файла содержит два целых числа: N – общее количество товаров и M – сумма выделенных на закупку денег (в рублях). Каждая из следующих N строк содержит целое число (цена товара в рублях) и символ (латинская буква Q или Z), определяющий тип товара. Все данные в строках входного файла отделены одним пробелом.\r\nЗапишите в ответе два числа: сначала количество закупленных товаров типа Q, затем оставшуюся неиспользованной сумму денег.\r\nПример входного файла:\r\n6 110\r\n40 Z\r\n50 Q\r\n50 Z\r\n30 Z\r\n20 Q\r\n10 Z\r\nВ данном случае можно купить не более четырёх товаров, из них не более двух товаров типа Q. Минимальная цена такой покупки 110 рублей (покупаем товары 10 Z, 20 Q, 30 Z, 50 Q). Останется 0 рублей. Ответ: 2 0.	95	2025-04-15 20:35:50.442575	1
311	Магазин предоставляет оптовому покупателю скидку по следующим правилам:\r\n− на каждый второй товар ценой больше 100 рублей предоставляется скидка 10%;\r\n− общая цена покупки со скидкой округляется вверх до целого числа рублей;\r\n− порядок товаров в списке определяет магазин и делает это так, чтобы общая сумма скидки была наименьшей.\r\nВам необходимо определить общую цену закупки с учётом скидки и цену самого дорогого товара, на который будет предоставлена скидка.\r\nВходные данные. Первая строка входного файла 26-s1.txt содержит число N – общее количество купленных товаров. Каждая из следующих N строк содержит одно целое число – цену товара в рублях. В ответе запишите два целых числа: сначала общую цену покупки с учётом скидки, затем цену самого дорогого товара, на который предоставлена скидка.\r\nПример входного файла\r\n7\r\n225\r\n160\r\n380\r\n95\r\n192\r\n310\r\n60\r\nВ данном случае товары с ценой 60 и 95 не участвуют в определении скидки, остальные товары магазину выгодно расположить в таком порядке цен: 380, 160, 225, 192, 310. Скидка предоставляется на товары ценой 160 и 192. Суммарная цена этих двух товаров со скидкой составит 316,8 руб., после округления – 317 руб. Общая цена покупки составит: 60 + 95 + 317 + 380 + 225 + 310 = 1387 руб. Самый дорогой товар, на который будет получена скидка, стоит 192 руб. В ответе нужно записать числа 1387 и 192.	95	2025-04-15 20:36:18.400537	1
312	(Досрочный ЕГЭ-2023) Входной файл содержит заявки пассажиров, желающих сдать свой багаж в камеру хранения. В заявке указаны время сдачи багажа и время освобождения ячейки (в минутах от начала суток). Багаж одного пассажира размещается в одной свободной ячейке с минимальным номером. Ячейки пронумерованы начиная с единицы. Размещение багажа в ячейке или её освобождение происходит в течение 1 мин. Багаж можно поместить в только что освобождённую ячейку начиная со следующей минуты. Если в момент сдачи багажа свободных ячеек нет, то пассажир уходит. Определите, сколько пассажиров сможет сдать свой багаж в течение 24 часов и какой номер будет иметь ячейка, которую займут последней. Если таких ячеек несколько, укажите минимальный номер ячейки.\r\nВходные данные представлены в файле 26-111.txt следующим образом. В первой строке входного файла находится натуральное число K, не превышающее 1000, – количество ячеек в камере хранения. Во второй строке – натуральное число N (N ≤ 1000), обозначающее количество пассажиров. Каждая из следующих N строк содержит два натуральных числа, каждое из которых не превышает 1440: указанное в заявке время размещения багажа в ячейке и время освобождения ячейки (в минутах от начала суток).\r\nЗапишите в ответе два числа: количество пассажиров, которые смогут воспользоваться камерой хранения, и номер последней занятой ячейки.\r\nПример входного файла:\r\n2\r\n5\r\n30 60\r\n40 1000\r\n59 60\r\n61 1000\r\n1010 1440\r\nПри таких исходных данных положить вещи в камеру хранения смогут первый, второй, четвёртый и пятый пассажиры. Последний пассажир положит вещи в ячейку 1, так как ячейки 1 и 2 будут свободны. Ответ: 4 1.	96	2025-04-15 20:37:25.245787	1
313	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд ­ это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой Н и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров.\r\nИстинный центр кластера, или центроид, ­ это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле:\r\nd(A,B) = √((x2-x1)² + (y2-y1)²)\r\nВ файле А хранятся данные о звёздах двух кластеров, где H=3, W=3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата х, затем координата у. Значения даны в условных единицах. Известно, что количество звёзд не превышает 1000.\r\nВ файле Б хранятся данные о звёздах трёх кластеров, где H=3, W=3 для каждого кластера. Известно, что количество звёзд не превышает 10 000. Структура хранения информации о звездах в файле Б аналогична файлу А.\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px: среднее арифметическое абсцисс центров кластеров, и Py ­ среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа: в первой строке сначала целую часть произведения Px * 10000, затем целую часть произведения Py * 10000 для файла А, во второй строке ­ аналогичные данные для файла Б.\r\n	103	2025-04-15 20:48:30.629505	1
345	Дана последовательность, которая состоит из троек натуральных чисел. Необходимо распределить все числа на три группы, при этом в каждую группу должно попасть ровно одно число из каждой исходной тройки. Сумма всех чисел как в первой, так и во второй группе должна быть четной. Определите максимально возможную сумму всех чисел в третьей группе.	112	2025-04-16 10:11:20.394039	1
314	Ученый решил провести кластеризацию некоторого множества звезд по их расположению на карте звездного неба. Кластер звезд ­ это набор звезд (точек) на графике, лежащий внутри прямоугольника высотой Н и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров.\r\nИстинный центр кластера, или центроид, это одна из звезд на графике, сумма расстояний от которой до всех остальных звезд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле:\r\nd(A,B) = √((x2-x1)² + (y2-y1)²)\r\nВ файле А хранятся данные о звездах двух кластеров, где H=3 W=3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата х, затем координата у. Значения даны в условных единицах. Известно, что количество звезд не превышает 1000.\r\nВ файле Б хранятся данные о звездах трех кластеров, где H=3, W=3 для каждого кластера. Известно, что количество звезд не превышает 10 000. Структура хранения информации о звездах в файле Б аналогична файлу А.\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px ­ среднее арифметическое абсцисс центров кластеров, и Py ­ среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа: в первой строке сначала целую часть произведения Px * 10000, затем целую часть произведения Py * 10000 для файла А, во второй строке аналогичные данные для файла Б.	104	2025-04-15 20:50:35.632469	1
315	По каналу связи передаются положительные целые числа, не превышающие 1000, — результаты измерений, полученных в ходе эксперимента (количество измерений известно заранее). После окончания эксперимента передаётся контрольное значение — наибольшее число R, удовлетворяющее следующим условиям:\r\n1) R — сумма двух различных переданных элементов последовательности («различные» означает, что нельзя просто удваивать переданные числа, суммы различных, но равных по величине элементов допускаются);\r\n2) R — нечётное число.\r\nНа вход программе в первой строке подаётся количество чисел N. В каждой из последующих N строк записано одно натуральное число, не превышающее 1000. В последней строке записано контрольное значение.\r\nПример входных данных:\r\n  6\r\n  100\r\n  8\r\n  33\r\n  45\r\n  19\r\n  90\r\nПример выходных данных для приведенного выше примера входных данных: Вычисленное контрольное значение: 145	97	2025-04-15 20:58:34.948618	1
316	Пусть R ­четное число. Найдите наибольшее такое R.\r\n	97	2025-04-15 20:58:41.643296	1
317	Пусть R ­– произведение двух различных элементов и R кратно 26. Найдите наибольшее такое R.	97	2025-04-15 20:58:52.274297	1
318	Пусть R - сумма двух различных элементов и R кратна 7. Найдите наибольшее такое R.	97	2025-04-15 20:59:01.729036	1
319	(В.Н. Бабий, Челябинск) На вход программы поступает последовательность из N натуральных чисел. Рассматриваются все пары различных элементов последовательности (элементы пары не обязательно должны стоять в последовательности рядом, порядок в паре неважен). Необходимо определить количество пар, для которых произведение элементов заканчивается на 3.\r\nОписание входных и выходных данных\r\nВ первой строке входных данных задается количество чисел N (7 ≤ N ≤ 10000). В каждой из последующих N строк записано одно целое положительное число, не превышающее 1000. В качестве ответа программа должна вывести одно число: количество пар, в которых произведение элементов заканчивается на 3, а номера чисел в последовательности отличаются не менее, чем на 6.\r\nПример входных данных:\r\n  10\r\n  17\r\n  11\r\n  15\r\n  24\r\n  36	98	2025-04-16 09:37:56.757066	1
320	(Д.В. Богданов) Дан набор из N натуральных чисел. Необходимо определить количество пар элементов (ai, aj) этого набора, в которых 1 < i < j < N и произведение элементов кратно 6. Напишите эффективную по времени и по памяти программу для решения этой задачи.\r\nОписание входных и выходных данных\r\nВ первой строке входных данных задается количество чисел N (1 ≤ N ≤ 10000). В каждой из последующих N строк записано одно натуральное число, не превышающее 1000.	98	2025-04-16 09:38:46.321363	1
321	Дан набор из N натуральных чисел. Необходимо определить количество троек элементов (ai, aj, ak) этого набора, в которых 1 < i < j < k < N и произведение элементов кратно 5. Напишите эффективную по времени и по памяти программу для решения этой задачи.\r\nОписание входных и выходных данных\r\nВ первой строке входных данных задается количество чисел N (1 ≤ N ≤ 10000). В каждой из последующих N строк записано одно натуральное число, не превышающее 1000.	98	2025-04-16 09:39:33.572422	1
322	(Статград, 29.04.2020) Дана последовательность N целых положительных чисел. Необходимо определить количество пар элементов этой последовательности, разность которых делится на m = 60.\r\nВходные данные:\r\nВ первой строке записано натуральное число N (2 ≤ N ≤ 10000) – количество чисел в последовательности. В следующих N строках записаны числа, входящие в последовательность, по одному в каждой строке.	98	2025-04-16 09:40:04.190684	1
323	Есть болото, на болоте есть 10 кочек. На первой кочке сидит кузнечик. Кузнечик умеет прыгать между кочками. Он может прыгать либо вперед на соседнюю кочку, либо через нее, прыгать назад нельзя.\r\nСколько у кузнечика есть есть способов допрыгать с первой кочки на последнюю?	99	2025-04-16 09:40:47.963395	1
568	№7. Определить минимальный объем памяти для хранения изображений.	172	2025-05-10 19:45:26.785386	7
324	По каналу связи передаются положительные целые числа, не превышающие 1000, – результаты измерений, полученных в ходе эксперимента (количество измерений известно заранее). После окончания эксперимента передаётся контрольное значение – наибольшее число R, удовлетворяющее следующим условиям:\r\n1) R – сумма двух различных переданных элементов последовательности («различные» означает, что нельзя просто удваивать переданные числа, суммы различных, но равных по величине элементов допускаются);\r\n2) R – четно.\r\nНа вход программе в первой строке подаётся количество чисел N. В каждой из последующих N строк записано одно натуральное число, не превышающее 1000. В последней строке записано контрольное значение.\r\nПример входных данных: \r\n6\r\n100\r\n8\r\n33 \r\n45 \r\n19 \r\n90	99	2025-04-16 09:41:42.206415	1
325	Отредактируем условие прошлой задачи:\r\n1) R – произведение двух различных переданных элементов последовательности; \r\n2) R – кратно 6.	99	2025-04-16 09:42:17.482703	1
326	Отредактируем условие прошлой задачи:\r\n1) R – сумма двух различных переданных элементов последовательности;\r\n2) R – кратно 60	99	2025-04-16 09:42:42.893208	1
327	(Д.В. Богданов) Дан набор из N натуральных чисел. Необходимо определить количество пар элементов (ai, aj) этого набора, в которых 1 < i < j < N и произведение элементов кратно 6. Напишите эффективную по времени и по памяти программу для решения этой задачи.\r\nОписание входных и выходных данных\r\nВ первой строке входных данных задаётся количество чисел N(1 ≤ N ≤ 10000). В каждой из последующих N строк записано одно натуральное число, не превышающее 1000.\r\nПример входных данных:\r\n4\r\n7\r\n5\r\n6\r\n12\r\nПример выходных данных для приведённого выше примера входных данных:\r\n5\r\nВ приведённом наборе из 4 чисел имеются пять пар (7, 6), (5, 6), (7, 12), (5, 12), (6, 12), произведение элементов которых кратно 6.	100	2025-04-16 09:43:49.022689	1
328	(Досрочный ЕГЭ 2020 г.) Дана последовательность N целых положительных чисел. Рассматриваются все пары элементов последовательности, разность которых четна, и в этих парах, по крайней мере, одно из чисел пары делится на 17. Порядок элементов в паре неважен. Среди всех таких пар нужно найти и вывести пару с максимальной суммой элементов. Если одинаковую максимальную сумму имеет несколько пар, можно вывести любую из них. Если подходящих пар в последовательности нет, нужно вывести два нуля.\r\nОписание входных и выходных данных\r\nВ первой строке входных данных задаётся количество чисел N (2 ≤ N ≤ 10000). В каждой из последующих N строк записано одно натуральное число, не превышающее 10 000.\r\nПример входных данных:\r\n5\r\n34\r\n12\r\n51\r\n52\r\n51\r\nПример выходных данных для приведённого выше примера входных данных:\r\n51 51\r\nПояснение: Из данных пяти чисел можно составить три различные пары, удовлетворяющих условию: (34, 12), (34, 52), (51, 51). Наибольшая сумма получается в паре (51, 51). Эта пара допускается, так как число 51 встречается в исходной последовательности дважды.\r\nРазность пары будет четна, если из четного числа вычесть четное, или из нечетного – нечетное.	100	2025-04-16 09:44:54.57778	1
329	(Досрочный ЕГЭ 2018 г.) На вход программы поступает последовательность из N целых положительных чисел, все числа в последовательности различны. Рассматриваются все пары различных элементов последовательности (элементы пары не обязаны стоять в последовательности рядом, порядок элементов в паре неважен). Необходимо определить количество пар, для которых произведение элементов не кратно 14.\r\nОписание входных и выходных данных\r\nВ первой строке входных данных задаётся количество чисел N (1 ≤ N ≤ 1000). В каждой из последующих N строк записано одно натуральное число, не превышающее 10000. В качестве результата программа должна вывести одно число: количество пар, в которых произведение элементов не кратно 14.	100	2025-04-16 09:45:29.390689	1
330	На спутнике «Восход» установлен прибор, предназначенный для измерения солнечной активности. Каждую минуту прибор передаёт по каналу связи неотрицательное целое число – количество энергии солнечного излучения, полученной за последнюю минуту, измеренное в условных единицах. Временем, в течение которого происходит передача, можно пренебречь. Необходимо найти в заданной серии показаний прибора минимальное нечётное произведение двух показаний, между моментами передачи которых прошло не менее 6 минут. Если получить такое произведение не удаётся, ответ считается равным −1. Количество энергии, получаемое прибором за минуту, не превышает 1000 условных единиц. Общее количество показаний прибора в серии не превышает 10000.	101	2025-04-16 09:46:27.488231	1
331	(В.Н. Бабий, Челябинск) На вход программы поступает последовательность из N натуральных чисел. Рассматриваются все пары различных элементов последовательности (элементы пары не обязательно должны стоять в последовательности рядом, порядок в паре неважен). Необходимо определить количество пар, для которых произведение элементов заканчивается на 3, а номера чисел в последовательности отличаются не менее, чем на 6.\r\n	101	2025-04-16 09:46:55.340241	1
383	№13 Сколько в заданной сети IP-адресов, для которых сумма единиц в двоичной записи IP-адреса не кратна 2?	76	2025-04-20 18:02:23.423249	7
332	На спутнике «Восход» установлен прибор, предназначенный для измерения солнечной активности. Каждую минуту прибор передает по каналу связи неотрицательное целое число – количество энергии солнечного излучения, полученной за последнюю минуту, измеренное в условных единицах. Временем, в течение которого происходит передача, можно пренебречь. Необходимо найти в заданной серии показаний прибора минимальное четное произведение двух показаний, между моментами передачи которых прошло не менее 6 минут. Если получить такое произведение не удается, ответ считается равным −1. Количество энергии, получаемое прибором за минуту, не превышает 1000 условных единиц. Общее количество показаний прибора в серии не превышает 10000.	102	2025-04-16 09:47:34.902732	1
333	(ЕГЭ-2023) По каналу связи передается последовательность целых чисел - показания прибора. В течение N минут (N – натуральное число) прибор ежеминутно регистрирует значение силы тока (в условных единицах) в электрической сети и передает его на сервер. Определите три таких переданных числа, чтобы между моментами передачи любых двух из них прошло не менее K минут, а сумма этих чисел была минимально возможной. Запишите в ответе найденную сумму.\r\nВходные данные: Дан входной файл B (27-165b.txt), который в первой строке содержит натуральное число N (1 < N ≤ 10000000) – количество переданных показаний, и натуральное число K (K < N) – минимальное количество минут, которое должно пройти между моментами передачами любых двух из трех показаний. В каждой из следующих N строк находится одно натуральное число, не превышающее 10000000, которое обозначает значение силы тока в соответствующую минуту.\r\nПример входного файла:\r\n62\r\n15\r\n14\r\n20\r\n23\r\n21\r\n10\r\nПри таких исходных данных искомая величина равна 45 – это сумма значений, зафиксированных на первой, третьей и шестой минутах измерений. Ответ: 45.	102	2025-04-16 09:48:08.511311	1
334	(Информатик-БУ) Используя входной файл 27-13b.txt, найти количество пар, разность которых кратна 120 и хотя бы один элемент больше 50. Расстояние между парами равно 6.	102	2025-04-16 09:48:32.882503	1
335	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба, а также по блеску звезды. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда, подходящая под заданный уровень блеска, обязательно принадлежит только одному из кластеров. Остальные звёзды не относятся к рассматриваемым кластерам. Истинный центр кластера, или центроид, – это одна из звёзд кластера, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле: \r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2). \r\nВ файле А хранятся данные о звёздах двух кластеров, где H = 5, W = 5, для каждого кластера, а звёзды обладают блеском не более 20 условных единиц. В каждой строке записана информация о расположении на карте одной звезды, а также об её уровне блеска: сначала координата x, затем координата y и наконец уровень блеска m. Значения даны в условных единицах, которые представлены вещественными числами. Известно, что количество звёзд не превышает 2000. В файле Б хранятся данные о звёздах четырёх кластеров, где H = 5, W = 5 для каждого кластера, а звёзды обладают блеском не более 20 условных единиц. Известно, что количество звёзд не превышает 20 000. Структура хранения информации о звездах в файле Б аналогична файлу А. Для каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px — среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа через пробел: сначала целую часть произведения Px × 10000 для файла А и Py × 10000 для файла А, далее целую часть произведения Px × 10000 для файла Б и Py × 10000 для файла Б.	105	2025-04-16 10:08:25.737877	1
336	(А. Жуков) Вам посчастливилось узнать стоимость акций некоторой компании в каждый из ближайших N дней. Какой наибольший доход Вы сможете получить, если за все дни возможны не более одной покупки и не более одной продажи акций. N не превышает 1000. Стоимость акции – натуральное число условных единиц (у.е.), меньшее, чем 10000.	106	2025-04-16 10:08:48.865871	1
337	(А. Жуков) На вход программы подается натуральное число N, а затем N целых чисел. Необходимо determinar максимальную сумму смежных элементов последовательности. N не превышает 1000, каждый элемент последовательности не превосходит по модулю 100.	106	2025-04-16 10:08:53.7493	1
338	(Демо-2022) Дана последовательность из N натуральных чисел. Рассматриваются все её непрерывные подпоследовательности, такие что сумма элементов каждой из них кратна k = 43. Найдите среди них подпоследовательность с максимальной суммой, определите её длину. Если таких подпоследовательностей найдено несколько, в ответе укажите количество элементов самой короткой из них.	106	2025-04-16 10:08:58.855407	1
339	Имеется набор данных, состоящий из пар положительных целых чисел. Необходимо выбрать из каждой пары ровно одно число так, чтобы сумма всех выбранных чисел не делилась на 3 и при этом была минимально возможной. Гарантируется, что искомую сумму получить можно.	107	2025-04-16 10:09:16.489159	1
340	Имеется набор данных, состоящий из троек положительных целых чисел. Необходимо выбрать из каждой тройки ровно одно число так, чтобы сумма всех выбранных чисел не делилась на 8 и при этом была максимально возможной. Гарантируется, что искомую сумму получить можно.	107	2025-04-16 10:09:21.344291	1
346	(Досрочный ЕГЭ-2022) В городе М расположена кольцевая автодорога длиной в N километров с движением в обе стороны. На каждом километре автодороги расположены пункты приема мусора определенной вместимости. В пределах кольцевой дороги в одном из пунктов сборки мусора собираются поставить мусороперерабатывающий завод таким образом, чтобы стоимость доставки мусора была минимальной. Стоимость доставки мусора вычисляется как вместимость пункта сбора, умноженная на расстояние от пункта сбора мусора до мусороперерабатывающего завода. Если мусороперерабатывающий завод находится рядом с пунктом сбора, расстояние считается нулевым. Пункты сбора мусора нумеруются с 1 до N. Рядом с каким пунктом сбора мусора нужно поставить мусороперерабатывающий завод?	111	2025-04-16 10:11:36.982534	1
347	На кольцевой автодороге с двусторонним движением находится N бензоколонок (не более одной бензоколонки на каждом километре дороги). Длина кольцевой автодороги равна K км. Нулевой километр и K-й километр находятся в одной точке. Известно количество топлива, которое ежедневно на каждую бензоколонку доставляет отдельный бензовоз. Для перевозки топлива используются бензовозы вместимостью 25 м³. Стоимость доставки топлива вычисляется как произведение количества рейсов бензовоза на расстояние от нефтехранилища до бензоколонки. Пробег пустого бензовоза не учитывается. Определите минимальные расходы на доставку топлива до всех бензоколонок, если нефтехранилище расположено на кольцевой автодороге на территории одной из бензоколонок.	113	2025-04-16 10:12:05.046195	1
348	(ЕГЭ-2022) У медицинской компании есть N пунктов приёма биоматериалов на анализ. Все пункты расположены вдоль автомагистрали и имеют номера, соответствующие расстоянию от нулевой отметки до конкретного пункта. Известно количество пробирок, которое ежедневно принимают в каждом из пунктов. Пробирки перевозят в специальных транспортировочных контейнерах вместимостью V пробирок. Каждый транспортировочный контейнер упаковывается в пункте приёма и вскрывается только в лаборатории. Компания планирует открыть лабораторию в одном из пунктов. Стоимость перевозки биоматериалов равна произведению расстояния от пункта до лаборатории на количество контейнеров с пробирками. Общая стоимость перевозки за день равна сумме стоимостей перевозок из каждого пункта в лабораторию. Лабораторию расположили в одном из пунктов приёма биоматериалов таким образом, что общая стоимость доставки биоматериалов из всех пунктов минимальна. Определите минимальную общую стоимость доставки биоматериалов из всех пунктов приёма в лабораторию.	113	2025-04-16 10:12:11.700174	1
349	(ЕГЭ-2022) На кольцевой автодороге с двусторонним движением находится N заправочных станций. Длина кольцевой автодороги равна K км, нулевой километр и K-й километр находятся в одной точке. Код заправочной станции совпадает с расстоянием этой станции до нулевой отметки дороги в километрах. На заправочные станции нужно ежедневно доставлять бензин из бензохранилища, которое требуется разместить рядом с одной из заправочных станций. Бензин поставляется в цистернах объемом V м³ каждая, затраты на доставку вычисляются как произведение расстояния на количество поездок бензовоза. За один рейс бензовоз доставляет бензин только на одну заправочную станцию. Бензохранилище расположено так, чтобы суммарные затраты на доставку бензина были минимальными. Определите минимально возможные суммарные затраты на доставку бензина.	114	2025-04-16 10:12:27.572801	1
350	На вход программы поступает последовательность из N натуральных чисел. Рассматриваются все пары различных элементов последовательности (элементы пары не обязательно должны стоять в последовательности рядом, порядок в паре неважен). Необходимо определить количество пар, для которых произведение содержит в конце ровно 5 нулей.	117	2025-04-16 10:12:42.201412	1
351	Имеется набор данных, состоящий из пар положительных целых чисел. Необходимо выбрать из каждой пары ровно одно число так, чтобы сумма всех выбранных чисел не делилась на 3 и при этом была минимально возможной. Гарантируется, что искомую сумму получить можно. Программа должна напечатать одно число – минимально возможную сумму, соответствующую условиям задачи.	118	2025-04-16 10:21:45.722867	1
384	№13 Для скольких различных значений маски возможны заданные IP-адрес и адрес сети?	76	2025-04-20 18:02:33.924395	7
385	№13 Определить третий слева байт маски.	76	2025-04-20 18:02:44.657031	7
352	Имеется набор данных, состоящий из пар положительных целых чисел. Необходимо выбрать из каждой пары ровно одно число так, чтобы сумма всех выбранных чисел делилась на 5 и при этом была максимально возможной. Гарантируется, что искомую сумму получить можно. Программа должна напечатать одно число – максимально возможную сумму, соответствующую условиям задачи.	118	2025-04-16 10:21:50.541051	1
353	Имеется набор данных, состоящий из троек положительных целых чисел. Необходимо выбрать из каждой тройки ровно одно число так, чтобы сумма всех выбранных чисел делилась на 8 и при этом была максимально возможной. Гарантируется, что искомую сумму получить можно. Программа должна напечатать одно число – максимально возможную сумму, соответствующую условиям задачи.	118	2025-04-16 10:21:55.32426	1
354	Имеется набор данных, состоящий из положительных целых чисел. Необходимо определить количество пар элементов (a_i, a_j) этого набора, в которых 1 ≤ i + 5 ≤ j ≤ N, сумма элементов нечётна, а произведение делится на 13.	119	2025-04-16 10:22:14.989427	1
355	Дана последовательность N целых положительных чисел. Необходимо определить количество пар элементов этой последовательности, разность которых делится на m = 60 и при этом хотя бы один элемент из пары больше b = 80.	119	2025-04-16 10:22:20.00919	1
356	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров. Истинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле: d(A, B) = sqrt((x2 - x1)^2 + (y2 - y1)^2). В файле А хранятся данные о звёздах двух кластеров, где H = 3, W = 3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y. Значения даны в условных единицах. Известно, что количество звёзд не превышает 1000. В файле Б хранятся данные о звёздах трёх кластеров, где H = 3, W = 3 для каждого кластера. Известно, что количество звёзд не превышает 10 000. Структура хранения информации о звездах в файле Б аналогична файлу А. Для каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px – среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа: в первой строке сначала целую часть произведения Px × 10 000, затем целую часть произведения Py × 10 000 для файла А, во второй строке – аналогичные данные для файла Б.	110	2025-04-16 10:22:36.096545	1
357	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров. Истинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле: d(A, B) = sqrt((x1 - x2)^2 + (y1 - y2)^2). В файле А хранятся данные о звёздах двух кластеров, где H = 3, W = 3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y. Значения даны в условных единицах. Известно, что количество звёзд не превышает 1000. В файле Б хранятся данные о звёздах трёх кластеров, где H = 3, W = 3 для каждого кластера. Известно, что количество звёзд не превышает 10000. Структура хранения информации о звездах в файле Б аналогична файлу А. Для каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px – среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа: в первой строке сначала целую часть произведения Px × 10000, затем целую часть произведения Py × 10000 для файла А, во второй строке – аналогичные данные для файла Б.	115	2025-04-16 10:22:49.266075	1
358	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров. Истинный центр кластера или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле: d(A, B) = sqrt((x1 - x2)^2 + (y1 - y2)^2). В файле А хранятся данные о звёздах двух кластеров, где H = 3, W = 3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y. Значения даны в условных единицах. Известно, что количество звёзд не превышает 1000. В файле Б хранятся данные о звёздах трёх кластеров, где H = 3, W = 3, для каждого кластера. Известно, что количество звёзд не превышает 10000. Структура хранения информации о звездах в файле аналогична файлу B. Для каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px – среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа: в первой строке сначала целую часть произведения Px × 10000, затем целую часть произведения Py × 10000 для файла А, во второй строке – аналогичные данные для файла Б.	116	2025-04-16 10:23:03.959211	1
359	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров. Истинный центр кластера или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле: d(A, B) = sqrt((x1 - x2)^2 + (y1 - y2)^2). В файле А хранятся данные о звёздах двух кластеров, где H = 3, W = 3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y. Значения даны в условных единицах. Известно, что количество звёзд не превышает 1000. В файле Б хранятся данные о звёздах трёх кластеров, где H = 3, W = 3, для каждого кластера. Известно, что количество звёзд не превышает 10000. Структура хранения информации о звездах в файле аналогична файлу B. Для каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px – среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа: в первой строке сначала целую часть произведения Px × 10000, затем целую часть произведения Py × 10000 для файла А, во второй строке – аналогичные данные для файла Б.	120	2025-04-16 10:23:20.610825	1
386	№13 Два узла находятся в разных сетях. Определить наименьшее значение третьего слева байта масок этих сетей.	76	2025-04-20 18:02:57.432871	7
387	№13 Два узла находятся в разных подсетях. Определить наибольшее количество единиц в масках этих подсетей.	76	2025-04-20 18:03:08.720822	7
388	№17 Определить количество пар, в которых хотя бы один элемент меньше, чем среднее арифметическое всех чисел, и десятичные записи обоих элементов содержат 1.	76	2025-04-20 18:03:22.804789	7
360	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри окружности радиуса R. Каждая звезда обязательно принадлежит только одному из кластеров. В файле хранятся данные о звёздах трёх кластеров. Известно, что количество звёзд не превышает 10000. Для заданного файла требуется распределить все точки по трем кластерам с помощью алгоритма DBSCAN.	121	2025-04-16 10:23:33.574242	1
361	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой Н и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров. Истинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле: d(A, B) = sqrt((x2 - x1)^2 + (y2 - y1)^2). В файле А хранятся данные о звёздах двух кластеров, где H=3, W=3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y. Значения даны в условных единицах. Известно, что количество звёзд не превышает 1000. В файле Б хранятся данные о звёздах трёх кластеров, где H=3, W=3 для каждого кластера. Известно, что количество звёзд не превышает 10 000. Структура хранения информации о звездах в файле Б аналогична файлу А. Для каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px – среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров. В ответе запишите четыре числа: в первой строке сначала целую часть произведения Px × 10 000, затем целую часть произведения Py × 10 000 для файла А, во второй строке – аналогичные данные для файла Б.	122	2025-04-16 10:23:47.157976	1
362	На спутнике «Восход» установлен прибор, предназначенный для измерения солнечной активности. Каждую минуту прибор передаёт по каналу связи неотрицательное целое число – количество энергии солнечного излучения, полученной за последнюю минуту, измеренное в условных единицах. Временем, в течение которого происходит передача, можно пренебречь. Необходимо найти в заданной серии показаний прибора минимальное чётное произведение двух показаний, между моментами передачи которых прошло не менее 6 минут. Если получить такое произведение не удаётся, ответ считается равным -1.	123	2025-04-16 10:23:58.919544	1
363	По каналу связи передаётся последовательность целых чисел – показания прибора. В течение N минут (N – натуральное число) прибор ежеминутно регистрирует значение силы тока (в условных единицах) в электрической сети и передаёт его на сервер. Определите три таких переданных числа, чтобы между моментами передачи любых двух из них прошло не менее K минут, а сумма этих чисел была минимально возможной. Запишите в ответе найденную сумму.	123	2025-04-16 10:24:04.53733	1
364	Дана последовательность из N натуральных чисел. Рассматриваются все её непрерывные подпоследовательности, такие что сумма элементов каждой из них кратна k = 43. Найдите среди них подпоследовательность с максимальной суммой, определите её длину. Если таких подпоследовательностей найдено несколько, в ответе укажите количество элементов самой короткой из них.\r\n\r\nВходные данные: Даны два входных файла: файл A (27-75a.txt) и файл B (27-75b.txt), каждый из которых содержит в первой строке количество чисел N (2 ≤ N ≤ 10^8). Каждая из следующих N строк содержит натуральное число, не превышающее 10000.	124	2025-04-16 10:48:14.008246	1
365	Фрагмент звёздного неба спроецирован на плоскость с декартовой системой координат. Учёный решил провести кластеризацию полученных точек, являющихся изображениями звёзд, то есть разбить их множество на N непересекающихся непустых подмножеств (кластеров), таких что точки каждого подмножества лежат внутри прямоугольника со сторонами длиной H и W, причём эти прямоугольники между собой не пересекаются. Стороны прямоугольников не обязательно параллельны координатным осям.\r\n\r\nБудем называть центром кластера точку этого кластера, сумма расстояний от которой до всех остальных точек кластера минимальна. Для каждого кластера гарантируется единственность его центра. Расстояние между двумя точками на плоскости A(x1, y1) и B(x2, y2) вычисляется по формуле:\r\nd(A, B) = √((x1 − x2)^2 + (y1 − y2)^2)\r\n\r\nВ файле A хранятся координаты точек двух кластеров, где H = 3, W = 3 для каждого кластера. В каждой строке записана информация о расположении на карте одной точки: сначала координата x, затем координата y. Известно, что количество точек не превышает 1000.\r\n\r\nВ файле Б хранятся координаты точек трёх кластеров, где H = 3, W = 3 для каждого кластера. Известно, что количество точек не превышает 10 000.\r\n\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px – среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров.	126	2025-04-16 10:48:39.337505	1
366	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, каждая из которых находится от хотя бы одной другой звезды на расстоянии не более R условных единиц. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nИстинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2) на плоскости, которое вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2)\r\n\r\nАномалиями назовём точки, находящиеся на расстоянии более одной условной единицы от точек кластеров. При расчётах аномалии учитывать не нужно.\r\n\r\nВ файле A хранятся данные о звёздах двух кластеров, где R = 0.5 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y. Значения даны в условных единицах, которые представлены вещественными числами. Известно, что количество звёзд не превышает 2500.\r\n\r\nВ файле Б хранятся данные о звёздах четырех кластеров, где R = 0.2 для каждого кластера. Известно, что количество звёзд не превышает 10 000.\r\n\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px — среднее арифметическое абсцисс центров кластеров, и Py – среднее арифметическое ординат центров кластеров.	127	2025-04-16 10:49:26.698067	1
389	№17 Определить количество троек, в которых хотя бы два элемента больше, чем среднее арифметическое всех чисел.	76	2025-04-20 18:03:35.852644	7
569	№7. Определить размер звукового файла, полученного при повторной звукозаписи.	172	2025-05-10 19:45:32.349968	7
367	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, каждая из которых находится от хотя бы одной другой звезды на расстоянии не более R условных единиц. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nДвойная звездная система – это две звезды на расстоянии менее t. При этом других звезд на расстоянии менее t у этих двух звезд быть не должно.\r\n\r\nРасстояние между двумя точками A(x1, y1) и B(x2, y2) на плоскости вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2)\r\n\r\nВ файле Б хранятся данные о звёздах четырех кластеров, где R = 0.2, а t = 0.05 для каждого кластера. Известно, что количество звёзд не превышает 10 000.\r\n\r\nНеобходимо в каждом кластере найти пары звезд с максимальным расстоянием между ними.	128	2025-04-16 10:49:50.320477	1
368	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nТройная звездная система – система, в которой три звезды находятся на расстоянии не более d между любыми двумя звездами в системе. Других звезд на расстоянии не более d у этих трех звезд быть не должно.\r\n\r\nРасстояние между двумя точками A(x1, y1) и B(x2, y2) на плоскости вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2)\r\n\r\nНеобходимо найти треугольник с максимальным периметром в каждом кластере.	129	2025-04-16 10:50:20.290938	1
369	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, каждая из которых находится от хотя бы одной другой звезды на расстоянии не более R условных единиц. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nДвойная звездная система – это две звезды на расстоянии менее t. При этом других звезд на расстоянии менее t у этих двух звезд быть не должно.\r\n\r\nРасстояние между двумя точками A(x1, y1) и B(x2, y2) на плоскости вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2)\r\n\r\nВ файле хранятся данные о звёздах четырех кластеров, где R = 0.5, t = 0.04 для каждого кластера. Известно, что количество звёзд не превышает 10 000.\r\n\r\nДля каждого кластера найдите двойную звездную систему, состоящую из красного гиганта (масса от 6 до 8 солнечных масс) и красного карлика (масса от 0.8 до 1.5 солнечных масс) с максимальной разницей в солнечных массах. В ответе запишите четыре разницы.	130	2025-04-16 10:50:57.818451	1
370	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, каждая из которых находится от хотя бы одной другой звезды на расстоянии не более R условных единиц. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nДвойная звездная система – это две звезды на расстоянии менее t. При этом других звезд на расстоянии менее t у этих двух звезд быть не должно.\r\n\r\nРасстояние между двумя точками A(x1, y1) и B(x2, y2) на плоскости вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2)\r\n\r\nВ файле хранятся данные о звёздах кластеров, где R = 0.4, t = 0.04 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды, а также ее масса (в солнечных массах): сначала координата x, затем координата y, затем масса m.\r\n\r\nДля каждого файла в каждом кластере найдите двойную звездную систему, состоящую из нейтронной звезды (масса по модулю от 1.5 до 2.8 солнечных масс) и черной дыры (масса по модулю от 2.9 солнечных масс).	131	2025-04-16 10:51:41.969388	1
390	№17 Определить количество пар, в которых один элемент меньше, чем сумма цифр всех чисел, делящихся на 49, а другой делится на 13.	76	2025-04-20 18:04:06.980355	7
391	Сеть задана IP-адресом и маской сети. Определить количество IP-адресов, для которых кол-во единиц в двоичной записи IP-адреса не кратно 5.\r\n\r\n	67	2025-04-20 18:05:47.391495	7
392	Сеть задана IP-адресом и маской сети. Определить кол-во IP-адресов, для которых сумма единиц в двоичной записи IP-адреса не кратна 2.	67	2025-04-20 18:05:52.273341	7
393	Два узла с заданными IP-адресами находятся в одной сети. Определить наиб. значение третьего слева байта маски этой сети.	67	2025-04-20 18:05:56.968492	7
394	Два узла с заданными IP-адресами находятся в разных сетях. Определить наим. значение третьего слева байта масок этих сетей.	67	2025-04-20 18:06:06.849523	7
571	№7. Сколько секунд длилась передача файла в город Б?	172	2025-05-10 19:45:46.302442	7
371	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, каждая из которых находится от хотя бы одной другой звезды на расстоянии не более R условных единиц. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nТройная звездная система – это система, в которой три звезды попарно находятся на расстоянии не более t. При этом других звезд на расстоянии менее t у этих трех звезд быть не должно.\r\n\r\nРасстояние между двумя точками A(x1, y1) и B(x2, y2) на плоскости вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2)\r\n\r\nВ файле Б хранятся данные о звёздах четырех кластеров, где R = 0.45, t = 0.01 для каждого кластера. Известно, что количество звёзд не превышает 10 000.\r\n\r\nДля каждого в каждом кластере файла найдите тройную звезду, которая образует треугольник с наименьшим периметром. Затем вычислите два числа: Px – среднее арифметическое абсцисс найденных звезд, и Py – среднее арифметическое ординат найденных звезд.	132	2025-04-16 10:52:39.129082	1
372	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nИстинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд минимальна. Расстояние между двумя точками A(x1, y1, z1) и B(x2, y2, z2) вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2 + (z2 − z1)^2)\r\n\r\nВ файле А хранятся данные о звёздах двух кластеров, где H = 3, W = 3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y, затем координата z.\r\n\r\nВ файле Б хранятся данные о звёздах трех кластеров, где H = 3, W = 3 для каждого кластера.\r\n\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите три числа: Px — среднее арифметическое абсцисс звезд, Py – среднее арифметическое ординат звезд, Pz – среднее арифметическое аппликат центров кластеров.	133	2025-04-16 10:53:26.545638	1
373	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной W. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nИстинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд минимальна. Расстояние между двумя точками A(x1, y1, z1) и B(x2, y2, z2) вычисляется по формуле:\r\nd(A, B) = √((x2 − x1)^2 + (y2 − y1)^2 + (z2 − z1)^2)\r\n\r\nВ файле А хранятся данные о звёздах двух кластеров, где H = 3, W = 3 для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x, затем координата y, затем координата z.\r\n\r\nВ файле Б хранятся данные о звёздах трех кластеров, где H = 3, W = 3 для каждого кластера.\r\n\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите три числа: Px — среднее арифметическое абсцисс звезд, Py – среднее арифметическое ординат звезд, Pz – среднее арифметическое аппликат центров кластеров.	134	2025-04-16 10:53:52.48983	1
374	Сколько слов можно составить так, чтобы в каждом из них Р использовалась хотя бы 2 раза?	72	2025-04-20 17:51:18.100358	7
375	Сколько слов можно составить так, чтобы в каждом из них Г использовалась 1 раз только на первом или последнем месте?	72	2025-04-20 17:52:35.430625	7
376	Сколько слов можно составить так, чтобы каждое из них не начиналось с Ч и не содержало сочетания ИАУ?	72	2025-04-20 17:52:52.943425	7
377	Сколько слов можно составить перестановкой букв исходного слова?	72	2025-04-20 17:52:56.103049	7
378	Все составленные слова записаны в алфавитном порядке. Определить под каким номером стоит первое слово, в котором нет А.	72	2025-04-20 17:53:06.690142	7
379	Все составленные слова записаны в алфавитном порядке. Определить номер последнего слова, в котором нет О и рядом стоящих С.\r\n\r\n	72	2025-04-20 17:53:14.553762	7
380	(№25)  На отрезке найти числа, имеющие ровно 4 различных делителя	72	2025-04-20 17:53:37.01471	7
381	(№25)  На отрезке найти числа, представляющие собой произведение двух различных простых делителей.\r\n\r\n	72	2025-04-20 17:53:48.283434	7
382	№13 Сколько в заданной сети IP-адресов, для которых количество единиц в двоичной записи IP-адреса не кратно 3?	76	2025-04-20 18:02:14.976653	7
399	Даны IP-адрес и адрес подсети. Определить количество значений третьего слева байта маски, если в сети не менее К узлов.	67	2025-04-20 18:06:39.504157	7
400	На отрезке найти числа, имеющие ровно 4 различных делителя.	30	2025-04-20 18:11:41.046211	7
401	На отрезке найти числа, имеющие ровно 3 нетривиальных делителя.	30	2025-04-20 18:11:47.519115	7
402	На отрезке найти числа, представляющие собой произведение двух различных простых делителей\r\n\r\n	30	2025-04-20 18:11:52.876971	7
403	На отрезке найти числа, соответствующие маске 12*4?65, делящиеся на 161 без остатка.	30	2025-04-20 18:11:59.004496	7
404	На отрезке найти числа, имеющие ровно 4 различных делителя.	43	2025-04-20 18:18:14.405655	7
405	На отрезке найти числа, имеющие ровно 3 нетривиальных делителя.	43	2025-04-20 18:18:20.030142	7
406	На отрезке найти числа, представляющие собой произведение двух различных делителей.	43	2025-04-20 18:18:28.152587	7
407	На отрезке найти числа, представляющие собой произведение трех различных простых делителей, оканчивающихся на одну и ту же цифру.	43	2025-04-20 18:18:34.382469	7
408	На отрезке найти числа, соответствующие маске 202*47*6 и делящиеся на 9573 без остатка.	43	2025-04-20 18:18:40.21859	7
409	На отрезке найти числа, соответствующие маске 73*5F486F и делящиеся на 43 без остатка.	43	2025-04-20 18:19:15.343292	7
410	№8. Сколько существует шестнадцатеричных трехзначных чисел, в которых все цифры различны и никакие две четные или две нечетных цифры не стоят рядом?	48	2025-04-20 18:22:10.230658	7
411	№25. На отрезке найти числа, имеющие ровно 4 различных делителя.	48	2025-04-20 18:22:25.143721	7
412	№25. На отрезке найти числа, представляющие собой произведение двух различных простых делителей.	48	2025-04-20 18:22:33.695366	7
413	№24. Найти длину самой длинной подцепочки, состоящей из символов С.	48	2025-04-20 18:22:44.183115	7
414	№24. Определить максимальное количество идущих подряд троек символов вида цифра+буква+цифра.	48	2025-04-20 18:22:51.922361	7
415	№24. Определить максимальное количество идущих подряд символов, среди которых нет сочетания QW.	48	2025-04-20 18:23:09.319434	7
416	Найти числа, имеющие ровно 6 различных делителей.\r\n🔹Хорошее объяснение решения базовой задачи\r\n	56	2025-04-20 18:24:48.908075	7
417	Найти числа, соответствующие маске 3?458*3.	56	2025-04-20 18:24:57.912656	7
418	Найти числа, соответствующие маске 3?458*3, у которых в девятеричной записи цифры идут в порядке невозрастания.	56	2025-04-20 18:25:04.458611	7
419	Найти числа, соответствующие маске 1234*7, делящиеся на 141 без остатка, у которых ровно 4 делителя.\r\n\r\n	56	2025-04-20 18:25:11.787443	7
420	Найти числа, соответствующие маске 73*5F486F и делящиеся на 43 без остатка.	56	2025-04-20 18:25:16.409665	7
421	 Сколько единиц в записи числа?	45	2025-04-20 18:28:41.276792	7
422	Указать все основания с.с., в которых запись числа 22 оканчивается на 4.	45	2025-04-20 18:28:49.829422	7
423	В с.с. с некоторым основанием число 12 записывается как 110. Определить это основание.	45	2025-04-20 18:28:55.370399	7
424	Сколько значащих нулей в двоичной записи восьмеричного числа 7512?без остатка.	45	2025-04-20 18:29:02.212321	7
425	Определить количество строк, для которых выполняется: в строке есть как повторяющиеся, так и неповторяющиеся числа; среднее арифметическое всех неповторяющихся чисел строки больше, чем среднее арифметическое повторяющихся.	59	2025-04-20 18:34:05.530378	7
426	Определить количество строк, для которых выполняется: наибольшее из четыре чисел меньше суммы трех других; среди четырех чисел есть только одна пара равных чисел.\r\n\r\n	59	2025-04-20 18:34:11.726825	7
427	Определить количество строк, для которых выполняется: в строке только одно число повторяется трижды; квадрат суммы всех повторяющихся чисел строки больше квадрата суммы всех ее неповторяющихся чисел.	59	2025-04-20 18:34:16.873142	7
428	Определить количество строк таблицы, содержащих хотя бы одну ячейку со свойствами: число в ячейке повторяется в ячейках этой строки; число в ячейке встречается меньше К раз в других строках таблицы.	59	2025-04-20 18:34:21.739471	7
429	Определить количество строк, для которых выполняется: в строке одно число повторяется дважды; сумма цифр различных чисел больше К.	59	2025-04-20 18:34:27.819651	7
430	Сколько слов можно составить так, чтобы в каждом из них К использовалась ровно 2 раза?	62	2025-04-20 18:38:26.220349	7
431	Сколько слов можно составить так, чтобы в каждом из них Р использовалась хотя бы 2 раза?	62	2025-04-20 18:38:48.327981	7
456	№18. Робот двигается по полю. Определить максимальную и минимальную денежные суммы, которые может собрать робот.	70	2025-04-20 18:52:24.687243	7
432	Сколько слов можно составить так, чтобы в каждом из них на первом и последнем местах стояли буквы Э, Ю, Я, и чтобы они не встречались на других позициях?	62	2025-04-20 18:38:54.826788	7
433	Сколько слов можно составить так, чтобы в каждом из них Ь не стояла на последнем месте и между гласными?	62	2025-04-20 18:39:03.352857	7
434	Игральный кубик бросается 8 раз. Какова вероятность того, что ровно 3 раза выпадет число, кратное 3?	62	2025-04-20 18:39:14.452528	7
435	Алгоритм вычисления функции F(n) задан соотношениями. Определить значение функции F(24).	63	2025-04-20 18:42:49.893373	7
436	Алгоритм вычисления функции F(n) задан соотношениями. Определить значение выражения F(2023)/F(2020).\r\n🔹17:16 - Решение на python: рекурсия\r\n🔹20:17 - Динамическое программирование\r\n🔹22:07 - Решение на python: динамика\r\n🔹29:22 - Решение руками\r\n	63	2025-04-20 18:42:58.018321	7
437	Алгоритм вычисления функций F(n) и G(n) задан соотношениями. Определить значение F(14)+G(14).	63	2025-04-20 18:43:07.97128	7
438	Алгоритм вычисления функции F(n) задан соотношениями. Определить количество значений n на отрезке, для которых F(n)=3.	63	2025-04-20 18:43:15.03908	7
439	Алгоритм вычисления функции F(n) задан соотношениями. Определить количество значений n из отрезка, для которых сумма цифр значения F(n)=27.	63	2025-04-20 18:43:23.027615	7
440	№23. У исполнителя есть 2 команды. Сколько существует программ, преобразующих число 1 в 16?	63	2025-04-20 18:43:43.828295	7
441	№23. У исполнителя есть 3 команды. Сколько существует программ, преобразующих число 3 в 21, при этом траектория вычислений содержит 8 и не содержит 12?	63	2025-04-20 18:43:52.350892	7
442	№23. У исполнителя есть 3 команды. Сколько существует программ, преобразующих число 3 в 30 и не содержащих двух команд «+1» подряд?	63	2025-04-20 18:44:03.655051	7
443	№3. Определить общую стоимость кофе всех сортов, проданного у магазинах N-го района за указанный период.\r\n🔹6:46 - Условие: определить магазин, в котором было продано максимальное количество кофе	65	2025-04-20 18:46:15.886533	7
444	№3. Определить, сколько кг детского мыла поступило в магазины N-го района за указанный период.	65	2025-04-20 18:46:40.790754	7
445	№3. Определить общий объем всех видов шампуня, проданных в магазинах на N-ой улице за указанный период.	65	2025-04-20 18:46:47.600193	7
446	№3. Определить разницу между суммой на счете с максимальным суммарным поступлением и суммой на счете с минимальным суммарным поступлением за указанный период.	65	2025-04-20 18:46:55.66855	7
447	№9. Определить количество строк, для которых выполняется: в строке есть как повторяющиеся, так и неповторяющиеся числа; среднее арифметическое всех неповторяющихся чисел строки больше, чем среднее арифметическое повторяющихся чисел.	65	2025-04-20 18:47:04.823625	7
448	№9. Определить количество строк, для которых выполняется: в строке одно число повторяется дважды; среднее арифметическое наибольшего и наименьшего чисел больше, чем среднее арифметическое всех чисел.	65	2025-04-20 18:47:17.876344	7
449	№9. Определить количество строк, в которых сумма наибольшего и наименьшего чисел не больше суммы двух оставшихся.	65	2025-04-20 18:47:29.33004	7
450	Определить кол-во строк, для которых выполняется: в строке одно число повторяется дважды; повторяющееся число строки не меньше, чем среднее арифметическое неповторяющихся чисел.	66	2025-04-20 18:50:12.337536	7
451	Определить кол-во строк, содержащих хотя бы одну ячейку со следующими свойствами: число в ячейке повторяется в ячейках этой строки; число в ячейке встречается более К раз в других строках.	66	2025-04-20 18:50:25.033816	7
452	Определить количество строк, содержащих числа, для которых выполняется: наибольшее из четырех чисел меньше суммы трех других; четыре числа можно разбить на 2 пары чисел с равными суммами.	66	2025-04-20 18:50:29.527135	7
453	Определить кол-во строк, содержащих числа, для которых выполняется: в строке одно число повторяется трижды; квадрат суммы всех повторяющихся чисел больше квадрата суммы неповторяющихся.	66	2025-04-20 18:50:37.508307	7
454	Определить количество строк, в которых все числа различны, а сумма цифр наибольшего и наименьшего чисел больше суммы цифр двух оставшихся.\r\n\r\n	66	2025-04-20 18:50:49.391458	7
455	Ячейка называется интересной, если: число в ячейке больше не встречается в данной строке; число в ячейке встречается в данном столбце, менее К раз. Определить количество строк, содержащих более М интересных ячеек.	66	2025-04-20 18:50:57.35083	7
553	№11. В системе хранятся идентификаторы. Определить объем памяти для хранения К идентификаторов.	68	2025-05-10 19:38:08.618709	7
457	№18. Робот двигается по полю с внутренними стенами. Определить максимальную и минимальную денежные суммы, которые может собрать робот.	70	2025-04-20 18:52:32.099276	7
458	№18. Ладья перемещается по полю. Определить минимальную и максимальную сумму чисел в клетках, в которых может остановиться ладья.\r\n🔹28:53 - Удобное сохранение кода\r\n🔹33:27- Как перемещается ладья?\r\n	70	2025-04-20 18:52:42.323745	7
459	№18. Робот двигается по полю с ямами. Определить максимальную и минимальную денежную сумму, которую может собрать робот, не застряв в яме.	70	2025-04-20 18:52:55.950414	7
460	№22. Определить минимальное время, через которое завершится выполнение всей совокупности процессов, при условии, что независимые друг от друга процессы могут выполняться параллельно.	70	2025-04-20 18:53:08.626208	7
461	№22. Определить максимальную продолжительность отрезка времени, в течение которого возможно одновременное выполнение 4 процессов, при условии, что независимые процессы могут выполняться параллельно.	70	2025-04-20 18:53:16.437866	7
462	Определить максимальную длину подстроки, в которой символ Y встречается не более К раз.\r\n\r\n	73	2025-04-20 18:56:10.634058	7
463	Определить минимальную длину подстроки, в которой символ Z встречается не менее К раз.\r\n\r\n	73	2025-04-20 18:56:13.276338	7
464	Определить максимальное количество идущих подряд символов, среди которых каждая из букв Х, Y, Z встречается не более 3 раз.\r\n\r\n	73	2025-04-20 18:56:29.352909	7
465	Определить максимальное количество идущих подряд символов, среди которых буквы Х и Y встречаются ровно по 1 разу, а буква А не встречается совсем.	73	2025-04-20 18:56:34.774871	7
466	 Определить максимальное количество идущих подряд символов, среди которых пара символов DE встречается не более К раз.	73	2025-04-20 18:56:41.789143	7
467	№16. Алгоритм вычисления функции F(n) задан соотношениями. Определить значение функции F(64).	74	2025-04-20 18:59:32.235418	7
468	№16. Алгоритм вычисления функции F(n) задан соотношениями. Определить количество значений n из отрезка, при которых значение F(n) не содержит 1.	74	2025-04-20 18:59:40.618046	7
469	№16. Алгоритм вычисления функций F(n) и G(n) задан соотношениями. Определить значение F(14)+G(14).	74	2025-04-20 18:59:51.236331	7
470	№23. У исполнителя есть 2 команды. Определить количество программ, преобразующих число 1 в 55.	74	2025-04-20 19:00:02.082369	7
471	№23. У исполнителя есть 2 команды. Сколько существует программ, преобразующих число 3 в 30, при этом траектория вычислений содержит 20 и не содержит 12?	74	2025-04-20 19:00:17.837335	7
472	№23. У исполнителя есть 3 команды. Сколько существует программ, преобразующих число 1 в 14, при этом не содержащих двух команд умножения подряд?	74	2025-04-20 19:00:27.748172	7
473	№23. У исполнителя есть 2 команды. Сколько результатов можно получить из исходного числа 2 после выполнения программы, содержащей 15 команд?\r\n\r\n	74	2025-04-20 19:00:37.631425	7
474	№1. Определить, какие номера пунктов в таблице могут соответствовать пунктам В и Е на схеме.	75	2025-04-20 19:03:38.831781	7
475	№1. Определить длину кратчайшего пути между пунктами Е и Л.	75	2025-04-20 19:03:47.515723	7
476	№1. Определить длину кратчайшего пути между пунктами Ж и Г.	75	2025-04-20 19:03:59.325482	7
477	№6. Определить периметр объединения фигур, ограниченных заданными алгоритмом линиями.\r\n\r\n	75	2025-04-20 19:04:10.356449	7
478	№6. Определить периметр области пересечения фигур, ограниченных заданными алгоритмом линиями.	75	2025-04-20 19:04:42.211592	7
479	№6. Определить, из какого количества отрезков будет состоять фигура, заданная данным алгоритмом.	75	2025-04-20 19:04:51.879753	7
480	№12. Исполнитель редактор. Определить наименьшее n, при котором сумма цифр в строке, получившейся в результате выполнения программы, равна 63.	75	2025-04-20 19:05:06.33019	7
481	№12. Исполнитель чертежник. Определить максимальное N, для которого найдутся такие a и b, что после выполнения программы чертежник вернется в исходную точку?	75	2025-04-20 19:05:21.766077	7
482	Определить максимальное количество идущих подряд символов, в которых каждая из указанных букв встречается не более 8 раз, а буквы V, X, Z не встречаются совсем.	79	2025-04-20 19:08:11.024714	7
483	Определить максимальную длину последовательности вида число1=число2=числоN, в которой нет соседних знаков = и есть хотя бы одно пятизначное число, которое является квадратом простого числа.	79	2025-04-20 19:08:35.564344	7
484	Определить максимальное количество символов в непрерывной последовательности, которая является корректным арифметическим выражением с целыми числами.	79	2025-04-20 19:08:44.902105	7
485	Входной файл содержит заявки пассажиров, желающих сдать свой багаж в камеру хранения. В заявке указаны время сдачи багажа и время освобождения ячейки (в минутах от начала суток). Багаж одного пассажира размещается в одной свободной ячейке с минимальным номером. Ячейки пронумерованы начиная с единицы. Размещение багажа в ячейке или её освобождение происходит в течение 1 мин. Багаж можно поместить в только что освобождённую ячейку начиная со следующей минуты. Если в момент сдачи багажа свободных ячеек нет, то пассажир уходит.\r\n\r\nВходные данные представлены в файле следующим образом.\r\n\r\nВ первой строке входного файла находится натуральное число K  , не превышающее 1000, – количество ячеек в камере хранения. Во второй строке – натуральное число N   (N   ≤  1000), обозначающее количество пассажиров. Каждая из следующих N   строк содержит два натуральных числа, каждое из которых не превышает 1440: указанное в заявке время размещения багажа в ячейке и время освобождения ячейки (в минутах от начала суток).\r\n\r\nТребуется выбрать для каждой ячейки один багаж, который находился в ней в течении 24 часов так, чтобы сумма времени хранения всех выбранных багажей была максимальной и не кратной 13.\r\n\r\nВ ответе запишите одно число: найденную сумму.\r\n\r\nПример входного файла:\r\n\r\n2\r\n\r\n5\r\n\r\n30 60\r\n\r\n40 1000\r\n\r\n59 60\r\n\r\n61 1000\r\n\r\n1010 1440	183	2025-04-20 19:11:58.932329	7
486	Для обеспечения безопасности на шоссе устанавливаются камеры видеонаблюдения. Установка возможна только в заранее определённых точках — на мачтах вдоль дороги. Известны расстояния от начала шоссе до каждой мачты.\r\n\r\nПо нормативам, чтобы камеры не мешали друг другу и не дублировали зоны наблюдения, любые две установленные камеры должны находиться на расстоянии не менее 10   метров друг от друга.\r\n\r\nНеобходимо установить максимально возможное количество камер, не нарушая нормативов и определить максимально возможное расстояние от начала шоссе до ближайшей установленной камеры при этом размещении.\r\n\r\nВходные данные\r\n\r\nВ первой строке — число N   (натуральное, не больше 10000  ) — количество мачт. В следующих N   строках — расстояния от начала шоссе до каждой мачты (натуральные числа не больше 10000  ), каждое в отдельной строке.\r\n\r\nВыходные данные\r\n\r\nДва целых числа через пробел: максимальное количество установленных камер и максимально возможное расстояние от начала шоссе до ближайшей установленной камеры\r\n\r\nПример входного файла:\r\n\r\n8  \r\n\r\n15  \r\n\r\n25  \r\n\r\n5  \r\n\r\n35  \r\n\r\n12  \r\n\r\n45  \r\n\r\n20  \r\n\r\n3  \r\n\r\nПри таких входных данных мы можем установить камеры на мачты 45  , 35  , 25  , 15  , 5   или 2  , 12  , 25  , 35  , 45  . Максимальное количество камер - 5, а максимальное расстояние до ближайшей камеры - 5.	184	2025-04-20 19:12:48.367863	7
487	При проведении эксперимента заряженные частицы попадают на чувствительный экран, представляющий из себя матрицу размером 100 000 на 100 000 точек. При попадании очередной частицы на экран в файл записываются координаты чувствительного элемента: номер строки (целое число от 1 до 100 000) и номер позиции в строке (целое число от 1 до 100 000). Точка экрана, в которую попала хотя бы одна частица, считается светлой, точка, в которую ни одна частица не попала, – тёмной.\r\n\r\nВам нужно определить наибольшую длину цепочки в одной строке, в которой светлые точки идут подряд. Если таких строк несколько, укажите номер первой из подходящих строк.\r\n\r\nВходные данные представлены в файле следующим образом. В первой строке входного файла записано целое число N – количество частиц, попавших на экран. В каждой из следующих N строк записаны по два числа, разделённые пробелом: номер строки и номер позиции в строке.\r\n\r\nЗапишите в ответе два числа через пробел: сначала номер строки, в которой находится эта цепочка (если таких строк несколько, запишите минимальный из их номеров), затем количество светлых точек в самой длинной цепочке из светлых точек.	184	2025-04-20 19:13:07.855755	7
488	Фрагмент звёздного неба спроецирован на плоскость с декартовой системой координат. Учёный решил провести кластеризацию полученных точек, являющихся изображениями звёзд, то есть разбить их множество на N   непересекающихся непустых подмножеств (кластеров), таких что точки каждого подмножества лежат внутри прямоугольника со сторонами длиной H   и W  , причём эти прямоугольники между собой не пересекаются. Стороны прямоугольников не обязательно параллельны координатным осям. Гарантируется, что такое разбиение существует и единственно для заданных размеров прямоугольников.\r\n\r\nБудем называть центром кластера точку этого кластера, сумма расстояний от которой до всех остальных точек кластера минимальна. Для каждого кластера гарантируется единственность его центра. Расстояние между двумя точками на плоскости A (x1,y1)   и B (x2,y2)   вычисляется по формуле:\r\n\r\n         ∘ ---------------------\r\nd(A,B) =   ((x1 − x2)2 + (y1 − y2)2)\r\nВ файле хранятся координаты точек трёх кластеров, где H = 3  , W  = 3   для каждого кластера. В каждой строке записана информация о расположении на карте одной точки: сначала координата x  , затем координата y  . Известно, что количество точек не превышает 10 000.\r\n\r\nДля файла определите координаты центра каждого кластера, затем вычислите два числа: Px   – среднее арифметическое абсцисс центров кластеров, и Py   – среднее арифметическое ординат центров кластеров.\r\n\r\nВ ответе запишите два числа: в первой строке сначала целую часть произведения Px × 10000  , затем целую часть произведения Px × 10000   для файла.	125	2025-05-01 05:18:38.797411	7
489	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор\r\nзвёзд (точек) на графике, лежащий внутри прямоугольника высотой H и шириной\r\nW. Каждая звезда обязательно принадлежит только одному из кластеров.\r\nИстинный центр кластера или центроид, – это одна из звёзд на графике, сумма\r\nрасстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1, y1) и B(x2, y2)\r\nна плоскости, которое вычисляется по формуле:\r\nd(A, B) = p((x1 − x2)^2 + (y1 − y2)^2)\r\nВ файле A хранятся данные о звёздах двух кластеров, где H = 3, W = 3 для\r\nкаждого кластера. В каждой строке записана информация о расположении на карте\r\nодной звезды: сначала координата x, затем координата y. Значения даны в условных\r\nединицах. Известно, что количество звёзд не превышает 1000.\r\nВ файле Б хранятся данные о звёздах трёх кластеров, где H = 3, W = 3, для\r\nкаждого кластера. Известно, что количество звёзд не превышает 10000. Структура\r\nхранения информации о звездах в файле аналогична файлу Б.\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px – среднее арифметическое абсцисс центров кластеров, и Py\r\n– среднее арифметическое ординат центров кластеров. В ответе запишите четыре\r\nчисла: в первой строке сначала целую часть произведения Px · 10000 , затем целую\r\nчасть произведения Py · 10000 для файла А, во второй строке – аналогичные данные\r\nдля файла Б	136	2025-05-01 05:20:56.764023	7
490	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, каждая из которых находится от хотя бы одной другой звезды на расстоянии не более R условных единиц. Каждая звезда обязательно принадлежит только одному из кластеров. Истинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна. Под расстоянием понимается расстояние Евклида между двумя точками A(x1,y1)   и B (x2,y2)   на плоскости, которое вычисляется по формуле:\r\n\r\nd(A,B ) =  (x2 − x1) + (y2 − y1)  \r\n\r\nАномалиями назовём точки, находящиеся на расстоянии более одной условной единицы от точек кластеров. При расчётах аномалии учитывать не нужно.\r\n\r\nВ файле A хранятся данные о звёздах двух кластеров, где R = 0,5   для каждого кластера. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x  , затем координата y  . Значения даны в условных единицах, которые представлены вещественными числами. Известно, что количество звёзд не превышает 2500.\r\n\r\nВ файле Б хранятся данные о звёздах четырех кластеров, где R = 0,2   для каждого кластера. Известно, что количество звёзд не превышает 10 000. Структура хранения информации о звездах в файле Б аналогична файлу А.\r\n\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px   — среднее арифметическое абсцисс центров кластеров, и P\r\n y   – среднее арифметическое ординат центров кластеров.\r\n\r\nВ ответе запишите четыре числа через пробел: сначала целую часть произведения Px ⋅100   для файла А, затем P  ⋅100\r\n y   для файла А, далее целую часть P ⋅100\r\n x   для файла Б и P  ⋅100\r\n  y   для файла Б. Возможные данные одного из файлов иллюстрированы графиком.	137	2025-05-01 05:22:01.585219	7
495	На отрезке найти числа, соответствующие маске 12*4?65, делящиеся на 161 без остатка.\r\n\r\n39:55 - Условие: маска 12*34*56\r\n42:25 - Условие: маска 12*25*56\r\n44:36 - Условие: маска 12*23*35*56	31	2025-05-10 08:32:16.879296	7
498	Определить количество городов с населением не менее К, которые являются столицами стран, в которых распространены несколько языков с процентом более 10 каждый.	78	2025-05-10 08:36:29.617254	7
554	№11. В базе хранятся результаты измерений и год измерения. Определить объем памяти для хранения результатов всех измерений.	68	2025-05-10 19:38:17.651015	7
491	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, образующий звезду на небесном полотне. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nТакже на звёздном небе присутствует пучок звёзд, образующий синусоиду. Кластер звёзд может считаться принадлежащим синусоиде, если график синусоиды проходит сквозь кластер\r\n\r\nИстинный центр кластера, или центроид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера минимальна.\r\n\r\nПод расстоянием понимается расстояние Евклида между двумя точками A(x1,y1)   и B(x2,y2)   на плоскости, которое вычисляется по формуле:\r\n\r\nd(A,B ) =  (x2 − x1)2 + (y2 − y1)2\r\nВ файле A хранятся данные о звёздах четырёх кластеров. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x  , затем координата y  . Значения даны в условных единицах, которые представлены вещественными числами. Известно, что количество звёзд не превышает 5500.\r\n\r\nВ файле Б хранятся данные о звёздах восьми кластеров. Известно, что количество звёзд не превышает 35000. Структура хранения информации о звёздах в файле Б аналогична файлу А.\r\n\r\nДля каждого файла определите координаты центра каждого кластера, затем вычислите два числа: Px   – среднее арифметическое абсцисс центров кластеров, и Py   – среднее арифметическое ординат центров кластеров. Кластеры, принадлежащие синусоиде, в вычислениях не учитывать.\r\n\r\nВ ответе запишите четыре числа через пробел: сначала целую часть произведений Px ⋅100   и Py ⋅100   для файла А, далее целую часть произведения Px ⋅1000   и Py ⋅1000   для файла Б.	137	2025-05-01 05:22:23.020104	7
500	№3. Определить код исполнителя старше 30 лет с гражданством Китая, который заработал больше всего при оказании определенной услуги.	78	2025-05-10 08:39:19.215894	7
501	№22. Определить максимальную продолжительность отрезка времени, в течение которого возможно одновременное выполнение максимального количества процессов, при условии, что все независимые друг от друга процессы могут выполняться параллельно.	78	2025-05-10 08:39:32.199379	7
502	№3. Определить минимальную разницу между суммами на двух разных счетах, которые идут друг за другом.\r\n\r\n	171	2025-05-10 18:52:53.27719	7
503	№3. Определить среднюю сумму, на которую изменились средства в указанный период по всем счетам в рублях.	171	2025-05-10 18:53:01.665646	7
510	№9. Определить количество строк, для которых выполняется: сумма повторяющихся чисел больше, чем сумма неповторяющихся; удвоенная сумма максимального и минимального чисел не больше суммы оставшихся трех.	173	2025-05-10 19:00:55.612068	7
511	№9. Определить количество строк, для которых выполняется: два числа повторяются дважды; сумма максимального и минимального чисел является четной.	173	2025-05-10 19:01:03.70885	7
516	№17. Определить количество троек, которые могут являться сторонами остроугольного треугольника.	173	2025-05-10 19:02:43.383628	7
518	Определить мин. время, через которое завершится выполнение всей совокупности процессов, при условии, что все независимые друг от друга процессы могут выполняться параллельно.	174	2025-05-10 19:04:50.935152	7
521	Определить мин. значение мс, на которой первый раз количество выполняемых процессов изменилось с 3 до 2, при условии, что все независимые процессы стартовали одновременно, а зависимые стартовали одновременно с завершением всех процессов, от которых они зависят.	174	2025-05-10 19:05:07.967361	7
525	Определить максимальное значение, которое является результатом вычисления непрерывной последовательности, являющейся корректным арифметическим выражением, в котором присутствует операция умножения, но операция сложения может как присутствовать, так и отсутствовать.	175	2025-05-10 19:14:37.307788	7
528	Определить макс. количество символов в непрерывной последовательности, состоящей из буквы А, за которой следует корректное арифметическое выражение в 10 СС.	179	2025-05-10 19:22:15.91156	7
529	Определить макс. длину подстроки, состоящей из троек UPK или KPU.	179	2025-05-10 19:22:20.949793	7
530	Определить самую длинную подстроку, которая может являться числом в 20 СС.	179	2025-05-10 19:22:26.501096	7
532	Определить макс. количество символов в непрерывной последовательности, которая является корректным арифметическим выражением, содержащим не более 10 арифметических знаков, с целыми числами, кратными 25.	179	2025-05-10 19:22:38.097292	7
533	№7. Определить объем памяти, необходимый для хранения изображения.	57	2025-05-10 19:32:30.624351	7
534	№7. Определить максимально возможное количество цветов в палитре изображения.	57	2025-05-10 19:32:39.030463	7
539	№7. Определить максимальную битовую глубину кодирования звука, которая могла быть использована в записи.	57	2025-05-10 19:33:24.374984	7
540	№7. Текст сохранили в виде аудиозаписи. Запись сжали и разделили на фрагменты. Определить количество полученных фрагментов.	57	2025-05-10 19:33:37.617317	7
543	№11. В системе хранятся идентификаторы пользователей. Определить объем памяти, необходимый для хранения N идентификаторов.	57	2025-05-10 19:33:57.276474	7
551	№11. В системе хранятся пароли пользователей и доп сведения о них. Определить объем памяти для хранения доп сведений об одном пользователе.	68	2025-05-10 19:37:31.739279	7
555	Определить количество цветов в палитре.	69	2025-05-10 19:41:38.714726	7
560	При сохранении изображение сжимается. Определить количество цветов в палитре.	69	2025-05-10 19:42:02.145467	7
493	Учёный Галлей, увлечённый астрономией, решил исследовать звёздное небо и провести кластеризацию звёзд по их расположению на карте. Каждая звезда представлена точкой на графике, а кластер звёзд – это набор точек, лежащих внутри прямоугольника. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nЦентр звёздного скопления – это одна из звёзд, сумма расстояний от которой до всех остальных звёзд в кластере минимальна. Галлей считает, что эта звезда является ключевой для понимания структуры скопления.\r\n\r\nПод расстоянием понимается расстояние Евклида между двумя точками A(x1,y1)   и B (x2,y2)   на плоскости, которое вычисляется по формуле:\r\n\r\n\r\nd(A,B ) =  (x2 − x1)2 + (y2 − y1)2\r\nАномалиями назовём точки, находящиеся на расстоянии не менее R условных единиц от точек кластеров. При расчётах аномалии учитывать не нужно. Координатная четверть, в которой лежит больше всего центров звёздных скоплений, считается зоной повышенной чувствительности. Кластеры, центры которых расположенные в данной зоне, считаются ложными, и не используются учёным в дальнейших расчётах.\r\n\r\nВ файле А хранятся данные о четырех кластерах звёзд, где R = 0.45   для каждого кластера. В каждой строке записана информация о расположении одной звезды: сначала координата x  , затем координата y  . Значения даны в условных единицах, которые представлены вещественными числами. Известно, что количество звёзд не превышает 1000.\r\n\r\nВ файле Б хранятся данные о шести кластерах звёзд, где R = 0.4   для каждого кластера. Известно, что количество звёзд не превышает 10000. Структура хранения информации о звёздах в файле Б аналогична файлу А.\r\n\r\nДля каждого файла определите координаты центра звёздного скопления каждого кластера, затем вычислите два числа: Zx   – среднее арифметическое абсцисс центров звёздных скоплений, и Zy   – среднее арифметическое ординат центров звёздных скоплений. Если в каждой четверти лежит одинаковое количество центров звёздных скоплений, считать  Zx   и Zy   равными 0.\r\n\r\nВ ответе запишите четыре числа через пробел: сначала целую часть произведений Zx ⋅100   и Zy ⋅100   для файла А, далее целую часть произведения Zx ⋅1000   и Zy ⋅1000   для файла Б.	135	2025-05-01 05:24:14.179051	7
492	Учёный решил провести кластеризацию некоторого множества звёзд по их расположению на карте звёздного неба. Кластер звёзд – это набор звёзд (точек) на графике, образующий цветы на небесном полотне. Каждая звезда обязательно принадлежит только одному из кластеров.\r\n\r\nИстинная периферия кластера, или перифероид, – это одна из звёзд на графике, сумма расстояний от которой до всех остальных звёзд кластера максимальна.\r\n\r\nПод расстоянием понимается расстояние Евклида между двумя точками A(x1,y1)   и B(x2,y2)   на плоскости, которое вычисляется по формуле:\r\n\r\nd(A,B ) = (x2 − x1)2 + (y2 − y1)2\r\n\r\nВ файле A хранятся данные о звёздах трёх цветков. В каждой строке записана информация о расположении на карте одной звезды: сначала координата x  , затем координата y  . Значения даны в условных единицах, которые представлены вещественными числами. Известно, что количество звёзд не превышает 10000.\r\n\r\nВ файле Б хранятся данные о звёздах пяти цветков. Известно, что количество звёзд не превышает 25000. Структура хранения информации о звёздах в файле Б аналогична файлу А.\r\n\r\nДля каждого файла определите координаты периферии каждого кластера, затем вычислите два числа: Px   — среднее арифметическое абсцисс периферий кластеров, и Py   – среднее арифметическое ординат периферий кластеров.\r\n\r\nВ ответе запишите четыре числа через пробел: сначала целую часть произведений Px ⋅100   и Py ⋅100   для файла А, далее целую часть произведения Px ⋅100   и Py ⋅100   для файла Б.	137	2025-05-01 05:22:45.886102	7
494	На отрезке найти числа, которые можно разбить на пары натуральных числа, наибольший общий делитель которых равен 28.	31	2025-05-10 08:31:57.977885	7
496	На отрезке найти числа, соответствующие маске 73*5F486F, делящиеся на 43 без остатка.	31	2025-05-10 08:32:25.334604	7
497	№3. Определить объем шампуней, проданных магазинами на улице N, за указанный период.	78	2025-05-10 08:36:10.316364	7
499	№3. Определить разницу между суммой на счете с максимальным суммарным поступлением и суммой на счете с минимальным суммарным поступлением за указанный период.\r\n\r\n	78	2025-05-10 08:38:42.57343	7
512	№9. Определить количество строк, для которых выполняется хотя бы 1 условие: разница максимального и минимального чисел больше суммы нечетных чисел; нечетных чисел больше чем четных.	173	2025-05-10 19:01:13.719779	7
513	№17. Определить количество пар, разность которых четна и хотя бы одно число кратно 31.	173	2025-05-10 19:01:28.064255	7
514	№17. Определить количество троек, в которых хотя бы 2 числа в 16 СС в нулевом разряде имеют 0.	173	2025-05-10 19:01:34.994359	7
515	№17. Определить количество троек, для которых пятеричная запись суммы разрядов чисел представляет собой палиндром, а среднее арифметическое чисел тройки больше, чем среднее арифметическое всех чисел, кратных 31.	173	2025-05-10 19:01:43.928791	7
517	Определить мин. время, через которое завершится выполнение всей совокупности процессов, при условии, что все независимые друг от друга процессы могут выполняться параллельно.	174	2025-05-10 19:04:46.885594	7
520	Определить макс. длительность отрезка времени, в течение которого возможно одновременное выполнение трех процессов, при условии, что передвинуть можно лишь один независимый процесс.	174	2025-05-10 19:05:03.047251	7
522	Определить максимальное количество символов в непрерывной последовательности, которая начинается символами АВ, за которыми следует правильное арифметическое выражение, записанными в 3 СС.	175	2025-05-10 19:14:20.745034	7
523	Определить максимальное количество символов в непрерывной последовательности, которая является выражением вида: четное число, запятая, нечетное число.	175	2025-05-10 19:14:26.001284	7
526	Определить макс. значение, которое является результатом вычисления непрерывной последовательности, являющейся корректным арифметическим выражением, в котором отсутствует операция деления.	179	2025-05-10 19:21:57.059539	7
527	Определить макс. количество символов в непрерывной последовательности, являющейся корректным арифметическим выражением в 10 СС.	179	2025-05-10 19:22:05.844297	7
531	Определить макс. длину подстроки, не содержащей в себе букв Y, J, I, N.	179	2025-05-10 19:22:30.614651	7
535	№7. Определить максимально возможное количество цветов в палитре изображения.	57	2025-05-10 19:32:50.196887	7
536	№7. Исходный файл больше сжатого на Х%. Определить максимальное количество цвет в палитре изображения.	57	2025-05-10 19:33:01.969783	7
504	№3. Определить трек в определенном жанре, чья стоимость ближе всего к средней арифметической стоимости всех треков в указанном жанре.	171	2025-05-10 18:56:16.808421	7
505	№18. Робот забирает монету, если ее номинал четный и меньше 70. Определить максимальную и минимальную денежную сумму, которую может собрать робот.	171	2025-05-10 18:56:29.350154	7
506	№18. Определить минимальную и максимальную сумму чисел в клетках, в которых может остановиться ладья.	171	2025-05-10 18:56:38.301773	7
507	№18. Внутри поля имеются стены. Определить минимальную и максимальную сумму чисел в клетках, в которых может остановиться ладья.	171	2025-05-10 18:56:46.907724	7
508	№9. Определить количество строк, для которых выполняется: сумма четных чисел больше суммы нечетных; сумма максимального и минимального чисел больше максимального числа в файле 	173	2025-05-10 19:00:36.480263	7
509	№9. Определить количество строк, для которых выполняется: сумма четных чисел кратна 3; сумма нечетных чисел меньше среднего арифметического всех чисел.	173	2025-05-10 19:00:45.209532	7
519	Определить макс. длительность отрезка времени, в течение которого возможно одновременное выполнение хотя бы трех процессов.	174	2025-05-10 19:04:55.579235	7
524	Определить максимальное значение, которое является результатом вычисления непрерывной последовательности, являющейся корректным арифметическим выражением, в котором отсутствует операция сложения.	175	2025-05-10 19:14:30.487547	7
541	№11. В системе хранятся пароли и доп сведения о пользователях. Определить объем памяти для хранения доп сведений о каждой пользователе.	57	2025-05-10 19:33:44.996736	7
542	№11. Кодируются автомобильные номера. Определить объем памяти, необходимый для хранения N номеров.	57	2025-05-10 19:33:51.403697	7
545	№4. Условие Фано. Даны коды для некоторых букв. Определить кратчайший код для буквы З.\r\n\r\n	68	2025-05-10 19:36:23.283092	7
546	№4. Условие Фано. Даны коды для некоторых букв. Определить кратчайший код для буквы Ж.	68	2025-05-10 19:36:31.719428	7
547	№4. Условие Фано. Даны коды для некоторых букв. Определить минимальную общую длину всех кодов.	68	2025-05-10 19:36:39.064934	7
550	№4. Алгоритм Хаффмана. Даны частоты использования букв. Определить минимальную длину закодированного сообщения	68	2025-05-10 19:37:06.320042	7
557	Даны параметры фотографий, сделанных старой и новой камеры. Сколько фотографий сможет передать новая камера за 1 секунду?	69	2025-05-10 19:41:48.765135	7
558	Прибор делает фотографии и передает в центр обработки информации. Определить максимальное количество цветов в палитре.	69	2025-05-10 19:41:53.088282	7
559	Прибор делает фотографии и передает в центр обработки информации. Определить количество цветов в палитре.	69	2025-05-10 19:41:56.828496	7
562	 Определить размер звукового файла.	69	2025-05-10 19:42:12.384741	7
563	№7. Определить количество цветов в палитре без учета степени прозрачности.	172	2025-05-10 19:44:46.601177	7
566	№7. Определить количество цветов в палитре изображений, отправленных по каналу связи.	172	2025-05-10 19:45:13.40166	7
567	№7. Сколько времени потребуется для передачи изображения?	172	2025-05-10 19:45:19.80694	7
570	№7. Определить длительность звукозаписи.	172	2025-05-10 19:45:40.241308	7
574	№11. В системе хранятся пароли и доп сведения. Определить объем памяти, необходимый для хранения сведений о К пользователях.	172	2025-05-10 19:46:13.604738	7
576	Выбрать такой отрезок А, что формула тождественно истинна.\r\n🔹23:54 - Проблема шаблонов\r\n	61	2025-05-10 19:50:40.078404	7
582	Для какого наименьшего целого А формула тождественно истинна?	61	2025-05-10 19:51:27.019849	7
537	№7. При кодировании пикселя используются биты для определения степени прозрачности. Определить максимально возможное количество цветов в палитре изображения.	57	2025-05-10 19:33:09.89148	7
538	№7. Сколько фотографий сможет передать новая камера за одну секунду, если пропускную способность канала увеличить в Х раз?	57	2025-05-10 19:33:17.066348	7
544	№11. На предприятии каждой детали присваивают серийный номер. Определить максимальную длину серийного номера.	57	2025-05-10 19:34:04.033912	7
548	№4. Алгоритм кодирования повторов (RLE). Сколько байт потребуется для сжатия и кодирования числа К?	68	2025-05-10 19:36:47.418716	7
549	№4. Алгоритм RLE. Сколько байт будет содержать указанная последовательность после распаковки?	68	2025-05-10 19:36:56.504517	7
552	№11. В системе хранятся пароли. Определить объем памяти для хранения К паролей.	68	2025-05-10 19:37:59.256339	7
556	Определить количество цветов в палитре (без учета степени прозрачности).	69	2025-05-10 19:41:43.477658	7
577	Определить наименьшую длину отрезка А, при которого логическое выражение истинно.	61	2025-05-10 19:50:46.262716	7
579	Определить наименьшее произведение элементов множества А, при котором выражение истинно.	61	2025-05-10 19:50:55.088545	7
583	Одна куча камней, два варианта хода. В начальный момент в куче было S камней. Определить значения S при различных условиях.	64	2025-05-10 19:53:29.115344	7
572	№11. В системе хранятся пароли и доп сведения. Определить объем памяти, необходимый для хранения доп сведений об одном пользователе.	172	2025-05-10 19:45:55.24287	7
573	№11. В системе хранятся пароли и доп сведения. Определить объем памяти, необходимый для хранения доп сведений об одном пользователе.	172	2025-05-10 19:46:02.685156	7
575	Для какого наибольшего натурального А формула (ДЕЛ) тождественно истинна?	61	2025-05-10 19:50:35.727711	7
578	Выбрать такой отрезок А, что формула тождественно истинна.	61	2025-05-10 19:50:50.764352	7
580	Определить наибольшее натуральное А, при котором выражение (&) тождественно истинно.	61	2025-05-10 19:51:01.464683	7
581	Определить наименьшее натуральное А, при котором выражение (&) тождественно истинно.	61	2025-05-10 19:51:08.308082	7
584	Одна куча камней, три варианта хода. В начальный момент в куче было S камней. Определить значения S при различных условиях.	64	2025-05-10 19:53:33.918866	7
585	Две кучи камней, два варианта хода. В начальный момент в первой куче было 5 камней, во второй - S камней. Определить значения S при различных условиях.	64	2025-05-10 19:53:38.692251	7
586	Найти наибольшую длину отрезка А, при котором формула тождественно ложна.	71	2025-05-10 19:55:09.571402	7
587	Найти наименьшую длину отрезка А, при котором формула тождественно истинна.	71	2025-05-10 19:55:16.458212	7
588	Найти наибольшую длину отрезка А, при котором формула тождественно ложна.	71	2025-05-10 19:55:21.821234	7
589	Найти наибольшую длину отрезка А, при котором формула тождественно истинна.\r\n32:43 - Изначальное назначение алгебры логики\r\n	71	2025-05-10 19:55:30.896194	7
590	Определить наибольшее количество элементов множества А, при котором выражение истинно.	71	2025-05-10 19:55:34.538954	7
591	Определить наименьшее целое А, при котором выражение истинно.	71	2025-05-10 19:55:38.699525	7
592	Определить наименьшее целое А, при котором выражение истинно.	71	2025-05-10 19:55:42.372397	7
593	Определить наибольшее целое А, при котором выражение истинно.	71	2025-05-10 19:55:50.623504	7
594	Определить наименьшее натуральное А, такое что выражение тождественно истинно.	71	2025-05-10 19:55:55.946544	7
595	Определить наибольшее натуральное А, такое что выражение тождественно истинно.	71	2025-05-10 19:56:01.226202	7
596	Определить наибольшее натуральное А, такое что выражение тождественно истинно.\r\n	71	2025-05-10 19:56:08.516455	7
597	 Определить наибольшее натуральное А, такое что выражение (&) тождественно истинно.	176	2025-05-10 19:58:03.182888	7
598	Определить наименьшее неотрицательное А, такое что выражение (&) тождественно истинно.	176	2025-05-10 19:58:08.345663	7
599	Определить наименьшее натуральное А, такое что выражение (&) тождественно ложно.	176	2025-05-10 19:58:14.209816	7
600	Определить наибольшее натуральное А, при котором формула (ДЕЛ) тождественно истинна.	176	2025-05-10 19:58:18.67079	7
601	Определить наименьшее натуральное А, при котором формула (ДЕЛ) тождественно истинна.	176	2025-05-10 19:58:23.197356	7
602	Определить наибольшее целое неотрицательное А, при котором выражение тождественно истинно.	176	2025-05-10 19:58:28.082417	7
603	Определить наибольшее целое неотрицательное А, при выражение тождественно истинно.	176	2025-05-10 19:58:33.370331	7
604	Определить наименьшее целое неотрицательное А, при выражение тождественно истинно.	176	2025-05-10 19:58:39.084347	7
605	Определить наименьшую длину такого отрезка А, что формула истинна.	176	2025-05-10 19:58:43.685709	7
606	Одна куча камней, два варианта хода. В начальный момент в куче было S камней. Определить минимальное S, при котором В выиграл своим первым ходом после неудачного первого хода П.	178	2025-05-10 20:00:53.892633	7
607	Одна куча камней, три варианта хода. После каждого хода в куче должно быть четное количество камней. В начальный момент в куче было S камней. Определить минимальное S, при котором В выиграл своим первым ходом при любой игре П.	178	2025-05-10 20:01:01.931454	7
608	Одна куча камней, три варианта хода. В начальный момент в куче было S камней. Определить минимальное S, при котором В выиграл своим первым ходом после неудачного первого хода П.	178	2025-05-10 20:01:07.786564	7
609	Две кучи камней, два варианта хода. В начальный момент в первой куче было 8 камней, во второй - S. Определить минимальное S, при котором В выиграл своим первым ходом после неудачного первого хода П.	178	2025-05-10 20:01:14.876617	7
610	Две кучи камней, два варианта хода. В начальный момент в первой куче было 9 камней, во второй - S. Определить минимальное S, при котором В выиграл своим первым ходом после неудачного первого хода П.	178	2025-05-10 20:01:21.537077	7
611	Две кучи камней, два варианта хода. В начальный момент в первой куче было 10 камней, во второй - S. Определить минимальное S, при котором В выиграл своим первым ходом после неудачного первого хода П.	178	2025-05-10 20:01:27.221236	7
617	Определить максимальное количество символов в непрерывной последовательности, которая является арифметическим выражением, содержащим не более 10 знаков, с целыми числами, кратными 25.	181	2025-05-10 20:03:12.938341	7
622	№5. Автомат обрабатывает натуральное N по алгоритму: строится двоичная запись N и дописываются разряды по правилу. При каком N<750 может получиться четное R, не кратное 4?	77	2025-05-10 20:05:35.908673	7
623	№10. Сколько раз в тексте встречаются слова с сочетанием букв удар?	77	2025-05-10 20:05:49.114074	7
628	Два узла, находящиеся в одной сети, имеют заданные IP-адреса. Определить наименьшее количество адресов в этой сети.	177	2025-05-10 20:20:30.563356	7
631	По заданным IP-адресу и адресу сети определить минимальное количество единиц в записи маски.	177	2025-05-10 20:20:45.265647	7
612	Две кучи камней, два варианта хода. В начальный момент в первой куче было 25 камней, во второй - S. Определить минимальное S, при котором В выиграл своим первым ходом после неудачного первого хода П.	178	2025-05-10 20:01:32.547061	7
615	Найти Самую длинную подстроку, которая может являться числом в 20 СС.	181	2025-05-10 20:03:04.952406	7
618	Определить максимальное значение, которое является результатом вычисления непрерывной последовательности, являющейся арифметическим выражением с числами, в котором отсутствует операция деления.	181	2025-05-10 20:03:16.63181	7
619	№2. Определить, какому столбцу таблицы истинности функции F соответствует каждая из переменных.	77	2025-05-10 20:05:15.623658	7
620	№2. Определить, какому столбцу таблицы истинности функции F соответствует каждая из переменных.	77	2025-05-10 20:05:21.58739	7
625	По заданным маске подсети и IP-адресу компьютера в сети определить номер компьютера.	177	2025-05-10 20:20:15.419284	7
627	По заданным IP-адресу и маске определить количество узлов, для которых количество нулей в записи IP-адреса больше 12.	177	2025-05-10 20:20:26.735436	7
632	По заданным IP-адресу и адресу сети определить количество возможных значений третьего слева байта маски.	177	2025-05-10 20:20:51.571313	7
635	Сколько существует программ, преобразующих число 13 в 52, если вторая и третья команды не могут идти друг за другом, а также повторяться может только первая команда?	182	2025-05-10 20:22:23.910959	7
613	Две кучи камней, два варианта хода. В начальный момент в первой куче было 90 камней, во второй - S. Определить минимальное S, при котором В выиграл своим первым ходом после неудачного первого хода П.	178	2025-05-10 20:01:36.380836	7
614	Определить максимальное количество идущих подряд символов, среди которых каждая из букв F, L встречается не более 3 раз.	181	2025-05-10 20:03:00.822293	7
616	Определить длину минимальной подстроки, содержащей не менее 100 символов Y.	181	2025-05-10 20:03:09.076375	7
621	№5. Автомат обрабатывает натуральное N по алгоритму: строится двоичная запись N и дописываются разряды по правилу. Какое наибольшее R<50 может получиться в результате?	77	2025-05-10 20:05:28.303885	7
624	По заданным маске подсети и IP-адресу компьютера в сети определить номер компьютера.	177	2025-05-10 20:20:04.79475	7
626	По заданным IP-адресу и адресу сети определить минимальное количество адресов в этой сети.	177	2025-05-10 20:20:21.81337	7
629	По заданным IP-адресу и маске определить адрес сети.	177	2025-05-10 20:20:34.821508	7
630	 По заданным IP-адресу и маске определить количество нулей в записи адреса сети.	177	2025-05-10 20:20:40.816527	7
633	Сколько существует программ, преобразующих число 1 в 824, траектория вычисления которых содержит 21 и 68, причем можно использовать ту команду, чей номер отличается на 1 от предыдущей?	182	2025-05-10 20:22:15.120471	7
634	Сколько различных результатов можно получить при исходном числе 16 в результате выполнения программы, содержащей 10 команд, если нельзя повторять третью команду два раза подряд?	182	2025-05-10 20:22:19.235763	7
640	Определить, на какую цифру оканчивается число	191	2025-07-06 11:43:48.324646	11
\.


--
-- Data for Name: webinar_task_association; Type: TABLE DATA; Schema: public; Owner: cyberorg
--

COPY public.webinar_task_association (webinar_id, task_number_id) FROM stdin;
11	7
12	11
12	7
13	8
14	9
15	8
16	3
17	15
17	2
18	15
20	21
20	19
20	20
21	14
21	2
21	5
22	13
22	1
22	4
23	24
24	14
25	23
25	16
26	21
26	19
26	20
27	15
28	17
29	22
29	18
30	25
31	25
32	8
32	6
33	15
34	9
34	3
35	22
35	18
36	13
36	1
36	4
36	10
37	14
37	5
37	12
38	13
38	2
38	8
39	21
39	19
39	20
40	21
40	16
40	19
40	20
41	24
42	7
43	25
44	6
44	5
45	14
46	15
47	8
48	25
48	24
49	17
49	8
49	12
50	13
51	21
51	19
51	20
52	17
53	22
53	18
54	24
55	8
55	2
55	5
55	6
56	25
57	11
57	7
58	12
59	9
60	24
61	15
62	8
63	23
63	16
64	21
64	19
64	20
65	9
65	3
66	9
67	13
68	11
68	4
69	7
70	22
70	18
71	15
72	25
72	8
73	24
74	23
74	16
75	12
75	1
75	6
76	17
76	13
77	10
77	2
77	5
78	22
78	3
79	24
80	26
81	26
82	26
83	26
84	26
85	26
86	26
87	26
88	26
89	26
90	26
91	26
92	26
93	26
94	26
95	26
96	26
97	27
98	27
99	27
100	27
101	27
102	27
103	27
104	27
105	27
106	27
107	27
108	27
109	27
110	27
111	27
112	27
113	27
114	27
115	27
116	27
117	27
118	27
119	27
120	27
121	27
122	27
123	27
124	27
125	27
126	27
127	27
128	27
129	27
130	27
131	27
132	27
133	27
134	27
135	27
136	27
137	27
138	27
152	7
153	8
154	22
154	3
154	9
154	18
155	11
155	4
156	15
157	17
158	25
158	24
159	11
160	13
161	8
162	15
163	9
164	13
164	1
164	3
164	4
164	10
165	15
165	7
165	8
165	11
166	14
166	2
166	5
166	6
166	8
166	12
167	22
167	3
167	9
167	18
168	25
168	9
168	17
168	24
169	23
169	16
169	19
169	20
169	21
170	27
170	26
171	18
171	3
172	11
172	7
173	17
173	9
174	22
175	24
176	15
177	13
178	21
178	19
178	20
179	24
181	24
182	23
183	26
184	26
185	26
186	26
187	26
188	26
189	26
190	26
199	24
201	27
202	27
203	26
204	26
198	9
195	17
196	17
206	8
207	7
208	11
208	7
209	18
209	3
210	9
211	17
211	9
212	8
213	13
214	5
214	12
215	15
216	10
216	1
216	4
217	14
217	6
219	24
218	25
220	24
221	23
221	16
222	21
222	19
222	20
227	26
228	26
229	26
232	10
233	10
236	4
237	4
238	9
240	9
242	1
243	6
244	1
245	2
246	6
247	2
\.


--
-- Name: known_task_number_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.known_task_number_id_seq', 281, true);


--
-- Name: maintenance_mode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.maintenance_mode_id_seq', 1, true);


--
-- Name: oge_parallel_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.oge_parallel_plan_id_seq', 2, true);


--
-- Name: oge_parallel_plan_slot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.oge_parallel_plan_slot_id_seq', 4, true);


--
-- Name: oge_parallel_plan_topic_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.oge_parallel_plan_topic_order_id_seq', 1, false);


--
-- Name: oge_parallel_plan_webinar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.oge_parallel_plan_webinar_id_seq', 8, true);


--
-- Name: oge_topic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.oge_topic_id_seq', 8, true);


--
-- Name: oge_topic_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.oge_topic_order_id_seq', 8, true);


--
-- Name: planned_webinar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.planned_webinar_id_seq', 376, true);


--
-- Name: student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.student_id_seq', 33, true);


--
-- Name: study_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.study_plan_id_seq', 24, true);


--
-- Name: task_number_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.task_number_id_seq', 27, true);


--
-- Name: update_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.update_notification_id_seq', 1, true);


--
-- Name: update_notification_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.update_notification_image_id_seq', 17, true);


--
-- Name: user_notification_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.user_notification_status_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.users_id_seq', 33, true);


--
-- Name: watched_webinar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.watched_webinar_id_seq', 661, true);


--
-- Name: webinar_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.webinar_comment_id_seq', 167, true);


--
-- Name: webinar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.webinar_id_seq', 259, true);


--
-- Name: webinar_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cyberorg
--

SELECT pg_catalog.setval('public.webinar_task_id_seq', 640, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: known_task_number known_task_number_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.known_task_number
    ADD CONSTRAINT known_task_number_pkey PRIMARY KEY (id);


--
-- Name: maintenance_mode maintenance_mode_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.maintenance_mode
    ADD CONSTRAINT maintenance_mode_pkey PRIMARY KEY (id);


--
-- Name: oge_parallel_plan oge_parallel_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan
    ADD CONSTRAINT oge_parallel_plan_pkey PRIMARY KEY (id);


--
-- Name: oge_parallel_plan_slot oge_parallel_plan_slot_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_slot
    ADD CONSTRAINT oge_parallel_plan_slot_pkey PRIMARY KEY (id);


--
-- Name: oge_parallel_plan_topic_order oge_parallel_plan_topic_order_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_topic_order
    ADD CONSTRAINT oge_parallel_plan_topic_order_pkey PRIMARY KEY (id);


--
-- Name: oge_parallel_plan_webinar oge_parallel_plan_webinar_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_webinar
    ADD CONSTRAINT oge_parallel_plan_webinar_pkey PRIMARY KEY (id);


--
-- Name: oge_topic_order oge_topic_order_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_topic_order
    ADD CONSTRAINT oge_topic_order_pkey PRIMARY KEY (id);


--
-- Name: oge_topic oge_topic_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_topic
    ADD CONSTRAINT oge_topic_pkey PRIMARY KEY (id);


--
-- Name: planned_webinar planned_webinar_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.planned_webinar
    ADD CONSTRAINT planned_webinar_pkey PRIMARY KEY (id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (id);


--
-- Name: study_plan study_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.study_plan
    ADD CONSTRAINT study_plan_pkey PRIMARY KEY (id);


--
-- Name: task_number task_number_number_key; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.task_number
    ADD CONSTRAINT task_number_number_key UNIQUE (number);


--
-- Name: task_number task_number_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.task_number
    ADD CONSTRAINT task_number_pkey PRIMARY KEY (id);


--
-- Name: update_notification_image update_notification_image_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.update_notification_image
    ADD CONSTRAINT update_notification_image_pkey PRIMARY KEY (id);


--
-- Name: update_notification update_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.update_notification
    ADD CONSTRAINT update_notification_pkey PRIMARY KEY (id);


--
-- Name: oge_parallel_plan_slot uq_oge_parallel_plan_slot; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_slot
    ADD CONSTRAINT uq_oge_parallel_plan_slot UNIQUE (plan_id, slot_number);


--
-- Name: oge_parallel_plan_webinar uq_oge_parallel_plan_webinar; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_webinar
    ADD CONSTRAINT uq_oge_parallel_plan_webinar UNIQUE (plan_id, webinar_id);


--
-- Name: oge_parallel_plan_topic_order uq_oge_plan_topic_order_topic; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_topic_order
    ADD CONSTRAINT uq_oge_plan_topic_order_topic UNIQUE (plan_id, topic_id);


--
-- Name: oge_topic_order uq_oge_topic_order_topic; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_topic_order
    ADD CONSTRAINT uq_oge_topic_order_topic UNIQUE (topic_id);


--
-- Name: user_notification_status uq_user_notification; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.user_notification_status
    ADD CONSTRAINT uq_user_notification UNIQUE (user_id, notification_id);


--
-- Name: webinar uq_webinar_url; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar
    ADD CONSTRAINT uq_webinar_url UNIQUE (url);


--
-- Name: user_notification_status user_notification_status_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.user_notification_status
    ADD CONSTRAINT user_notification_status_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: watched_webinar watched_webinar_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.watched_webinar
    ADD CONSTRAINT watched_webinar_pkey PRIMARY KEY (id);


--
-- Name: webinar_comment webinar_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_comment
    ADD CONSTRAINT webinar_comment_pkey PRIMARY KEY (id);


--
-- Name: webinar_oge_topic_association webinar_oge_topic_association_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_oge_topic_association
    ADD CONSTRAINT webinar_oge_topic_association_pkey PRIMARY KEY (webinar_id, oge_topic_id);


--
-- Name: webinar webinar_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar
    ADD CONSTRAINT webinar_pkey PRIMARY KEY (id);


--
-- Name: webinar_task_association webinar_task_association_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_task_association
    ADD CONSTRAINT webinar_task_association_pkey PRIMARY KEY (webinar_id, task_number_id);


--
-- Name: webinar_task webinar_task_pkey; Type: CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_task
    ADD CONSTRAINT webinar_task_pkey PRIMARY KEY (id);


--
-- Name: ix_student_first_name; Type: INDEX; Schema: public; Owner: cyberorg
--

CREATE INDEX ix_student_first_name ON public.student USING btree (first_name);


--
-- Name: ix_student_last_name; Type: INDEX; Schema: public; Owner: cyberorg
--

CREATE INDEX ix_student_last_name ON public.student USING btree (last_name);


--
-- Name: ix_student_platform_id; Type: INDEX; Schema: public; Owner: cyberorg
--

CREATE INDEX ix_student_platform_id ON public.student USING btree (platform_id);


--
-- Name: known_task_number known_task_number_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.known_task_number
    ADD CONSTRAINT known_task_number_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(id);


--
-- Name: maintenance_mode maintenance_mode_enabled_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.maintenance_mode
    ADD CONSTRAINT maintenance_mode_enabled_by_id_fkey FOREIGN KEY (enabled_by_id) REFERENCES public.users(id);


--
-- Name: oge_parallel_plan oge_parallel_plan_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan
    ADD CONSTRAINT oge_parallel_plan_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.users(id);


--
-- Name: oge_parallel_plan_slot oge_parallel_plan_slot_current_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_slot
    ADD CONSTRAINT oge_parallel_plan_slot_current_topic_id_fkey FOREIGN KEY (current_topic_id) REFERENCES public.oge_topic(id);


--
-- Name: oge_parallel_plan_slot oge_parallel_plan_slot_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_slot
    ADD CONSTRAINT oge_parallel_plan_slot_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.oge_parallel_plan(id);


--
-- Name: oge_parallel_plan oge_parallel_plan_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan
    ADD CONSTRAINT oge_parallel_plan_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(id);


--
-- Name: oge_parallel_plan_topic_order oge_parallel_plan_topic_order_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_topic_order
    ADD CONSTRAINT oge_parallel_plan_topic_order_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.oge_parallel_plan(id);


--
-- Name: oge_parallel_plan_topic_order oge_parallel_plan_topic_order_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_topic_order
    ADD CONSTRAINT oge_parallel_plan_topic_order_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.oge_topic(id);


--
-- Name: oge_parallel_plan_webinar oge_parallel_plan_webinar_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_webinar
    ADD CONSTRAINT oge_parallel_plan_webinar_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.oge_parallel_plan(id);


--
-- Name: oge_parallel_plan_webinar oge_parallel_plan_webinar_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_webinar
    ADD CONSTRAINT oge_parallel_plan_webinar_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.oge_topic(id);


--
-- Name: oge_parallel_plan_webinar oge_parallel_plan_webinar_webinar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_parallel_plan_webinar
    ADD CONSTRAINT oge_parallel_plan_webinar_webinar_id_fkey FOREIGN KEY (webinar_id) REFERENCES public.webinar(id);


--
-- Name: oge_topic_order oge_topic_order_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.oge_topic_order
    ADD CONSTRAINT oge_topic_order_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.oge_topic(id);


--
-- Name: planned_webinar planned_webinar_study_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.planned_webinar
    ADD CONSTRAINT planned_webinar_study_plan_id_fkey FOREIGN KEY (study_plan_id) REFERENCES public.study_plan(id);


--
-- Name: planned_webinar planned_webinar_webinar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.planned_webinar
    ADD CONSTRAINT planned_webinar_webinar_id_fkey FOREIGN KEY (webinar_id) REFERENCES public.webinar(id);


--
-- Name: study_plan study_plan_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.study_plan
    ADD CONSTRAINT study_plan_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.users(id);


--
-- Name: study_plan study_plan_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.study_plan
    ADD CONSTRAINT study_plan_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(id);


--
-- Name: update_notification update_notification_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.update_notification
    ADD CONSTRAINT update_notification_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.users(id);


--
-- Name: update_notification_image update_notification_image_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.update_notification_image
    ADD CONSTRAINT update_notification_image_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.update_notification(id);


--
-- Name: user_notification_status user_notification_status_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.user_notification_status
    ADD CONSTRAINT user_notification_status_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.update_notification(id);


--
-- Name: user_notification_status user_notification_status_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.user_notification_status
    ADD CONSTRAINT user_notification_status_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: watched_webinar watched_webinar_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.watched_webinar
    ADD CONSTRAINT watched_webinar_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.users(id);


--
-- Name: watched_webinar watched_webinar_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.watched_webinar
    ADD CONSTRAINT watched_webinar_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(id);


--
-- Name: watched_webinar watched_webinar_webinar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.watched_webinar
    ADD CONSTRAINT watched_webinar_webinar_id_fkey FOREIGN KEY (webinar_id) REFERENCES public.webinar(id);


--
-- Name: webinar_comment webinar_comment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_comment
    ADD CONSTRAINT webinar_comment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: webinar_comment webinar_comment_webinar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_comment
    ADD CONSTRAINT webinar_comment_webinar_id_fkey FOREIGN KEY (webinar_id) REFERENCES public.webinar(id);


--
-- Name: webinar webinar_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar
    ADD CONSTRAINT webinar_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.users(id);


--
-- Name: webinar_oge_topic_association webinar_oge_topic_association_oge_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_oge_topic_association
    ADD CONSTRAINT webinar_oge_topic_association_oge_topic_id_fkey FOREIGN KEY (oge_topic_id) REFERENCES public.oge_topic(id);


--
-- Name: webinar_oge_topic_association webinar_oge_topic_association_webinar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_oge_topic_association
    ADD CONSTRAINT webinar_oge_topic_association_webinar_id_fkey FOREIGN KEY (webinar_id) REFERENCES public.webinar(id);


--
-- Name: webinar_task_association webinar_task_association_task_number_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_task_association
    ADD CONSTRAINT webinar_task_association_task_number_id_fkey FOREIGN KEY (task_number_id) REFERENCES public.task_number(id);


--
-- Name: webinar_task_association webinar_task_association_webinar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_task_association
    ADD CONSTRAINT webinar_task_association_webinar_id_fkey FOREIGN KEY (webinar_id) REFERENCES public.webinar(id);


--
-- Name: webinar_task webinar_task_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_task
    ADD CONSTRAINT webinar_task_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.users(id);


--
-- Name: webinar_task webinar_task_webinar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cyberorg
--

ALTER TABLE ONLY public.webinar_task
    ADD CONSTRAINT webinar_task_webinar_id_fkey FOREIGN KEY (webinar_id) REFERENCES public.webinar(id);


--
-- PostgreSQL database dump complete
--

