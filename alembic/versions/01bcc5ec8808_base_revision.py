"""base revision

Revision ID: 01bcc5ec8808
Revises: 
Create Date: 2020-07-12 20:14:57.019779

"""
from alembic import op
import sqlalchemy as sa
from psycopg2 import InternalError
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '01bcc5ec8808'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("SET statement_timeout = 0;")
    op.execute("SET lock_timeout = 0;")
    op.execute("SET idle_in_transaction_session_timeout = 0;")
    op.execute("SET client_encoding = 'UTF8';")
    op.execute("SET standard_conforming_strings = on;")
    op.execute("SET check_function_bodies = false;")
    op.execute("SET xmloption = content;")
    op.execute("SET client_min_messages = warning;")
    op.execute("SET row_security = off;")

    '''
    try:
        op.execute("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;")
        op.execute("COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';")
    except InternalError as e:
        print(e.pgerror)

    try:
        op.execute("CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;")
        op.execute("COMMENT ON EXTENSION pg_stat_statements IS 'track execution statistics of all SQL statements executed';")
    except InternalError as e:
        print(e.pgerror)

    try:
        op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;")
        op.execute("COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';")
    except InternalError as e:
        print(e.pgerror)
    '''

    op.execute("SET default_tablespace = '';")
    op.execute("SET default_table_access_method = heap;")

    # region Create Tables
    op.create_table('titles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_before', sa.Boolean(), nullable=False, server_default='true'),
    sa.Column('text', sa.String(length=64), nullable=True),
    sa.Column('qualification_expr', sa.String(length=256), nullable=True),
    sa.Column('requirement_string', sa.String(length=512), nullable=True),
    sa.Column('color', sa.String(length=6), nullable=True, server_default='000000'),
    sa.Column('kind', sa.Integer(), nullable=True, server_default='1'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('passhash', sa.String(length=255), nullable=False),
    sa.Column('created_utc', sa.Integer(), nullable=False),
    sa.Column('admin_level', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('over_18', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('creation_ip', sa.String(length=255), nullable=True),
    sa.Column('hide_offensive', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('is_activated', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('reddit_username', sa.String(length=64), nullable=True, server_default=text('NULL::character varying')),
    sa.Column('bio', sa.String(length=256), nullable=True, server_default=''),
    sa.Column('bio_html', sa.String(length=300), nullable=True),
    sa.Column('real_id', sa.String(), nullable=True),
    sa.Column('referred_by', sa.Integer(), nullable=True),
    sa.Column('is_banned', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('ban_reason', sa.String(length=128), nullable=True, server_default=''),
    sa.Column('ban_state', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('login_nonce', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('title_id', sa.Integer(), nullable=True),
    sa.Column('has_banner', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('has_profile', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('reserved', sa.String(length=256), nullable=True, server_default=text('NULL::character varying')),
    sa.Column('is_nsfw', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('tos_agreed_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('profile_nonce', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('banner_nonce', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('last_siege_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('mfa_secret', sa.String(length=32), nullable=True, server_default=text('NULL::character varying')),
    sa.Column('has_earned_darkmode', sa.Boolean(), nullable=True),
    sa.Column('is_private', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('read_announcement_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('feed_nonce', sa.Integer(), nullable=True, server_default='1'),
    sa.Column('discord_id', sa.Integer(), nullable=True),
    sa.Column('show_nsfl', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('karma', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('comment_karma', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('unban_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('is_deleted', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('delete_reason', sa.String(length=1000), nullable=True, server_default=''),
    sa.Column('patreon_id', sa.String(length=64), nullable=True),
    sa.Column('patreon_access_token', sa.String(length=128), nullable=True),
    sa.Column('patreon_refresh_token', sa.String(length=128), nullable=True),
    sa.Column('patreon_pledge_cents', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['referred_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['title_id'], ['titles.id'], ),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('reddit_username'),
    sa.UniqueConstraint('username'),
    sa.Index('users_is_deleted_idx', 'is_deleted'),
    sa.Index('users_created_utc_idx', 'created_utc'),
    sa.Index('users_title_id_idx', 'title_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('alts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user1', sa.Integer(), nullable=True),
    sa.Column('user2', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user1'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user2'], ['users.id'], ),
    sa.Index('alts_user1_idx', 'user1'),
    sa.Index('alts_user2_idx', 'user2'),
    sa.UniqueConstraint('user1', 'user2'),
    sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('badge_defs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('icon', sa.String(length=64), nullable=True),
    sa.Column('kind', sa.Integer(), nullable=True, server_default='1'),
    sa.Column('rank', sa.Integer(), nullable=True, server_default='1'),
    sa.Column('qualification_expr', sa.String(length=128), nullable=True),
    sa.UniqueConstraint('icon'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('badges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('badge_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True, server_default=''),
    sa.Column('url', sa.String(length=256), nullable=True, server_default=''),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['badge_id'], ['badge_defs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('badges_user_idx', 'user_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('badpics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True, server_default=''),
    sa.Column('phash', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('badwords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(length=64), nullable=True),
    sa.Column('regex', sa.String(length=256), nullable=True),
    sa.UniqueConstraint('keyword'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('boards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=1500), nullable=True, server_default=''),
    sa.Column('description_html', sa.String(length=2500), nullable=True, server_default=''),
    sa.Column('over_18', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('has_banner', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('has_profile', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('ban_reason', sa.String(length=256), nullable=True, server_default=text('NULL::character varying')),
    sa.Column('color', sa.String(length=8), nullable=True, server_default='603abb'),
    sa.Column('downvotes_disabled', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('restricted_posting', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('hide_banner_data', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('profile_nonce', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('banner_nonce', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('is_private', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('color_nonce', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('is_nsfl', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('rank_trending', sa.Float(), nullable=True, server_default=text('0')),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.UniqueConstraint('name'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('bans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.Column('banning_mod_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
    sa.Column('mod_note', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['banning_mod_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('ban_board_idx', 'board_id'),
    sa.Index('ban_user_idx', 'user_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=100), nullable=True),
    sa.Column('can_submit', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('can_comment', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('reason', sa.Integer(), nullable=True),
    sa.Column('show_thumbnail', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('embed_function', sa.String(length=64), nullable=True, server_default=text('NULL::character varying')),
    sa.UniqueConstraint('domain'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=False),
    sa.Column('is_banned', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('over_18', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('distinguish_level', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('created_str', sa.String(length=255), nullable=True),
    sa.Column('stickied', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('board_id', sa.Integer(), nullable=True, server_default='1'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('domain_ref', sa.Integer(), nullable=True),
    sa.Column('is_approved', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('approved_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('original_board_id', sa.Integer(), nullable=True),
    sa.Column('edited_utc', sa.Integer(), nullable=True),
    sa.Column('creation_ip', sa.String(length=64), nullable=False, server_default=''),
    sa.Column('mod_approved', sa.Integer(), nullable=True),
    sa.Column('is_image', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('has_thumb', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('accepted_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('post_public', sa.Boolean(), nullable=True, server_default='true'),
    sa.Column('score_hot', sa.Float(), nullable=True, server_default=text('0')),
    sa.Column('score_top', sa.Integer(), nullable=True, server_default=text('0')),
    sa.Column('score_activity', sa.Float(), nullable=True, server_default=text('0')),
    sa.Column('score_disputed', sa.Float(), nullable=True, server_default=text('0')),
    sa.Column('is_offensive', sa.Boolean(), nullable=True),
    sa.Column('is_pinned', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('is_nsfl', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('repost_id', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('score_best', sa.Float(), nullable=True, server_default=text('0')),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['domain_ref'], ['domains.id'], ),
    sa.ForeignKeyConstraint(['is_approved'], ['users.id'], ),
    sa.ForeignKeyConstraint(['original_board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['repost_id'], ['submissions.id'], ),
    sa.Index('submissions_domain_ref_idx', 'domain_ref'),
    sa.Index('submissions_over_18_idx', 'over_18'),
    sa.Index('submissions_author_id_idx', 'author_id'),
    sa.Index('submissions_is_offensive_idx', 'is_offensive'),
    sa.Index('submissions_is_pinned_idx', 'is_pinned'),
    sa.Index('submissions_board_id_idx', 'board_id'),
    sa.Index('submissions_stickied_idx', 'stickied'),
    sa.Index('submissions_created_utc_idx', 'created_utc', postgresql_ops={'created_utc': 'DESC'}),
    sa.Index('submissions_binary_group_idx', 'is_banned', 'is_deleted', 'over_18'),
    sa.Index('submissions_activity_disputed_idx', 'score_disputed', 'board_id', postgresql_ops={'score_disputed': 'DESC'}),
    sa.Index('submissions_activity_hot_idx', 'score_hot', 'board_id', postgresql_ops={'score_hot': 'DESC'}),
    sa.Index('submissions_activity_sort_idx', 'score_activity', 'board_id', postgresql_ops={'score_activity': 'DESC'}),
    sa.Index('submissions_activity_top_idx', 'score_top', 'board_id', postgresql_ops={'score_top': 'DESC'}),
    sa.Index('submissions_activity_best_idx', 'score_best', 'board_id', postgresql_ops={'score_best': 'DESC'}),
    sa.Index('submissions_disputed_sort_idx', 'is_banned', 'is_deleted', 'score_disputed', 'over_18', postgresql_ops={'score_disputed': 'DESC'}),
    sa.Index('submissions_hot_sort_idx', 'is_banned', 'is_deleted', 'score_hot', 'over_18', postgresql_ops={'score_hot': 'DESC'}),
    sa.Index('submissions_new_sort_idx', 'is_banned', 'is_deleted', 'created_utc', 'over_18', postgresql_ops={'created_utc': 'DESC'}),
    sa.Index('submissions_trending_all_idx', 'is_banned', 'is_deleted', 'stickied', 'over_18', postgresql_ops={'stickied': 'DESC'}),
    sa.Index('submissions_time_board_idx', 'created_utc', 'board_id', postgresql_where=text('created_utc > 1590859918')),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=False),
    sa.Column('parent_submission', sa.Integer(), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('parent_fullname', sa.String(length=255), nullable=True),
    sa.Column('distinguish_level', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('edited_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('is_approved', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('author_name', sa.String(length=64), nullable=True),
    sa.Column('approved_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('creation_ip', sa.String(length=64), nullable=False, server_default=''),
    sa.Column('score_disputed', sa.Float(), nullable=True, server_default=text('0')),
    sa.Column('score_hot', sa.Float(), nullable=True, server_default=text('0')),
    sa.Column('score_top', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('level', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('parent_comment_id', sa.Integer(), nullable=True),
    sa.Column('title_id', sa.Integer(), nullable=True),
    sa.Column('over_18', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('is_op', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('is_offensive', sa.Boolean(), nullable=True),
    sa.Column('is_nsfl', sa.Boolean(), nullable=True, server_default='false'),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['parent_submission'], ['submissions.id'], ),
    sa.Index('comments_parent_idx', 'parent_comment_id'),
    sa.Index('comments_post_id_idx', 'parent_submission'),
    sa.Index('comments_loader_idx', 'parent_submission', 'level', 'score_hot', postgresql_ops={'score_hot': 'DESC'}, postgresql_where=text('level <= 8')),
    sa.Index('comments_score_disupted_idx', 'score_disputed', postgresql_ops={'score_disputed': 'DESC'}),
    sa.Index('comments_score_hot_idx', 'score_hot', postgresql_ops={'score_hot': 'DESC'}),
    sa.Index('comments_score_top_idx', 'score_top', postgresql_ops={'score_top': 'DESC'}),
    sa.Index('comments_user_idx', 'author_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('commentflags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('commentflags_user_idx', 'user_id'),
    sa.Index('commentflags_comment_idx', 'comment_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('comments_aux',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=10000), nullable=True),
    sa.Column('body_html', sa.String(length=20000), nullable=True),
    sa.Column('ban_reason', sa.String(length=128), nullable=True),
    sa.Column('key_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['comments.id'], ),
    sa.Index('comments_aux_id_idx', 'id'),
    sa.PrimaryKeyConstraint('key_id')
    )

    op.create_table('commentvotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('vote_type', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('commentvotes_comment_id_idx', 'comment_id'),
    sa.Index('commentvotes_comment_type_idx', 'vote_type'),
    sa.Index('commentvotes_user_id_idx', 'user_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('contributors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
    sa.Column('approving_mod_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['approving_mod_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('contributors_active_idx', 'is_active'),
    sa.Index('contributors_board_idx', 'board_id'),
    sa.Index('contributors_user_idx', 'user_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('dms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.Column('to_user_id', sa.Integer(), nullable=True),
    sa.Column('from_user_id', sa.Integer(), nullable=True),
    sa.Column('body_html', sa.String(length=300), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('flags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['submissions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('flags_user_idx', 'user_id'),
    sa.Index('flags_post_idx', 'post_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('follows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['target_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.UniqueConstraint('user_id', 'target_id'),
    sa.Index('follows_target_id_idx', 'target_id'),
    sa.Index('follows_user_id_idx', 'user_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=8), nullable=True),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('ips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('addr', sa.String(length=64), nullable=True),
    sa.Column('reason', sa.String(length=256), nullable=True, server_default=''),
    sa.Column('banned_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['banned_by'], ['users.id'], ),
    sa.UniqueConstraint('addr'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('mods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.Column('accepted', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('invite_rescinded', sa.Boolean(), nullable=True, server_default='false'),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.UniqueConstraint('user_id', 'board_id'),
    sa.Index('mods_board_id_idx', 'board_id'),
    sa.Index('mods_invite_rescinded_idx', 'invite_rescinded'),
    sa.Index('mods_user_id_idx', 'user_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=False, server_default='false'),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('notifications_read_idx', 'read'),
    sa.Index('notifications_comment_id_idx', 'comment_id'),
    sa.Index('notifications_user_id_idx', 'user_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('postrels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['submissions.id'], ),
    sa.UniqueConstraint('post_id', 'board_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True, server_default='0'),
    sa.ForeignKeyConstraint(['post_id'], ['submissions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('reports_post_id_idx', 'post_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('rule_body', sa.String(length=256), nullable=True),
    sa.Column('rule_html', sa.String(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.Column('edited_utc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('submissions_aux',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('body', sa.String(length=10000), nullable=True),
    sa.Column('body_html', sa.String(length=20000), nullable=True),
    sa.Column('embed_url', sa.String(length=256), nullable=True),
    sa.Column('ban_reason', sa.String(length=128), nullable=True),
    sa.Column('key_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['submissions.id'], ),
    sa.Index('submissions_aux_id_idx', 'id'),
    sa.Index('submissions_aux_title_idx', 'title'),
    sa.PrimaryKeyConstraint('key_id')
    )

    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.UniqueConstraint('user_id', 'board_id'),
    sa.Index('subscriptions_is_active_idx', 'is_active'),
    sa.Index('subscriptions_user_id_idx', 'user_id'),
    sa.Index('subscriptions_board_id_idx', 'board_id'),
    sa.PrimaryKeyConstraint('id')
    )



    op.create_table('useragents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kwd', sa.String(length=128), nullable=True),
    sa.Column('banned_by', sa.Integer(), nullable=True),
    sa.Column('reason', sa.String(length=256), nullable=True),
    sa.Column('mock', sa.String(length=256), nullable=True, server_default=''),
    sa.Column('status_code', sa.Integer(), nullable=True, server_default='418'),
    sa.ForeignKeyConstraint(['banned_by'], ['users.id'], ),
    sa.UniqueConstraint('kwd'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('userblocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['target_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('userblocks_target_id_idx', 'target_id'),
    sa.Index('userblocks_user_id_idx', 'user_id'),
    sa.Index('userblocks_both_idx', 'user_id', 'target_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('userflags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('resolved', sa.Boolean(), nullable=True, server_default='false'),
    sa.ForeignKeyConstraint(['target_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('vote_type', sa.Integer(), nullable=True, server_default='0'),
    sa.ForeignKeyConstraint(['submission_id'], ['submissions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('votes_user_id_idx', 'user_id'),
    sa.Index('votes_submission_id_idx', 'submission_id'),
    sa.Index('votes_vote_type_idx', 'vote_type'),
    sa.PrimaryKeyConstraint('id')
    )
    # endregion

    # region Functions
    op.execute("CREATE FUNCTION public.age(public.comments) RETURNS integer \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST( EXTRACT( EPOCH FROM CURRENT_TIMESTAMP) AS int) - $1.created_utc \
                        $_$;")

    op.execute("CREATE FUNCTION public.age(public.submissions) RETURNS integer \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST( EXTRACT( EPOCH FROM CURRENT_TIMESTAMP) AS int) - $1.created_utc \
                        $_$;")

    op.execute("CREATE FUNCTION public.age(public.users) RETURNS integer \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST( EXTRACT( EPOCH FROM CURRENT_TIMESTAMP) AS int) - $1.created_utc \
                    $_$;")

    op.execute("CREATE FUNCTION public.board_id(public.comments) RETURNS integer \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT submissions.board_id \
                        FROM submissions \
                        WHERE submissions.id=$1.parent_submission \
                        $_$;")

    op.execute("CREATE FUNCTION public.board_id(public.reports) RETURNS integer \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT submissions.board_id \
                        FROM submissions \
                        WHERE submissions.id=$1.post_id \
                        $_$;")

    op.execute("CREATE FUNCTION public.comment_count(public.submissions) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COUNT(*) \
                        FROM comments \
                        WHERE is_banned=false \
                            AND is_deleted=false \
                            AND parent_submission = $1.id \
                        $_$;")

    op.execute("CREATE FUNCTION public.comment_energy(public.users) RETURNS numeric \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COALESCE( \
                        ( \
                            SELECT SUM(comments.score) \
                            FROM comments \
                            WHERE comments.author_id=$1.id \
                            AND comments.is_banned=false \
                            ), \
                            0 \
                        ) \
                        $_$;")

    op.execute("CREATE FUNCTION public.created_utc(public.notifications) RETURNS integer \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT created_utc FROM comments \
                        WHERE comments.id=$1.comment_id \
                        $_$;")

    op.execute("CREATE FUNCTION public.downs(public.comments) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT ( \
                        ( \
                          SELECT count(*) \
                          FROM ( \
                            SELECT * FROM commentvotes \
                            WHERE comment_id=$1.id \
                            AND vote_type=-1 \
                          ) as v1 \
                          LEFT JOIN users \
                            ON users.id=v1.user_id \
                          WHERE users.is_banned=0 \
                        )-( \
                          SELECT count(distinct v1.id) \
                          FROM ( \
                            SELECT * FROM commentvotes \
                            WHERE comment_id=$1.id \
                            AND vote_type=-1 \
                          ) as v1 \
                          LEFT JOIN (SELECT * FROM users) as u1 \
                            ON u1.id=v1.user_id \
                          LEFT JOIN (SELECT * FROM alts) as a1 \
                            ON a1.user1=v1.user_id \
                          LEFT JOIN (SELECT * FROM alts) as a2 \
                            ON a2.user2=v1.user_id \
                          LEFT JOIN ( \
                              SELECT * FROM commentvotes \
                              WHERE comment_id=$1.id \
                              AND vote_type=-1 \
                          ) as v2 \
                            ON (v2.user_id=a1.user2 OR v2.user_id=a2.user1) \
                          LEFT JOIN (SELECT * FROM users) as u2 \
                            ON u2.id=v2.user_id \
                          WHERE u1.is_banned=0 \
                          AND u2.is_banned=0 \
                          AND v1.id is not null \
                          AND v2.id is not null \
                        )) \
                        $_$;")

    op.execute("CREATE FUNCTION public.downs(public.submissions) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT ( \
                        ( \
                          SELECT count(*) \
                          FROM ( \
                            SELECT * FROM votes \
                            WHERE submission_id=$1.id \
                            AND vote_type=-1 \
                          ) as v1 \
                          LEFT JOIN users \
                            on users.id=v1.user_id \
                          WHERE users.is_banned=0 \
                        )-( \
                          SELECT count(distinct v1.id) \
                          FROM ( \
                            SELECT * FROM votes \
                            WHERE submission_id=$1.id \
                            AND vote_type=-1 \
                          ) as v1 \
                          LEFT JOIN (SELECT * FROM users) as u1 \
                            on u1.id=v1.user_id \
                          LEFT JOIN (SELECT * FROM alts) as a1 \
                            on a1.user1=v1.user_id \
                          LEFT JOIN (SELECT * FROM alts) as a2 \
                            on a2.user2=v1.user_id \
                          LEFT JOIN ( \
                              SELECT * FROM votes \
                              WHERE submission_id=$1.id \
                              AND vote_type=-1 \
                          ) as v2 \
                            on (v2.user_id=a1.user2 or v2.user_id=a2.user1) \
                          LEFT JOIN (SELECT * FROM users) as u2 \
                            on u2.id=v2.user_id \
                          WHERE u1.is_banned=0 \
                          AND u2.is_banned=0 \
                          AND v1.id is not null \
                          AND v2.id is not null \
                        )) \
                        $_$;")

    op.execute("CREATE FUNCTION public.energy(public.users) RETURNS numeric \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COALESCE( \
                        ( \
                            SELECT SUM(submissions.score) \
                            FROM submissions \
                            WHERE submissions.author_id=$1.id \
                                AND submissions.is_banned=false \
                        ), \
                        0 \
                        ) \
                    $_$;")

    op.execute("CREATE FUNCTION public.flag_count(public.comments) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COUNT(*) \
                        FROM commentflags \
                        JOIN users ON commentflags.user_id=users.id \
                        WHERE comment_id=$1.id \
                        AND users.is_banned=0 \
                        $_$;")

    op.execute("CREATE FUNCTION public.flag_count(public.submissions) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COUNT(*) \
                        FROM flags \
                        JOIN users ON flags.user_id=users.id \
                        WHERE post_id=$1.id \
                        AND users.is_banned=0 \
                        $_$;")

    op.execute("CREATE FUNCTION public.follower_count(public.users) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT count(*) \
                        FROM follows \
                        LEFT JOIN users \
                        ON follows.target_id=users.id \
                        WHERE follows.target_id=$1.id \
                        AND users.is_banned=0 \
                        $_$;")

    op.execute("CREATE FUNCTION public.is_banned(public.notifications) RETURNS boolean \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT is_banned FROM comments \
                        WHERE comments.id=$1.comment_id \
                        $_$;")

    op.execute("CREATE FUNCTION public.is_deleted(public.notifications) RETURNS boolean \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT is_deleted FROM comments \
                        WHERE comments.id=$1.comment_id \
                        $_$;")

    op.execute("CREATE FUNCTION public.is_public(public.comments) RETURNS boolean \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT submissions.is_public \
                        FROM submissions \
                        WHERE submissions.id=$1.parent_submission \
                        $_$;")

    op.execute("CREATE FUNCTION public.is_public(public.submissions) RETURNS boolean \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT \
                            case \
                                when $1.post_public=true \
                                    then true \
                                when (select (is_private) \
                                    from boards \
                                    where id=$1.board_id \
                                    )=true \
                                    then false \
                                else \
                                    true \
                            end \
                      $_$;")

    op.execute("CREATE FUNCTION public.mod_count(public.users) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$select count(*) from mods where accepted=true and invite_rescinded=false and user_id=$1.id;$_$;")

    op.execute("CREATE FUNCTION public.rank_activity(public.submissions) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST($1.comment_count AS float)/((CAST(($1.age+5000) AS FLOAT)/100.0)^(1.3)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_best(public.submissions) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT 10000000.0*CAST(($1.ups - $1.downs) AS float)/((CAST(($1.age+5000) AS FLOAT)*cast((select boards.subscriber_count from boards where boards.id=$1.board_id)+3000 as float)/100.0)^(1.3)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_fiery(public.comments) RETURNS double precision \
                LANGUAGE sql IMMUTABLE STRICT \
                AS $_$ \
                    SELECT SQRT(CAST(($1.ups * $1.downs) AS float))/((CAST(($1.age+100000) AS FLOAT)/6.0)^(1.3)) \
                $_$;")

    op.execute("CREATE FUNCTION public.rank_fiery(public.submissions) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT SQRT(CAST(($1.ups * $1.downs) AS float))/((CAST(($1.age+5000) AS FLOAT)/100.0)^(1.3)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_hot(public.comments) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST(($1.ups - $1.downs) AS float)/((CAST(($1.age+100000) AS FLOAT)/6.0)^(1.3)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_hot(public.submissions) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST(($1.ups - $1.downs) AS float)/((CAST(($1.age+5000) AS FLOAT)/100.0)^(1.3)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.recent_subscriptions(public.boards) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        select count(*) \
                        from subscriptions \
                        left join users \
                        on subscriptions.user_id=users.id \
                        where subscriptions.board_id=$1.id \
                        and subscriptions.is_active=true \
                        and subscriptions.created_utc > CAST( EXTRACT( EPOCH FROM CURRENT_TIMESTAMP) AS int) - 60*60*24 \
                        and users.is_banned=0 \
                    $_$;")

    op.execute("CREATE FUNCTION public.referral_count(public.users) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COUNT(*) \
                        FROM USERS \
                        WHERE users.is_banned=0 \
                        AND users.referred_by=$1.id \
                    $_$;")

    op.execute("CREATE FUNCTION public.report_count(public.submissions) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COUNT(*) \
                        FROM reports \
                        JOIN users ON reports.user_id=users.id \
                        WHERE post_id=$1.id \
                        AND users.is_banned=0 \
                        and reports.created_utc >= $1.edited_utc \
                    $_$;")

    op.execute("CREATE FUNCTION public.score(public.comments) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT ($1.ups - $1.downs) \
                    $_$;")

    op.execute("CREATE FUNCTION public.score(public.submissions) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT ($1.ups - $1.downs) \
                    $_$;")

    op.execute("CREATE FUNCTION public.similar_count(public.comments) RETURNS bigint \
                    LANGUAGE sql \
                    AS $_$ select count(*) from comments where author_id=$1.id and similarity(comments.body, $1.body) > 0.5 $_$;")

    op.execute("CREATE FUNCTION public.splash(text) RETURNS SETOF public.images \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT * \
                        FROM images \
                        WHERE state=$1 \
                        ORDER BY random() \
                        LIMIT 1 \
                    $_$;")

    op.execute("CREATE FUNCTION public.subscriber_count(public.boards) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        select \
                            case \
                            when $1.is_private=false \
                            then \
                                 (select count(*) \
                                 from subscriptions \
                                 left join users \
                                 on subscriptions.user_id=users.id \
                                 where subscriptions.board_id=$1.id \
                                 and users.is_banned=0) \
                            when $1.is_private=true \
                            then \
                                 (select count(*) \
                                 from subscriptions \
                                 left join users \
                                    on subscriptions.user_id=users.id \
                                 left join ( \
                                    select * from contributors \
                                    where contributors.board_id=$1.id \
                                 )as contribs \
                                    on contribs.user_id=users.id \
                                 where subscriptions.board_id=$1.id \
                                 and users.is_banned=0 \
                                 and contribs.user_id is not null) \
                            end \
                    $_$;")

    op.execute("CREATE FUNCTION public.trending_rank(public.boards) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        select \
                            case \
                                when $1.subscriber_count<10 then 0 \
                                when $1.subscriber_count>=9 then cast($1.recent_subscriptions as float) / log(cast($1.subscriber_count as float)) \
                            end \
                    $_$;")

    op.execute("CREATE FUNCTION public.ups(public.comments) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        select ( \
                        ( \
                          SELECT count(*) \
                          from ( \
                            select * from commentvotes \
                            where comment_id=$1.id \
                            and vote_type=1 \
                          ) as v1 \
                          left join users \
                            on users.id=v1.user_id \
                          where users.is_banned=0 \
                        )-( \
                          SELECT count(distinct v1.id) \
                          from ( \
                            select * from commentvotes \
                            where comment_id=$1.id \
                            and vote_type=1 \
                          ) as v1 \
                          left join (select * from users) as u1 \
                            on u1.id=v1.user_id \
                          left join (select * from alts) as a1 \
                            on a1.user1=v1.user_id \
                          left join (select * from alts) as a2 \
                            on a2.user2=v1.user_id \
                          left join ( \
                              select * from commentvotes \
                              where comment_id=$1.id \
                              and vote_type=1 \
                          ) as v2 \
                            on (v2.user_id=a1.user2 or v2.user_id=a2.user1) \
                          left join (select * from users) as u2 \
                            on u2.id=v2.user_id \
                          where u1.is_banned=0 \
                          and u2.is_banned=0 \
                          and v1.id is not null \
                          and v2.id is not null \
                        )) \
                      $_$;")

    op.execute("CREATE FUNCTION public.ups(public.submissions) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        select ( \
                        ( \
                          SELECT count(*) \
                          from ( \
                            select * from votes \
                            where submission_id=$1.id \
                            and vote_type=1 \
                          ) as v1 \
                          left join users \
                            on users.id=v1.user_id \
                          where users.is_banned=0 \
                        )-( \
                          SELECT count(distinct v1.id) \
                          from ( \
                            select * from votes \
                            where submission_id=$1.id \
                            and vote_type=1 \
                          ) as v1 \
                          left join (select * from users) as u1 \
                            on u1.id=v1.user_id \
                          left join (select * from alts) as a1 \
                            on a1.user1=v1.user_id \
                          left join (select * from alts) as a2 \
                            on a2.user2=v1.user_id \
                          left join ( \
                              select * from votes \
                              where submission_id=$1.id \
                              and vote_type=1 \
                          ) as v2 \
                            on (v2.user_id=a1.user2 or v2.user_id=a2.user1) \
                          left join (select * from users) as u2 \
                            on u2.id=v2.user_id \
                          where u1.is_banned=0 \
                          and u2.is_banned=0 \
                          and v1.id is not null \
                          and v2.id is not null \
                        )) \
                      $_$;")
    # endregion

def downgrade():

    # Remove all functions
    op.execute("DO $$ DECLARE \
                    funcname VARCHAR; \
                BEGIN \
                    FOR funcname IN (SELECT ns.nspname || '.' || proname || '(' || oidvectortypes(proargtypes) || ');' \
                                        FROM pg_proc INNER JOIN pg_namespace ns ON (pg_proc.pronamespace = ns.oid) \
                                        WHERE ns.nspname = 'public'  order by proname) \
                LOOP \
                    EXECUTE 'DROP FUNCTION IF EXISTS ' || funcname; \
                END LOOP; \
                END $$;")

    # remove all tables
    op.drop_table('notifications')
    op.drop_table('commentvotes')
    op.drop_table('comments_aux')
    op.drop_table('commentflags')
    op.drop_table('votes')
    op.drop_table('submissions_aux')
    op.drop_table('reports')
    op.drop_table('postrels')
    op.drop_table('flags')
    op.drop_table('subscriptions')
    op.drop_table('rules')
    op.drop_table('mods')
    op.drop_table('contributors')
    op.drop_table('bans')
    op.drop_table('userblocks')
    op.drop_table('useragents')
    op.drop_table('userflags')
    op.drop_table('ips')
    op.drop_table('follows')
    op.drop_table('badges')
    op.drop_table('alts')
    op.drop_table('images')
    op.drop_table('badwords')
    op.drop_table('badge_defs')
    op.drop_table('dms')
    op.drop_table('badpics')
    op.drop_table('comments')
    op.drop_table('submissions')
    op.drop_table('domains')
    op.drop_table('boards')
    op.drop_table('users')
    op.drop_table('titles')
