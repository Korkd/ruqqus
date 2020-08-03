"""base revision

Revision ID: 01bcc5ec8808
Revises: 
Create Date: 2020-07-12 20:14:57.019779

"""
from alembic import op
from alembic import context
import sqlalchemy as sa
from psycopg2 import InternalError
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '01bcc5ec8808'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    schema_downgrade()


def schema_upgrades():
    op.execute("SET statement_timeout = 0;")
    op.execute("SET lock_timeout = 0;")
    op.execute("SET idle_in_transaction_session_timeout = 0;")
    op.execute("SET client_encoding = 'UTF8';")
    op.execute("SET standard_conforming_strings = on;")
    op.execute("SET check_function_bodies = false;")
    op.execute("SET xmloption = content;")
    op.execute("SET client_min_messages = warning;")
    op.execute("SET row_security = off;")

    op.execute("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;")
    op.execute("COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';")

    op.execute("CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;")
    op.execute("COMMENT ON EXTENSION pg_stat_statements IS 'track execution statistics of all SQL statements executed';")

    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;")
    op.execute("COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';")

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
    sa.Column('background_color_1', sa.String(length=8), nullable=True, server_default=text('NULL::character varying')),
    sa.Column('background_color_2', sa.String(length=8), nullable=True,server_default=text('NULL::character varying')),
    sa.Column('gradient_angle', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('box_shadow_color', sa.String(length=32), nullable=True),
    sa.Column('text_shadow_color', sa.String(length=32), nullable=True),
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
    sa.Column('bio', sa.String(length=300), nullable=True, server_default=''),
    sa.Column('bio_html', sa.String(length=1000), nullable=True),
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
    sa.Column('patreon_id', sa.String(length=64), nullable=True, server_default=text('NULL::bpchar')),
    sa.Column('patreon_access_token', sa.String(length=128), nullable=True),
    sa.Column('patreon_refresh_token', sa.String(length=128), nullable=True),
    sa.Column('patreon_pledge_cents', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('patreon_name', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['referred_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['title_id'], ['titles.id'], ),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('reddit_username'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('patreon_id'),
    sa.Index('users_is_deleted_idx', 'is_deleted'),
    sa.Index('users_created_utc_idx', 'created_utc'),
    sa.Index('users_title_id_idx', 'title_id'),
    sa.Index('users_is_banned_idx', 'is_banned'),
    sa.Index('users_is_private_idx', 'is_private'),
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
    sa.Index('badge_defs_qualification_expr_idx', 'qualification_expr'),
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
    sa.Index('badges_user_id_idx', 'user_id'),
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
    sa.Column('stored_subscriber_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.UniqueConstraint('name'),
    sa.Index('boards_stored_subscriber_count_idx', 'stored_subscriber_count', postgresql_ops={'stored_subscriber_count': 'DESC'}),
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
    sa.Index('ban_board_id_idx', 'board_id'),
    sa.Index('ban_user_id_idx', 'user_id'),
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
    sa.Column('is_offensive', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('is_pinned', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('is_nsfl', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('repost_id', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('score_best', sa.Float(), nullable=True, server_default=text('0')),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['domain_ref'], ['domains.id'], ),
    sa.ForeignKeyConstraint(['original_board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['mod_approved'], ['users.id'], ),
    sa.Index('submissions_domain_ref_idx', 'domain_ref'),
    sa.Index('submissions_over_18_idx', 'over_18'),
    sa.Index('submissions_author_id_idx', 'author_id'),
    sa.Index('submissions_is_offensive_idx', 'is_offensive'),
    sa.Index('submissions_is_pinned_idx', 'is_pinned'),
    sa.Index('submissions_board_id_idx', 'board_id'),
    sa.Index('submissions_stickied_idx', 'stickied'),
    sa.Index('submissions_created_utc_sort_idx', 'created_utc', postgresql_ops={'created_utc': 'DESC'}),
    sa.Index('submissions_binary_group_idx', 'is_banned', 'is_deleted', 'over_18'),
    sa.Index('submissions_board_sort_disputed_idx', 'score_disputed', 'board_id', postgresql_ops={'score_disputed': 'DESC'}),
    sa.Index('submissions_board_sort_hot_idx', 'score_hot', 'board_id', postgresql_ops={'score_hot': 'DESC'}),
    sa.Index('submissions_board_sort_activity_idx', 'score_activity', 'board_id', postgresql_ops={'score_activity': 'DESC'}),
    sa.Index('submissions_board_sort_top_idx', 'score_top', 'board_id', postgresql_ops={'score_top': 'DESC'}),
    sa.Index('submissions_board_sort_best_idx', 'score_best', 'board_id', postgresql_ops={'score_best': 'DESC'}),
    sa.Index('submissions_shown_sort_disputed_idx', 'is_banned', 'is_deleted', 'score_disputed', 'over_18', postgresql_ops={'score_disputed': 'DESC'}),
    sa.Index('submissions_shown_sort_hot_idx', 'is_banned', 'is_deleted', 'score_hot', 'over_18', postgresql_ops={'score_hot': 'DESC'}),
    sa.Index('submissions_shown_sort_new_idx', 'is_banned', 'is_deleted', 'created_utc', 'over_18', postgresql_ops={'created_utc': 'DESC'}),
    sa.Index('submissions_trending_all_idx', 'is_banned', 'is_deleted', 'stickied', 'post_public', 'score_hot', postgresql_ops={'score_hot': 'DESC'}),
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
    sa.Column('original_board_id', sa.Integer(), nullable=True),
    #sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    #sa.ForeignKeyConstraint(['parent_comment_id'], ['comments.id'], ),
    #sa.ForeignKeyConstraint(['parent_submission'], ['submissions.id'], ),
    #sa.ForeignKeyConstraint(['original_board_id'], ['boards.id']),
    sa.Index('comments_parent_comment_id_idx', 'parent_comment_id'),
    sa.Index('comments_parent_submission_idx', 'parent_submission'),
    sa.Index('comments_author_id_idx', 'author_id'),
    sa.Index('comments_original_board_id_idx', 'original_board_id'),
    sa.Index('comments_loader_idx', 'parent_submission', 'level', 'score_hot', postgresql_ops={'score_hot': 'DESC'}, postgresql_where=text('level <= 8')),
    sa.Index('comments_score_disputed_idx', 'score_disputed', postgresql_ops={'score_disputed': 'DESC'}),
    sa.Index('comments_score_hot_idx', 'score_hot', postgresql_ops={'score_hot': 'DESC'}),
    sa.Index('comments_score_top_idx', 'score_top', postgresql_ops={'score_top': 'DESC'}),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('commentflags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.Index('commentflags_user_id_idx', 'user_id'),
    sa.Index('commentflags_comment_id_idx', 'comment_id'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('comments_aux',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=10000), nullable=True),
    sa.Column('body_html', sa.String(length=20000), nullable=True),
    sa.Column('ban_reason', sa.String(length=128), nullable=True),
    sa.Column('key_id', sa.Integer(), nullable=False),
    #sa.ForeignKeyConstraint(['id'], ['comments.id'], ),
    sa.Index('commentsaux_id_idx', 'id'),
    sa.PrimaryKeyConstraint('key_id')
    )

    op.create_table('commentvotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('vote_type', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    #sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    #sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.UniqueConstraint('user_id', 'comment_id'),
    sa.Index('commentvotes_comment_id_idx', 'comment_id'),
    sa.Index('commentvotes_vote_type_idx', 'vote_type'),
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
    sa.Index('contributors_is_active_idx', 'is_active'),
    sa.Index('contributors_board_id_idx', 'board_id'),
    sa.Index('contributors_user_id_idx', 'user_id'),
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
    sa.Index('flags_user_id_idx', 'user_id'),
    sa.Index('flags_post_id_idx', 'post_id'),
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

    op.create_table('boardblocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('created_utc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
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
    sa.Index('submissionsaux_id_idx', 'id'),
    sa.Index('submissionsaux_title_idx', 'title'),
    sa.Index('submissionsaux_url_idx', 'url'),
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
    #sa.ForeignKeyConstraint(['submission_id'], ['submissions.id'], ),
    #sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.UniqueConstraint('user_id', 'submission_id'),
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

    op.execute("CREATE FUNCTION public.comment_energy(public.users) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COALESCE( \
                        ( \
                            SELECT SUM(comments.score_top) \
                            FROM comments \
                            WHERE comments.author_id=$1.id \
                            AND comments.is_banned=false \
                            and comments.parent_submission is not null \
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

    op.execute("CREATE FUNCTION public.energy(public.users) RETURNS bigint \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT COALESCE( \
                        ( \
                            SELECT SUM(submissions.score_top) \
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
                        SELECT CAST($1.comment_count AS float)/((CAST(($1.age+5000) AS FLOAT)/100.0)^(1.6)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_best(public.submissions) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT 10000000.0*CAST(($1.ups - $1.downs) AS float)/((CAST(($1.age+5000) AS FLOAT)*cast((select boards.subscriber_count from boards where boards.id=$1.board_id)+3000 as float)/100.0)^(1.6)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_fiery(public.comments) RETURNS double precision \
                LANGUAGE sql IMMUTABLE STRICT \
                AS $_$ \
                    SELECT SQRT(CAST(($1.ups * $1.downs) AS float))/((CAST(($1.age+100000) AS FLOAT)/6.0)^(1.6)) \
                $_$;")

    op.execute("CREATE FUNCTION public.rank_fiery(public.submissions) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT SQRT(CAST(($1.ups * $1.downs) AS float))/((CAST(($1.age+5000) AS FLOAT)/100.0)^(1.6)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_hot(public.comments) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST(($1.ups - $1.downs) AS float)/((CAST(($1.age+100000) AS FLOAT)/6.0)^(1.6)) \
                    $_$;")

    op.execute("CREATE FUNCTION public.rank_hot(public.submissions) RETURNS double precision \
                    LANGUAGE sql IMMUTABLE STRICT \
                    AS $_$ \
                        SELECT CAST(($1.ups - $1.downs) AS float)/((CAST(($1.age+5000) AS FLOAT)/100.0)^(1.6)) \
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


def schema_downgrade():

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


def data_upgrades():
    users = sa.table('users',
                     sa.column('id', sa.Integer()),
                     sa.column('username', sa.String(length=255)),
                     sa.column('email', sa.String(length=255)),
                     sa.column('passhash', sa.String(length=255)),
                     sa.column('created_utc', sa.Integer()),
                     sa.column('admin_level', sa.Integer()),
                     sa.column('creation_ip', sa.String(length=255)),
                     sa.column('login_nonce', sa.Integer()),
                     sa.column('tos_agreed_utc', sa.Integer())
                     )

    op.execute(users.insert().values(
        username='ruqqie',
        email='ruqqie@ruqqus.com',
        passhash='pbkdf2:sha512:150000$vmPzuBFj$24cde8a6305b7c528b0428b1e87f256c65741bb035b4356549c13e745cc0581701431d5a2297d98501fcf20367791b4334dcd19cf063a6e60195abe8214f91e8',
        admin_level='100',
        created_utc='1592672337',
        creation_ip='127.0.0.1',
        tos_agreed_utc='1592672337',
        login_nonce='1'
    ))

    boards = sa.table('boards',
                      sa.column('id', sa.Integer()),
                      sa.column('name', sa.String(length=64)),
                      sa.column('is_banned', sa.Boolean()),
                      sa.column('created_utc', sa.Integer()),
                      sa.column('creator_id', sa.Integer()),
                      sa.column('color', sa.String(length=8))
                      )

    op.execute(boards.insert().values(
        name='general',
        is_banned=False,
        created_utc='1594709265',
        creator_id='1',
        color='805ad5'
    ))

    badge_defs = sa.table('badge_defs',
                          sa.column('id', sa.Integer()),
                          sa.column('name', sa.String(length=64)),
                          sa.column('description', sa.String(length=256)),
                          sa.column('icon', sa.String(length=64)),
                          sa.column('kind', sa.Integer()),
                          sa.column('rank', sa.Integer()),
                          sa.Column('qualification_expr', sa.String(length=128))
                          )

    op.execute(
        badge_defs.insert().values(id='1', name='Alpha User', description='Joined Ruqqus during open alpha',
                                   icon='alpha.png', kind='4', rank='4'))
    op.execute(
        badge_defs.insert().values(id='2', name='Verified Email', description='Verified Email', icon='mail.png',
                                   kind='1', rank='1', qualification_expr='v.is_activated'))
    op.execute(
        badge_defs.insert().values(id='3', name='Code Contributor', description='Contributed to Ruqqus source code',
                                   icon='git.png', kind='3', rank='3'))
    op.execute(
        badge_defs.insert().values(id='4', name='White Hat', description='Responsibly reported a security issue',
                                   icon='whitehat.png', kind='3', rank='3'))
    op.execute(
        badge_defs.insert().values(id='6', name='Beta User', description='Joined Ruqqus during open beta', icon='beta.png',
                                   kind='4', rank='3'))
    op.execute(
        badge_defs.insert().values(id='7', name='Sitebreaker', description='Inadvertantly broke Ruqqus',
                                   icon='sitebreaker.png', kind='3', rank='2'))
    op.execute(
        badge_defs.insert().values(id='8', name='Unsilenced', description='Ruqqus rejected a foreign order to take down this user\'s content.',
                                   icon='unsilenced.png', kind='3', rank='4'))
    op.execute(
        badge_defs.insert().values(id='9', name='Unknown', description='Ruqqus rejected a foreign order to turn over this user\'s information',
                                   icon='unknowable.png', kind='3', rank='4'))
    op.execute(
        badge_defs.insert().values(id='10', name='Recruiter', description='Recruited 1 friend to join Ruqqus',
                                   icon='recruit-1.png', kind='1', rank='1',
                                   qualification_expr='v.referral_count>=1 and v.referral_count<9'))
    op.execute(
        badge_defs.insert().values(id='11', name='Recruiter', description='Recruited 10 friend to join Ruqqus',
                                   icon='recruit-10.png', kind='1', rank='2',
                                   qualification_expr='v.referral_count>=10 and v.referral_count<99'))
    op.execute(
        badge_defs.insert().values(id='12', name='Recruiter', description='Recruited 100 friend to join Ruqqus',
                                   icon='recruit-100.png', kind='1', rank='3',
                                   qualification_expr='v.referral_count>=100'))
    op.execute(
        badge_defs.insert().values(id='13', name='New User', description='Been on Ruqqus for less than 30 days',
                                   icon='baby.png', kind='1', rank='1',
                                   qualification_expr='v.age < 2592000'))
    op.execute(
        badge_defs.insert().values(id='14', name='Charter Supporter', description='Financially supported Ruqqus during start-up',
                                   icon='charter.png', kind='4', rank='4'))
    op.execute(
        badge_defs.insert().values(id='15', name='Idea Maker',
                                   description='Had a good idea for Ruqqus which was implemented by the developers',
                                   icon='idea.png', kind='3', rank='2'))
    op.execute(
        badge_defs.insert().values(id='16', name='Game Night Participant',
                                   description='Participated in a Ruqqus community gaming event',
                                   icon='game-participant.png', kind='3', rank='2'))
    op.execute(
        badge_defs.insert().values(id='17', name='Game Night Finalist',
                                   description='Had a top finish in a Ruqqus community gaming event',
                                   icon='game-highfinish.png', kind='3', rank='3'))
    op.execute(
        badge_defs.insert().values(id='18', name='Artisan', description='Contributed to Ruqqus artwork or text',
                                   icon='art.png', kind='3', rank='3'))
    op.execute(
        badge_defs.insert().values(id='19', name='Fire Extinguisher',
                                   description='Awarded to @mutageno and @AmoralAtBest for contributing highly advanced technical experience and wisdom during scale-up operations resulting from the flood of new users.',
                                   icon='fire.png', kind='5', rank='5'))
    op.execute(
        badge_defs.insert().values(id='20', name='Dumpster Arsonist',
                                   description='Awarded to 8535 tenacious users who managed to sign up for Ruqqus while the servers were getting crushed',
                                   icon='dumpsterfire.png', kind='5', rank='6'))
    op.execute(
        badge_defs.insert().values(id='21', name='Bronze Patron', description='Contributes at least $1/month',
                                   icon='patreon-1.png', kind='2', rank='1',
                                   qualification_expr='v.patreon_pledge_cents>=100 and v.patreon_pledge_cents<500'))
    op.execute(
        badge_defs.insert().values(id='22', name='Silver Patron', description='Contributes at least $5/month',
                                   icon='patreon-2.png', kind='2', rank='2',
                                   qualification_expr='v.patreon_pledge_cents>=500 and v.patreon_pledge_cents<2000'))
    op.execute(
        badge_defs.insert().values(id='23', name='Gold Patron', description='Contributes at least $20/month',
                                   icon='patreon-3.png', kind='2', rank='3',
                                   qualification_expr='v.patreon_pledge_cents>=2000 and v.patreon_pledge_cents<5000'))
    op.execute(
        badge_defs.insert().values(id='24', name='Diamond Patron', description='Contributes at least $50/month',
                                   icon='patreon-4.png', kind='2', rank='4',
                                   qualification_expr='v.patreon_pledge_cents>=5000'))

    op.execute('SELECT pg_catalog.setval(\'badge_defs_id_seq\', 24, true);')

    titles = sa.table('titles',
                      sa.column('id', sa.Integer()),
                      sa.column('is_before', sa.Boolean()),
                      sa.column('text', sa.String(length=64)),
                      sa.column('qualification_expr', sa.String(length=256)),
                      sa.column('requirement_string', sa.String(length=512)),
                      sa.column('color', sa.String(length=6)),
                      sa.column('kind', sa.Integer()),
                      sa.column('background_color_1', sa.String(length=8)),
                      sa.column('background_color_2', sa.String(length=8)),
                      sa.column('gradient_angle', sa.Integer()),
                      sa.column('box_shadow_color', sa.String(length=32)),
                      sa.column('text_shadow_color', sa.String(length=32)),
                      )

    op.execute(
        titles.insert().values(id='1', is_before=False, text=', Novice Recruiter',
                               qualification_expr='v.referral_count>=1',
                               requirement_string='Refer 1 friend to join Ruqqus.', color='bb00bb'))
    op.execute(
        titles.insert().values(id='2', is_before=False, text=', Expert Recruiter',
                               qualification_expr='v.referral_count>=10',
                               requirement_string='Refer 10 friend to join Ruqqus.', color='bb00bb'))
    op.execute(
        titles.insert().values(id='3', is_before=False, text=', Master Recruiter',
                               qualification_expr='v.referral_count>=100',
                               requirement_string='Refer 100 friend to join Ruqqus.', color='bb00bb'))
    op.execute(
        titles.insert().values(id='4', is_before=False, text=', Breaker of Ruqqus',
                               qualification_expr='v.has_badge(7)',
                               requirement_string='Inadvertently break Ruqqus', color='dd5555', kind='3'))
    op.execute(
        titles.insert().values(id='5', is_before=False, text=' the Codesmith',
                               qualification_expr='v.has_badge(3)',
                               requirement_string='Make a contribution to the Ruqqus codebase', color='5555dd', kind='3'))
    op.execute(
        titles.insert().values(id='6', is_before=False, text=', Early Adopter',
                               qualification_expr='v.has_badge(6)',
                               requirement_string='Joined during open beta', color='aaaa22', kind='4'))
    op.execute(
        titles.insert().values(id='7', is_before=False, text=', Very Early Adopter',
                               qualification_expr='v.has_badge(1)',
                               requirement_string='Joined during open alpha', color='5555ff', kind='4'))
    op.execute(
        titles.insert().values(id='8', is_before=False, text=', the Invited',
                               qualification_expr='v.referred_by',
                               requirement_string='Joined Ruqqus from another user\'s referral', color='55aa55', kind='4'))
    op.execute(
        titles.insert().values(id='9', is_before=False, text=', Guildmaker',
                               qualification_expr='v.boards_created.first()',
                               requirement_string='Create your first Guild', color='aa8855'))
    op.execute(
        titles.insert().values(id='10', is_before=False, text=', Guildbuilder',
                               qualification_expr='v.boards_created.filter(Board.subscriber_count>=10).first()',
                               requirement_string='A Guild you created grows past 10 members.', color='aa8855'))
    op.execute(
        titles.insert().values(id='11', is_before=False, text=', Guildsmith',
                               qualification_expr='v.boards_created.filter(Board.subscriber_count>=100).first()',
                               requirement_string='A Guild you created grows past 100 members.', color='aa8855'))
    op.execute(
        titles.insert().values(id='12', is_before=False, text=', Guildmaster',
                               qualification_expr='v.boards_created.filter(Board.subscriber_count>=1000).first()',
                               requirement_string='A Guild you created grows past 1,000 members.', color='aa8855'))
    op.execute(
        titles.insert().values(id='13', is_before=False, text=', Arch Guildmaster',
                               qualification_expr='v.boards_created.filter(Board.subscriber_count>=10000).first()',
                               requirement_string='A Guild you created grows past 10,000 members.', color='aa8855'))
    op.execute(
        titles.insert().values(id='14', is_before=False, text=', Guildlord',
                               qualification_expr='v.boards_created.filter(Board.subscriber_count>=100000).first()',
                               requirement_string='A Guild you created grows past 100,000 members.', color='aa8855'))
    op.execute(
        titles.insert().values(id='15', is_before=False, text=', Ultimate Guildlord',
                               qualification_expr='v.boards_created.filter(Board.subscriber_count>=1000000).first()',
                               requirement_string='A Guild you created grows past 1,000,000 members.', color='aa8855'))
    op.execute(
        titles.insert().values(id='16', is_before=False, text=' the Spymaster',
                               qualification_expr='v.has_badge(4)',
                               requirement_string='Responsibly report a security issue to us', color='666666', kind='3'))
    op.execute(
        titles.insert().values(id='17', is_before=False, text=', the Unsilenced',
                               qualification_expr='v.has_badge(8)',
                               requirement_string='We rejected a foreign order to take down your content', color='666666', kind='3'))
    op.execute(
        titles.insert().values(id='18', is_before=False, text=', the Unknown',
                               qualification_expr='v.has_badge(9)',
                               requirement_string='We rejected a foreign order for your user information', color='666666', kind='3'))
    op.execute(
        titles.insert().values(id='19', is_before=False, text=', Bane of Tyrants',
                               qualification_expr='v.has_badge(8) and v.has_badge(9)',
                               requirement_string='We rejected foreign orders for your information and to take down your content.', color='666666', kind='3'))
    op.execute(
        titles.insert().values(id='20', is_before=False, text=' the Hot',
                               qualification_expr='v.submissions.filter(Submission.score>=100).first()',
                               requirement_string='Get at least 100 Reputation from a single post.', color='dd5555'))
    op.execute(
        titles.insert().values(id='21', is_before=False, text=' the Friendly',
                               qualification_expr='v.follower_count>=1',
                               requirement_string='Have at least 1 subscriber', color='5555dd'))
    op.execute(
        titles.insert().values(id='22', is_before=False, text=' the Likeable',
                               qualification_expr='v.follower_count>=10',
                               requirement_string='Have at least 10 subscriber', color='5555dd'))
    op.execute(
        titles.insert().values(id='23', is_before=False, text=' the Popular',
                               qualification_expr='v.follower_count>=100',
                               requirement_string='Have at least 100 subscriber', color='5555dd'))
    op.execute(
        titles.insert().values(id='24', is_before=False, text=' the Influential',
                               qualification_expr='v.follower_count>=1000',
                               requirement_string='Have at least 1000 subscriber', color='5555dd'))
    op.execute(
        titles.insert().values(id='25', is_before=False, text=', the Famous',
                               qualification_expr='v.follower_count>=10000',
                               requirement_string='Have at least 10000 subscriber', color='5555dd'))
    op.execute(
        titles.insert().values(id='26', is_before=False, text=' the Generous',
                               qualification_expr='v.has_badge(14)',
                               requirement_string='Financially supported Ruqqus during start-up', color='bb00bb', kind='4'))
    op.execute(
        titles.insert().values(id='27', is_before=False, text=', the Innovative',
                               qualification_expr='v.has_badge(15)',
                               requirement_string='Had a good idea for Ruqqus', color='603abb'))
    op.execute(
        titles.insert().values(id='28', is_before=False, text=' the Gamer',
                               qualification_expr='v.has_badge(16)',
                               requirement_string='Participate in Ruqqus gaming night', color='bb00bb'))
    op.execute(
        titles.insert().values(id='29', is_before=False, text=' [Level 1337]',
                               qualification_expr='v.has_badge(17)',
                               requirement_string='Earn a top finish in a Ruqqus gaming night', color='aaaa66'))
    op.execute(
        titles.insert().values(id='30', is_before=False, text=' the Artisan',
                               qualification_expr='v.has_badge(18)',
                               requirement_string='Made a contribution to Ruqqus text or art.', color='5555dd', kind='3'))
    op.execute(
        titles.insert().values(id='31', is_before=False, text=' the Dumpster Arsonist',
                               qualification_expr='v.has_badge(20)',
                               requirement_string='Joined Ruqqus despite the flood of users crashing the site', color='885588', kind='4'))
    op.execute(
        titles.insert().values(id='32', is_before=False, text=', Bronze Patron',
                               qualification_expr='v.patreon_pledge_cents>=100 and v.patreon_pledge_cents<500',
                               requirement_string='Contribute at least $1/month on Patreon', color='aa8855', kind='2'))
    op.execute(
        titles.insert().values(id='33', is_before=False, text='Silver Patron',
                               qualification_expr='v.patreon_pledge_cents>=500 and v.patreon_pledge_cents<2000',
                               requirement_string='Contribute at least $5/month on Patreon', color='30363c', kind='2',
                               background_color_1='899caa', background_color_2='c6d1dc', gradient_angle='4'))
    op.execute(
        titles.insert().values(id='34', is_before=False, text='Gold Patron',
                               qualification_expr='v.patreon_pledge_cents>=2000 and v.patreon_pledge_cents<5000',
                               requirement_string='Contribute at least $20/month on Patreon', color='502e0e', kind='2',
                               background_color_1='ce9632', background_color_2='f7ce68', gradient_angle='5',
                               box_shadow_color='216, 178, 84', text_shadow_color='240, 188, 120'))
    op.execute(
        titles.insert().values(id='35', is_before=False, text='Diamond Patron',
                               qualification_expr='v.patreon_pledge_cents>=5000',
                               requirement_string='Contribute at least $50/month on Patreon', color='2a4042', kind='2',
                               background_color_1='54c0c0', background_color_2='89e5ee', gradient_angle='10',
                               box_shadow_color='88, 195, 199', text_shadow_color='191, 220, 216'))

    op.execute('SELECT pg_catalog.setval(\'titles_id_seq\', 35, true);')
