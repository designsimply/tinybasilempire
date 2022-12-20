-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS basil_links_id_seq;

-- Table Definition
CREATE TABLE "basil_links" (
    "id" int8 NOT NULL DEFAULT nextval('basil_links_id_seq'::regclass),
    "url" text,
    "title" varchar(120) NOT NULL DEFAULT ''::character varying,
    "description" text,
    "datecreated" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "lastmodified" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "datedeleted" timestamptz,
    PRIMARY KEY ("id")
);

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS basil_tags_tag_id_seq;

-- Table Definition
CREATE TABLE "basil_tags" (
    "tag_id" int8 NOT NULL DEFAULT nextval('basil_tags_tag_id_seq'::regclass),
    "name" varchar(64) NOT NULL,
    PRIMARY KEY ("tag_id")
);

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS basil_tagmap_tagmap_id_seq;

-- Table Definition
CREATE TABLE "basil_tagmap" (
    "tagmap_id" int8 NOT NULL DEFAULT nextval('basil_tagmap_tagmap_id_seq'::regclass),
    "link_id" int8 NOT NULL,
    "tag_id" int8 NOT NULL,
    PRIMARY KEY ("tagmap_id")
);

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS basil_users_id_seq;

-- Table Definition
CREATE TABLE "basil_users" (
    "id" int4 NOT NULL DEFAULT nextval('basil_users_id_seq'::regclass),
    "email" text NOT NULL,
    "name" text,
    "profile_pic" text,
    PRIMARY KEY ("id")
);