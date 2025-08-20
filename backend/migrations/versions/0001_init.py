from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sender_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('recipient_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted', sa.Boolean, server_default=sa.false()),
    )

    op.create_table(
        'attachments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('message_id', sa.Integer, sa.ForeignKey('messages.id', ondelete='CASCADE')),
        sa.Column('file_path', sa.String(512), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('uploaded_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_messages_sender', 'messages', ['sender_id'])
    op.create_index('ix_messages_recipient', 'messages', ['recipient_id'])
    op.create_index('ix_attachments_message', 'attachments', ['message_id'])


def downgrade():
    op.drop_table('attachments')
    op.drop_table('messages')
    op.drop_table('users')
