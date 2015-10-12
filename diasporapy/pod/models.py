#!/usr/bin/env python
#
# Copyright 2015 Flavio Garcia
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
#
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Text, Boolean, String
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
    aspect_id = Column('aspect_id', Integer(), ForeignKey('aspects.id'),
                       nullable=False)
    contact_id = Column('contact_id', Integer(), ForeignKey('contacts.id'),
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
    aspect_id = Column('aspect_id', Integer(), ForeignKey('aspects.id'),
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
      ChatContactBase.jid, postgresql_using='btree')


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
    author_id = Column('author_id', Integer(), ForeignKey('people.id'),
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
    person_id = Column('person_id', Integer(), ForeignKey('people.id'),
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
    conversation_id = Column('conversation_id', Integer(),
                             ForeignKey('conversations.id'), nullable=False)
    person_id = Column('person_id', Integer(), ForeignKey('people.id'),
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
    author_id = Column('author_id', Integer(), ForeignKey('people.id'),
                       nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)

Index('idx_conversations_author_id', ConversationBase.author_id,
      postgresql_using='btree')


class InvitationCodesBase(Base):

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
    sender_id = Column('sender_id', Integer(), ForeignKey('users.id'),
                       nullable=True)
    recipient_id = Column('recipient_id', Integer(), ForeignKey('users.id'),
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
    language = Column('language', String(255), nullable=True, unique=True)
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
                                  nullable=True, unique=True)
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
    exporting_photos = Column( 'exporting_photos', Boolean(),
                               DefaultClause('False'),nullable=True)
    preferences = relationship("UserPreferenceBase", backref="user")


class UserPreferenceBase(Base):

    __tablename__ = 'user_preferences'

    id = Column('id', Integer(), primary_key=True)
    email_type = Column('email_type', String(255), nullable=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'), nullable=True)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)


class PeopleBase(Base):

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
                            DefaultClause('False'),nullable=True)
    fetch_status = Column('fetch_status', Integer(), DefaultClause('0'),
                          nullable=True)


class TagBase(Base):

    __tablename__ = 'tags'

    id = Column('id', Integer(), primary_key=True)
    name = Column('name', String(255), nullable=False)
    taggings_count = Column('taggings_count', Integer(), DefaultClause('0'),
                            nullable=False)
