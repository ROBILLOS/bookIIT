PGDMP     (    ;            	    v            BookIIT    10.5    10.5                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            	           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            
           1262    16426    BookIIT    DATABASE     �   CREATE DATABASE "BookIIT" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE "BookIIT";
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false                       0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false                       0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16427    account    TABLE     �   CREATE TABLE public.account (
    acc_id character varying NOT NULL,
    acc_type integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL
);
    DROP TABLE public.account;
       public         postgres    false    3            �            1259    16451 	   admin_acc    TABLE     �   CREATE TABLE public.admin_acc (
    admin_id character varying(8) NOT NULL,
    fname character varying NOT NULL,
    lname character varying NOT NULL,
    college character varying NOT NULL,
    contact character varying NOT NULL
);
    DROP TABLE public.admin_acc;
       public         postgres    false    3            �            1259    16443    user_acc    TABLE     �   CREATE TABLE public.user_acc (
    user_id character varying(8) NOT NULL,
    fname character varying,
    lname character varying,
    contact character varying
);
    DROP TABLE public.user_acc;
       public         postgres    false    3            �            1259    16461    venue    TABLE     �   CREATE TABLE public.venue (
    venue_id integer NOT NULL,
    admin_id character varying NOT NULL,
    location character varying NOT NULL,
    rate integer NOT NULL,
    v_info character varying
);
    DROP TABLE public.venue;
       public         postgres    false    3            �            1259    16459    venue_venue_id_seq    SEQUENCE     �   CREATE SEQUENCE public.venue_venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.venue_venue_id_seq;
       public       postgres    false    200    3                       0    0    venue_venue_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.venue_venue_id_seq OWNED BY public.venue.venue_id;
            public       postgres    false    199            ~
           2604    16464    venue venue_id    DEFAULT     p   ALTER TABLE ONLY public.venue ALTER COLUMN venue_id SET DEFAULT nextval('public.venue_venue_id_seq'::regclass);
 =   ALTER TABLE public.venue ALTER COLUMN venue_id DROP DEFAULT;
       public       postgres    false    200    199    200                       0    16427    account 
   TABLE DATA               N   COPY public.account (acc_id, acc_type, username, email, password) FROM stdin;
    public       postgres    false    196   �                 0    16451 	   admin_acc 
   TABLE DATA               M   COPY public.admin_acc (admin_id, fname, lname, college, contact) FROM stdin;
    public       postgres    false    198                    0    16443    user_acc 
   TABLE DATA               B   COPY public.user_acc (user_id, fname, lname, contact) FROM stdin;
    public       postgres    false    197   7                 0    16461    venue 
   TABLE DATA               K   COPY public.venue (venue_id, admin_id, location, rate, v_info) FROM stdin;
    public       postgres    false    200   T                  0    0    venue_venue_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.venue_venue_id_seq', 1, false);
            public       postgres    false    199            �
           2606    16434    account account_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (acc_id);
 >   ALTER TABLE ONLY public.account DROP CONSTRAINT account_pkey;
       public         postgres    false    196            �
           2606    16458    admin_acc admin_acc_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.admin_acc
    ADD CONSTRAINT admin_acc_pkey PRIMARY KEY (admin_id);
 B   ALTER TABLE ONLY public.admin_acc DROP CONSTRAINT admin_acc_pkey;
       public         postgres    false    198            �
           2606    16450    user_acc user_acc_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.user_acc
    ADD CONSTRAINT user_acc_pkey PRIMARY KEY (user_id);
 @   ALTER TABLE ONLY public.user_acc DROP CONSTRAINT user_acc_pkey;
       public         postgres    false    197            �
           2606    16469    venue venue_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (venue_id);
 :   ALTER TABLE ONLY public.venue DROP CONSTRAINT venue_pkey;
       public         postgres    false    200                   x������ � �            x������ � �            x������ � �            x������ � �     