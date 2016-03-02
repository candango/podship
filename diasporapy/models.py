#!/usr/bin/env python
#
# Copyright 2015-2016 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Date, Integer, Text, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index, DefaultClause
from sqlalchemy.dialects.postgres import TIMESTAMP

from firenado.util.sqlalchemy_util import Base


class AccountDeletionBase(Base):

    __tablename__ = 'account_deletions'

    id = Column('id', Integer(), primary_key=True)
    diaspora_handle = Column('diaspora_handle', String(255), nullable=False)
    person_id = Column('person_id', Integer(), nullable=True)
    completed_at = Column('completed_at', TIMESTAMP(), nullable=False)


class AspectMembershipBase(Base):

    __tablename__ = 'aspect_memberships'

    id = Column('id', Integer(), primary_key=True)
    aspect_id = Column('aspect_id', Integer(),
                       ForeignKey('aspects.id',
                                  name='fk_aspect_memberships_aspect_id',
                                  ondelete='CASCADE'),
                       nullable=False)
    contact_id = Column('contact_id', Integer(),
                        ForeignKey('contacts.id',
                                   name='fk_aspect_memberships_contact_id',
                                   ondelete='CASCADE'),
                        nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_aspect_memberships_aspect_id_contact_id',
      AspectMembershipBase.aspect_id, AspectMembershipBase.contact_id,
      unique=True, postgresql_using='btree')
Index('idx_aspect_memberships_aspect_id', AspectMembershipBase.aspect_id,
      postgresql_using='btree')
Index('idx_aspect_memberships_contact_id', AspectMembershipBase.contact_id,
      postgresql_using='btree')


class AspectVisibilityBase(Base):

    __tablename__ = 'aspect_visibilities'

    id = Column('id', Integer(), primary_key=True)
    shareable_id = Column('shareable_id', Integer(), nullable=False)
    aspect_id = Column('aspect_id', Integer(),
                       ForeignKey('aspects.id',
                                  name='fk_aspect_visibilities_aspect_id',
                                  ondelete='CASCADE'),
                       nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    shareable_type = Column('shareable_type', String(255),
                            DefaultClause('Post'), nullable=False)

Index('idx_aspect_visibilities_aspect_id', AspectVisibilityBase.aspect_id,
      postgresql_using='btree')
Index('idx_aspect_visibilities_shareable_id_shareable_type',
      AspectVisibilityBase.shareable_id, AspectVisibilityBase.shareable_type,
      postgresql_using='btree')
Index('idx_aspect_visibilities_shareable_id_shareable_type_aspect_id',
      AspectVisibilityBase.shareable_id, AspectVisibilityBase.shareable_type,
      AspectVisibilityBase.aspect_id, postgresql_using='btree')


class AspectBase(Base):

    __tablename__ = 'aspects'

    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(255), nullable=False)
    # TODO: Diaspora don't set this as FK. Why?
    user_id = Column('user_id', Integer(), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    contacts_visible = Column('contacts_visible', Boolean(),
                              DefaultClause('True'), nullable=False)
    order_id = Column('order_id', Integer(), nullable=True)
    chat_enabled = Column('chat_enabled', Boolean(),
                          DefaultClause('False'), nullable=True)

Index('idx_aspects_user_id', AspectBase.user_id, postgresql_using='btree')
Index('idx_aspects_user_id_contacts_visible', AspectBase.user_id,
      AspectBase.contacts_visible, postgresql_using='btree')


class BlockBase(Base):

    __tablename__ = 'blocks'

    id = Column('id', Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), nullable=True)
    person_id = Column('person_id', Integer(), nullable=True)


class ChatContactBase(Base):

    __tablename__ = 'chat_contacts'

    id = Column('id', Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), nullable=False)
    jid = Column('jid', String(255), nullable=False)
    name = Column('name', String(255), nullable=True)
    ask = Column('ask', String(128), nullable=True)
    subscription = Column('subscription', String(128), nullable=False)

Index('idx_chat_contacts_user_id_jid', ChatContactBase.user_id,
      ChatContactBase.jid, unique='true', postgresql_using='btree')


class ChatFragmentBase(Base):

    __tablename__ = 'chat_fragments'

    id = Column('id', Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), nullable=False)
    root = Column('root', String(256), nullable=False)
    namespace = Column('namespace', String(256), nullable=False)
    xml = Column('xml', Text(), nullable=False)

Index('idx_chat_fragments_user_id', ChatFragmentBase.user_id,
      unique=True, postgresql_using='btree')


class ChatOfflineMessageBase(Base):

    __tablename__ = 'chat_offline_messages'

    id = Column('id', Integer(), primary_key=True)
    cfrom = Column('from', String(255), nullable=False)
    to = Column('to', String(255), nullable=False)
    message = Column('message', Text(), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)


class CommentBase(Base):

    __tablename__ = 'comments'

    id = Column('id', Integer(), primary_key=True)
    text = Column('text', Text(), nullable=False)
    commentable_id = Column('commentable_id', Integer(), nullable=False)
    author_id = Column('author_id', Integer(),
                       ForeignKey('people.id', name='fk_comments_author_id',
                                  ondelete='CASCADE'),
                       nullable=False)
    guid = Column('guid', String(255), nullable=False)
    author_signature = Column('author_signature', Text(), nullable=True)
    parent_author_signature = Column('parent_author_signature', Text(),
                                     nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    likes_count = Column('likes_count', Integer(), DefaultClause('0'),
                         nullable=False)
    commentable_type = Column('commentable_type', String(60),
                              DefaultClause('Post'), nullable=False)

Index('idx_comments_guid', CommentBase.guid, unique=True,
      postgresql_using='btree')
Index('idx_comments_author_id', CommentBase.author_id,
      postgresql_using='btree')
Index('idx_comments_commentable_id_commentable_type',
      CommentBase.commentable_id, CommentBase.commentable_type,
      postgresql_using='btree')


class ContactBase(Base):

    __tablename__ = 'contacts'

    id = Column('id', Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), nullable=False)
    person_id = Column('person_id', Integer(),
                       ForeignKey('people.id', name='fk_contacts_person_id',
                                  ondelete='CASCADE'),
                       nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    sharing = Column('sharing', Boolean(),
                     DefaultClause('False'), nullable=False)
    receiving = Column('receiving', Boolean(),
                       DefaultClause('False'), nullable=False)

Index('idx_contacts_user_id_person_id', ContactBase.user_id,
      ContactBase.person_id, unique=True, postgresql_using='btree')
Index('idx_contacts_person_id', ContactBase.person_id,
      postgresql_using='btree')


class ConversationVisibilityBase(Base):

    __tablename__ = 'conversation_visibilities'

    id = Column('id', Integer(), primary_key=True)
    conversation_id = Column(
        'conversation_id', Integer(),
        ForeignKey('conversations.id',
                   name='fk_conversation_visibilities_conversation_id',
                   ondelete='CASCADE'),
        nullable=False)
    person_id = Column(
        'person_id', Integer(),
        ForeignKey('people.id',
                   name='fk_conversation_visibilities_person_id',
                   ondelete='CASCADE'),
        nullable=False)
    unread = Column('unread', Integer(), DefaultClause('0'), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_conversation_visibilities_conversation_id_person_id',
      ConversationVisibilityBase.conversation_id,
      ConversationVisibilityBase.person_id, unique=True,
      postgresql_using='btree')
Index('idx_conversation_visibilities_conversation_id',
      ConversationVisibilityBase.conversation_id, postgresql_using='btree')
Index('idx_conversation_visibilities_person_id',
      ConversationVisibilityBase.person_id, postgresql_using='btree')


class ConversationBase(Base):

    __tablename__ = 'conversations'

    id = Column('id', Integer(), primary_key=True)
    subject = Column('subject', String(255), nullable=True)
    guid = Column('guid', String(255), nullable=False)
    author_id = Column('author_id', Integer(),
                       ForeignKey('people.id',
                                  name='fk_conversations_author_id',
                                  ondelete='CASCADE'),
                       nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_conversations_author_id', ConversationBase.author_id,
      postgresql_using='btree')


class InvitationCodeBase(Base):

    __tablename__ = 'invitation_codes'

    id = Column('id', Integer(), primary_key=True)
    token = Column('token', String(255), nullable=True)
    user_id = Column('user_id', Integer(), nullable=True)
    count = Column('count', Integer(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)


class InvitationsBase(Base):

    __tablename__ = 'invitations'

    id = Column('id', Integer(), primary_key=True)
    message = Column('message', Text(), nullable=True)
    sender_id = Column('sender_id', Integer(),
                       ForeignKey('users.id',
                                  name='fk_invitations_sender_id',
                                  ondelete='CASCADE'),
                       nullable=True)
    recipient_id = Column('recipient_id', Integer(),
                          ForeignKey('users.id',
                                     name='fk_invitations_recipient_id',
                                     ondelete='CASCADE'),
                          nullable=True)
    aspect_id = Column('aspect_id', Integer(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    service = Column('service', String(255), nullable=True)
    identifier = Column('identifier', String(255), nullable=True)
    admin = Column('admin', Boolean(), DefaultClause('False'), nullable=True)
    language = Column('language', String(255), DefaultClause('en'),
                      nullable=True)

Index('idx_invitations_aspect_id', InvitationsBase.aspect_id,
      postgresql_using='btree')
Index('idx_invitations_recipient_id', InvitationsBase.recipient_id,
      postgresql_using='btree')
Index('idx_invitations_sender_id', InvitationsBase.sender_id,
      postgresql_using='btree')


class LikeBase(Base):

    __tablename__ = 'likes'

    id = Column('id', Integer(), primary_key=True)
    positive = Column('positive', Boolean(), DefaultClause('True'),
                      nullable=True)
    target_id = Column('target_id', Integer(), nullable=True)
    author_id = Column('author_id', Integer(),
                       ForeignKey('people.id',
                                  name='fk_likes_author_id',
                                  ondelete='CASCADE'),
                       nullable=True)
    guid = Column('guid', String(255), nullable=True)
    author_signature = Column('author_signature', Text(), nullable=True)
    parent_author_signature = Column('parent_author_signature', Text(),
                                     nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    target_type = Column('target_type', String(60), nullable=False)

Index('idx_likes_guid', LikeBase.guid, unique=True, postgresql_using='btree')
Index('idx_likes_target_id_author_id_target_type', LikeBase.target_id,
      LikeBase.author_id, LikeBase.target_type, unique=True,
      postgresql_using='btree')
Index('idx_likes_author_id', LikeBase.author_id, postgresql_using='btree')
Index('idx_likes_target_id', LikeBase.target_id, postgresql_using='btree')


class LocationBase(Base):

    __tablename__ = 'locations'

    id = Column('id', Integer(), primary_key=True)
    address = Column('address', String(255), nullable=True)
    lat = Column('lat', String(255), nullable=True)
    lng = Column('lng', String(255), nullable=True)
    status_message_id = Column('status_message_id', Integer(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)


class MentionBase(Base):

    __tablename__ = 'mentions'

    id = Column('id', Integer(), primary_key=True)
    post_id = Column('post_id', Integer(), nullable=False)
    person_id = Column('person_id', Integer(), nullable=False)

Index('idx_mentions_person_id_post_id', MentionBase.person_id,
      MentionBase.post_id, unique=True, postgresql_using='btree')
Index('idx_mentions_person_id', MentionBase.person_id,
      postgresql_using='btree')
Index('idx_mentions_post_id', MentionBase.post_id, postgresql_using='btree')


class MessageBase(Base):

    __tablename__ = 'messages'

    id = Column('id', Integer(), primary_key=True)

    conversation_id = Column('conversation_id', Integer(),
                             ForeignKey('conversations.id',
                                        name='fk_messages_conversation_id',
                                        ondelete='CASCADE'), nullable=False)
    author_id = Column('author_id', Integer(),
                       ForeignKey('people.id',
                                  name='fk_messages_author_id',
                                  ondelete='CASCADE'), nullable=False)
    guid = Column('guid', String(255), nullable=False)
    text = Column('text', Text(), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    author_signature = Column('author_signature', Text(),
                              nullable=True)
    parent_author_signature = Column('parent_author_signature', Text(),
                                     nullable=True)

Index('idx_messages_author_id', MessageBase.author_id,
      postgresql_using='btree')
Index('idx_messages_conversation_id', MessageBase.conversation_id,
      postgresql_using='btree')


class NotificationActorBase(Base):

    __tablename__ = 'notification_actors'

    id = Column('id', Integer(), primary_key=True)
    notification_id = Column(
        'notification_id', Integer(),
        ForeignKey('notifications.id',
                   name='fk_notification_actors_notification_id',
                   ondelete='CASCADE'), nullable=True)
    person_id = Column('person_id', Integer(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_notification_actors_notification_id_person_id',
      NotificationActorBase.notification_id, NotificationActorBase.person_id,
      unique=True, postgresql_using='btree')
Index('idx_notification_actors_notification_id',
      NotificationActorBase.notification_id, postgresql_using='btree')
Index('idx_notification_actors_person_id', NotificationActorBase.person_id,
      postgresql_using='btree')


class NotificationBase(Base):

    __tablename__ = 'notifications'

    id = Column('id', Integer(), primary_key=True)
    target_type = Column('target_type', String(255), nullable=True)
    target_id = Column('target_id', Integer(), nullable=True)
    recipient_id = Column('recipient_id', Integer(), nullable=False)
    unread = Column('unread', Boolean(), DefaultClause('True'), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    type = Column('type', String(255), nullable=True)

Index('idx_notifications_recipient_id', NotificationBase.recipient_id,
      postgresql_using='btree')
Index('idx_notifications_target_id', NotificationBase.target_id,
      postgresql_using='btree')
Index('idx_notifications_target_type_target_id', NotificationBase.target_type,
      NotificationBase.target_id, postgresql_using='btree')


class OEmbedCache(Base):

    __tablename__ = 'o_embed_caches'

    id = Column('id', Integer(), primary_key=True)
    url = Column('url', String(1024), nullable=False)
    data = Column('data', Text(), nullable=False)

Index('idx_o_embed_caches_url', OEmbedCache.url, postgresql_using='btree')


class OpenGraphCache(Base):

    __tablename__ = 'open_graph_caches'

    id = Column('id', Integer(), primary_key=True)
    title = Column('title', String(255), nullable=True)
    ob_type = Column('ob_type', String(255), nullable=True)
    image = Column('image', Text(), nullable=True)
    url = Column('url', Text(), nullable=True)
    description = Column('description', Text(), nullable=True)


class Participation(Base):

    __tablename__ = 'participations'

    id = Column('id', Integer(), primary_key=True)
    guid = Column('guid', String(255), nullable=True)
    target_id = Column('target_id', Integer(), nullable=True)
    target_type = Column('target_type', String(60), nullable=False)
    author_id = Column('author_id', Integer(), nullable=True)
    author_signature = Column('author_signature', Text(),
                              nullable=True)
    parent_author_signature = Column('parent_author_signature', Text(),
                                     nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_participations_guid', Participation.guid, postgresql_using='btree')
Index('idx_participations_target_id_target_type_author_id',
      Participation.target_id, Participation.target_type,
      Participation.author_id, postgresql_using='btree')


class PersonBase(Base):

    __tablename__ = 'people'

    id = Column('id', Integer(), primary_key=True)
    guid = Column('guid', String(255), nullable=False)
    url = Column('url', Text, nullable=False)
    diaspora_handle = Column('diaspora_handle', String(255),
                             nullable=False)
    serialized_public_key = Column('serialized_public_key', Text,
                                   nullable=False)
    owner_id = Column('owner_id', Integer(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    closed_account = Column('closed_account', Boolean(),
                            DefaultClause('False'), nullable=True)
    fetch_status = Column('fetch_status', Integer(), DefaultClause('0'),
                          nullable=True)

Index('idx_people_diaspora_handle', PersonBase.diaspora_handle, unique=True,
      postgresql_using='btree')
Index('idx_people_guid', PersonBase.guid, unique=True,
      postgresql_using='btree')
Index('idx_people_owner_id', PersonBase.owner_id, unique=True,
      postgresql_using='btree')


class PhotoBase(Base):

    __tablename__ = 'photos'

    id = Column('id', Integer(), primary_key=True)
    tmp_old_id = Column('tmp_old_id', Integer(), nullable=True)
    author_id = Column('author_id', Integer(), nullable=False)
    public = Column('public', Boolean(), DefaultClause('False'),
                    nullable=False)
    diaspora_handle = Column('diaspora_handle', String(255),
                             nullable=True)
    guid = Column('guid', String(255), nullable=False)
    pending = Column('pending', Boolean(), DefaultClause('False'),
                     nullable=False)
    text = Column('text', Text(), nullable=True)
    remote_photo_path = Column('remote_photo_path', Text(), nullable=True)
    remote_photo_name = Column('remote_photo_name', String(255),
                               nullable=True)
    random_string = Column('random_string', String(255), nullable=True)
    processed_image = Column('processed_image', String(255), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=True)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=True)
    unprocessed_image = Column('unprocessed_image', String(255), nullable=True)
    status_message_guid = Column('status_message_guid', String(255),
                                 nullable=True)
    comments_count = Column('comments_count', Integer(), nullable=True)
    height = Column('height', Integer(), nullable=True)
    width = Column('width', Integer(), nullable=True)

Index('idx_photos_status_message_guid', PhotoBase.status_message_guid,
      postgresql_using='btree')


class PodBase(Base):

    __tablename__ = 'pods'

    id = Column('id', Integer(), primary_key=True)
    host = Column('host', String(255), nullable=True)
    ssl = Column('ssl', Boolean(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    status = Column('status', Integer(), DefaultClause('0'), nullable=True)
    checked_at = Column('checked_at', TIMESTAMP(), nullable=False)
    offline_since = Column('offline_since', TIMESTAMP(), nullable=False)
    response_time = Column('response_time', Integer(), DefaultClause('-1'),
                           nullable=True)
    software = Column('software', String(255), nullable=True)
    error = Column('error', String(255), nullable=True)

Index('idx_pods_host', PodBase.host, unique=True, postgresql_using='btree')
Index('idx_pods_checked_at', PodBase.checked_at, postgresql_using='btree')
Index('idx_pods_offline_since', PodBase.offline_since,
      postgresql_using='btree')
Index('idx_pods_response_time', PodBase.response_time,
      postgresql_using='btree')


class PollAnswerBase(Base):

    __tablename__ = 'poll_answers'

    id = Column('id', Integer(), primary_key=True)
    answer = Column('answer', String(255), nullable=False)
    # TODO:  poll_id not FK ?
    poll_id = Column('poll_id', Integer(), nullable=False)
    guid = Column('guid', String(255), nullable=True)
    vote_count = Column('vote_count', Integer(), DefaultClause('0'),
                        nullable=True)

Index('idx_poll_answers_poll_id', PollAnswerBase.poll_id,
      postgresql_using='btree')


class PollParticipationBase(Base):

    __tablename__ = 'poll_participations'

    # TODO:  No Fks here too ?
    id = Column('id', Integer(), primary_key=True)
    poll_answer_id = Column('poll_answer_id', Integer(), nullable=False)
    author_id = Column('author_id', Integer(), nullable=False)
    poll_id = Column('poll_id', Integer(), nullable=False)
    guid = Column('guid', String(255), nullable=True)
    author_signature = Column('author_signature', Text(),
                              nullable=True)
    parent_author_signature = Column('parent_author_signature', Text(),
                                     nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=True)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=True)

Index('idx_poll_participations_poll_id', PollParticipationBase.poll_id,
      postgresql_using='btree')


class PollsBase(Base):

    __tablename__ = 'polls'

    id = Column('id', Integer(), primary_key=True)
    question = Column('question', String(255), nullable=False)
    status_message_id = Column('status_message_id', Integer(), nullable=False)
    status = Column('status', Boolean(), nullable=True)
    guid = Column('guid', String(255), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=True)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=True)

Index('idx_polls_status_message_id', PollsBase.status_message_id,
      postgresql_using='btree')


class PostBase(Base):

    __tablename__ = 'posts'

    id = Column('id', Integer(), primary_key=True)
    author_id = Column('author_id', Integer(),
                       ForeignKey('people.id', name='fk_posts_author_id',
                                  ondelete='CASCADE'), nullable=False)
    public = Column('public', Boolean(), DefaultClause('false'),
                    nullable=False)
    diaspora_handle = Column('diaspora_handle', String(255), nullable=True)
    guid = Column('guid', String(255), nullable=False)
    pending = Column('pending', Boolean(), DefaultClause('false'),
                     nullable=False)
    type = Column('type', String(40), nullable=False)
    text = Column('text', Text(), nullable=True)
    remote_photo_path = Column('remote_photo_path', Text(), nullable=True)
    remote_photo_name = Column('remote_photo_name', String(255), nullable=True)
    random_string = Column('random_string', String(255), nullable=True)
    processed_image = Column('processed_image', String(255), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    unprocessed_image = Column('unprocessed_image', String(255), nullable=True)
    object_url = Column('object_url', String(255), nullable=True)
    image_url = Column('image_url', String(255), nullable=True)
    image_height = Column('image_height', Integer(), nullable=True)
    image_width = Column('image_width', Integer(), nullable=True)
    provider_display_name = Column('provider_display_name', String(255),
                                   nullable=True)
    actor_url = Column('actor_url', String(255), nullable=True)
    objectId = Column('objectId', String(255), nullable=True)
    root_guid = Column('root_guid', String(255), nullable=True)
    status_message_guid = Column('status_message_guid', String(255),
                                 nullable=True)
    likes_count = Column('likes_count', Integer(), DefaultClause('0'),
                         nullable=True)
    comments_count = Column('comments_count', Integer(), DefaultClause('0'),
                            nullable=True)
    o_embed_cache_id = Column('o_embed_cache_id', Integer(), nullable=True)
    reshares_count = Column('reshares_count', Integer(), DefaultClause('0'),
                            nullable=True)
    interacted_at = Column('interacted_at', TIMESTAMP(), nullable=True)
    frame_name = Column('frame_name', String(255), nullable=True)
    favorite = Column('favorite', Boolean(), DefaultClause('false'),
                      nullable=True)
    facebook_id = Column('facebook_id', String(255), nullable=True)
    tweet_id = Column('tweet_id', String(255), nullable=True)
    open_graph_cache_id = Column('open_graph_cache_id', Integer(),
                                 nullable=True)
    tumblr_ids = Column('tumblr_ids', Text(), nullable=True)

Index('idx_posts_author_id_root_guid', PostBase.author_id,
      PostBase.root_guid, unique=True, postgresql_using='btree')
Index('idx_posts_guid', PostBase.guid, unique=True,
      postgresql_using='btree')
Index('idx_posts_author_id', PostBase.author_id, postgresql_using='btree')
Index('idx_posts_id_type_created_at', PostBase.id, PostBase.type,
      PostBase.created_at, postgresql_using='btree')
Index('idx_posts_root_guid', PostBase.root_guid, postgresql_using='btree')
Index('idx_posts_status_message_guid', PostBase.status_message_guid,
      postgresql_using='btree')
Index('idx_posts_status_message_guid_pending', PostBase.status_message_guid,
      PostBase.pending, postgresql_using='btree')
Index('idx_posts_tweet_id', PostBase.tweet_id, postgresql_using='btree')
Index('idx_posts_type_pending_id', PostBase.type, PostBase.pending,
      PostBase.id, postgresql_using='btree')


class ProfileBase(Base):

    __tablename__ = 'profiles'

    id = Column('id', Integer(), primary_key=True)
    diaspora_handle = Column('diaspora_handle', String(255), nullable=True)
    first_name = Column('first_name', String(127), nullable=True)
    last_name = Column('last_name', String(127), nullable=True)
    image_url = Column('image_url', String(255), nullable=True)
    image_url_small = Column('image_url_small', String(255), nullable=True)
    image_url_medium = Column('image_url_medium', String(255), nullable=True)
    birthday = Column('birthday', Date(), nullable=True)
    gender = Column('gender', String(255), nullable=True)
    bio = Column('bio', Text(), nullable=True)
    searchable = Column('searchable', Boolean(), DefaultClause('true'),
                        nullable=False)
    person_id = Column('person_id', Integer(),
                       ForeignKey('people.id', name='fk_profiles_person_id',
                                  ondelete='CASCADE'),
                       nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    location = Column('location', String(255), nullable=True)
    full_name = Column('full_name', String(70), nullable=True)
    nsfw = Column('nsfw', Boolean(), DefaultClause('false'), nullable=True)

Index('idx_profiles_full_name', ProfileBase.full_name,
      postgresql_using='btree')
Index('idx_profiles_full_name_searchable', ProfileBase.full_name,
      ProfileBase.searchable, postgresql_using='btree')
Index('idx_profiles_person_id', ProfileBase.person_id,
      postgresql_using='btree')


class ReportBase(Base):

    __tablename__ = 'reports'

    id = Column('id', Integer(), primary_key=True)
    item_id = Column('item_id', Integer(), nullable=False)
    item_type = Column('item_type', String(255), nullable=False)
    reviewed = Column('reviewed', Boolean(), DefaultClause('false'),
                      nullable=True)
    text = Column('text', Text(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=True)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=True)
    user_id = Column('user_id', Integer(), nullable=False)

Index('idx_reports_item_id', ReportBase.item_id, postgresql_using='btree')


class RoleBase(Base):

    __tablename__ = 'roles'

    id = Column('id', Integer(), primary_key=True)
    person_id = Column('person_id', Integer(), nullable=True)
    name = Column('name', String(255), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)


class SchemaMigrationBase(Base):

    __tablename__ = 'schema_migrations'

    # On diaspora* this table has no pk!
    id = Column('id', Integer(), primary_key=True)
    version = Column('version', String(255), nullable=False)

Index('idx_schema_migrations_version', SchemaMigrationBase.version,
      unique=True, postgresql_using='btree')


class ServiceBase(Base):

    __tablename__ = 'services'

    id = Column('id', Integer(), primary_key=True)
    type = Column('type', String(127), nullable=False)
    user_id = Column('user_id', Integer(),
                     ForeignKey('users.id', name='fk_services_user_id',
                                ondelete='CASCADE'),
                     nullable=False)
    uid = Column('uid', String(127), nullable=True)
    access_token = Column('access_token', String(255), nullable=True)
    access_secret = Column('access_secret', String(255), nullable=True)
    nickname = Column('nickname', String(255), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_services_type_uid', ServiceBase.type, ServiceBase.uid,
      postgresql_using='btree')
Index('idx_services_user_id', ServiceBase.user_id, postgresql_using='btree')


class ShareVisibilityBase(Base):

    __tablename__ = 'share_visibilities'

    id = Column('id', Integer(), primary_key=True)
    shareable_id = Column('shareable_id', Integer(), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    hidden = Column('hidden', Boolean(), DefaultClause('false'),
                    nullable=False)
    contact_id = Column('contact_id', Integer(),
                        ForeignKey('contacts.id',
                                   name='fk_post_visibilities_contact_id',
                                   ondelete='CASCADE'),
                        nullable=False)
    shareable_type = Column('shareable_type', String(60),
                            DefaultClause('Post'), nullable=False)

Index('idx_share_visibilities_contact_id', ShareVisibilityBase.contact_id,
      postgresql_using='btree')
Index('idx_share_visibilities_shareable_id', ShareVisibilityBase.shareable_id,
      postgresql_using='btree')
Index('idx_share_visibilities_shareable_id_shareable_type_contact_id',
      ShareVisibilityBase.shareable_id, ShareVisibilityBase.shareable_type,
      ShareVisibilityBase.contact_id, postgresql_using='btree')
Index('idx_share_visibilities_shareable_id_shareable_type_hidden_conta',
      ShareVisibilityBase.shareable_id, ShareVisibilityBase.shareable_type,
      ShareVisibilityBase.hidden, ShareVisibilityBase.contact_id,
      postgresql_using='btree')


class SimpleCaptchaDataBase(Base):

    __tablename__ = 'simple_captcha_data'

    id = Column('id', Integer(), primary_key=True)
    key = Column('key', String(40), nullable=True)
    value = Column('value', String(12), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=True)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=True)

Index('idx_simple_captcha_data_key', SimpleCaptchaDataBase.key,
      postgresql_using='btree')


class TagFollowingBase(Base):

    __tablename__ = 'tag_followings'

    id = Column('id', Integer(), primary_key=True)
    # TODO: No fks here too?!
    tag_id = Column('tag_id', Integer(), nullable=False)
    user_id = Column('user_id', Integer(), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_tag_followings_tag_id_user_id', TagFollowingBase.tag_id,
      TagFollowingBase.user_id, unique=True, postgresql_using='btree')
Index('idx_tag_followings_tag_id', TagFollowingBase.tag_id,
      postgresql_using='btree')
Index('idx_tag_followings_user_id', TagFollowingBase.user_id,
      postgresql_using='btree')


class TaggingBase(Base):

    __tablename__ = 'taggings'

    id = Column('id', Integer(), primary_key=True)
    # TODO: No fks here too?!
    tag_id = Column('tag_id', Integer(), nullable=True)
    taggable_id = Column('taggable_id', Integer(), nullable=True)
    taggable_type = Column('taggable_type', String(127), nullable=True)
    tagger_id = Column('tagger_id', Integer(), nullable=True)
    tagger_type = Column('tagger_type', String(127), nullable=True)
    context = Column('context', String(127), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=True)

Index('idx_taggings_taggable_id_taggable_type_tag_id', TaggingBase.taggable_id,
      TaggingBase.taggable_type, TaggingBase.tag_id, unique=True,
      postgresql_using='btree')
Index('idx_taggings_created_at', TaggingBase.created_at,
      postgresql_using='btree')
Index('idx_taggings_tag_id', TaggingBase.tag_id, postgresql_using='btree')
Index('idx_taggings_taggable_id_taggable_type_context',
      TaggingBase.taggable_id, TaggingBase.taggable_type, TaggingBase.context,
      postgresql_using='btree')


class TagBase(Base):

    __tablename__ = 'tags'

    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(255), nullable=True)
    taggings_count = Column('taggings_count', Integer(), DefaultClause('0'),
                            nullable=True)

Index('idx_tags_name', TagBase.name, unique=True,
      postgresql_using='btree')


class UserPreferenceBase(Base):

    __tablename__ = 'user_preferences'

    id = Column('id', Integer(), primary_key=True)
    email_type = Column('email_type', String(255), nullable=True)
    # TODO: No FK here too!
    user_id = Column('user_id', Integer(), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)


# TODO: Follow that doc
# http://stackoverflow.com/questions/6151084/which-timestamp-type-should-i-choose-in-a-postgresql-database
# http://stackoverflow.com/questions/13677781/getting-sqlalchemy-to-issue-create-schema-on-create-all
class UserBase(Base):

    __tablename__ = 'users'

    id = Column('id', Integer(), primary_key=True)
    user_name = Column('username', String(255), nullable=True)
    serialized_private_key = Column('serialized_private_key', Text,
                                    nullable=True)
    getting_started = Column('getting_started', Boolean(),
                             DefaultClause('True'), nullable=False)
    disable_mail = Column('disable_mail', Boolean(),
                          DefaultClause('False'), nullable=False)
    language = Column('language', String(255), nullable=True)
    email = Column('email', String(255), DefaultClause(''), nullable=False)
    encrypted_password = Column('encrypted_password', String(255),
                                DefaultClause(''), nullable=False)
    invitation_token = Column('invitation_token', String(60), nullable=True)
    invitation_sent_at = Column('invitation_sent_at', TIMESTAMP(),
                                nullable=True)
    reset_password_token = Column('reset_password_token', String(255),
                                  nullable=True)
    remember_created_at = Column('remember_created_at', TIMESTAMP(),
                                 nullable=True)
    sign_in_count = Column('sign_in_count', Integer(),
                           DefaultClause('0'), nullable=True)
    current_sign_in_at = Column('current_sign_in_at', TIMESTAMP(),
                                nullable=True)
    last_sign_in_at = Column('last_sign_in_at', TIMESTAMP(), nullable=True)
    current_sign_in_ip = Column('current_sign_in_ip', String(255),
                                nullable=True)
    last_sign_in_ip = Column('last_sign_in_ip', String(255), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    invitation_service = Column('invitation_service', String(127),
                                nullable=True)
    invitation_identifier = Column('invitation_identifier', String(127),
                                   nullable=True)
    invitation_limit = Column('invitation_limit', Integer(), nullable=True)
    invited_by_id = Column('invited_by_id', Integer(), nullable=True)
    invited_by_type = Column('invited_by_type', String(255), nullable=True)
    authentication_token = Column('authentication_token', String(30),
                                  nullable=True)
    unconfirmed_email = Column('unconfirmed_email', String(255), nullable=True)
    confirm_email_token = Column('confirm_email_token', String(30),
                                 nullable=True)
    locked_at = Column('locked_at', TIMESTAMP(), nullable=True)
    show_community_spotlight_in_stream = Column(
        'show_community_spotlight_in_stream', Boolean(), DefaultClause('True'),
        nullable=False)
    auto_follow_back = Column('auto_follow_back', Boolean(),
                              DefaultClause('False'), nullable=True)
    auto_follow_back_aspect_id = Column('auto_follow_back_aspect_id',
                                        Integer(), nullable=True)
    hidden_shareables = Column('hidden_shareables', Text, nullable=True)
    reset_password_sent_at = Column('reset_password_sent_at', TIMESTAMP(),
                                    nullable=True)
    last_seen = Column('last_seen', TIMESTAMP(), nullable=True)
    remove_after = Column('remove_after', TIMESTAMP(), nullable=True)
    export = Column('export', String(255), nullable=True)
    exported_at = Column('exported_at', TIMESTAMP(), nullable=True)
    exporting = Column('exporting', Boolean(), DefaultClause('False'),
                       nullable=True)
    strip_exif = Column('strip_exif', Boolean(), DefaultClause('True'),
                        nullable=True)
    exported_photos_file = Column('exported_photos_file', String(255),
                                  nullable=True)
    exported_photos_at = Column('exported_photos_at', TIMESTAMP(),
                                nullable=True)
    exporting_photos = Column('exporting_photos', Boolean(),
                              DefaultClause('False'), nullable=True)

Index('idx_users_authentication_token', UserBase.authentication_token,
      unique=True, postgresql_using='btree')
Index('idx_users_invitation_service_invitation_identifier',
      UserBase.invitation_service, UserBase.invitation_identifier, unique=True,
      postgresql_using='btree')
Index('idx_users_username', UserBase.user_name, unique=True,
      postgresql_using='btree')
Index('idx_users_email', UserBase.email, postgresql_using='btree')
Index('idx_users_invitation_token', UserBase.authentication_token,
      postgresql_using='btree')
