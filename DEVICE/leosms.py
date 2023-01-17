# Import the necessary modules
import jnius
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

# Get the Android SmsMessage class
SmsMessage = jnius.autoclass('android.telephony.SmsMessage')

# Get the Android ContentResolver class
ContentResolver = jnius.autoclass('android.content.ContentResolver')

# Get the Android Uri class
Uri = jnius.autoclass('android.net.Uri')
activity = jnius.autoclass("org.kivy.android.PythonActivity").mActivity
# Get the Android Telephony class
Telephony = jnius.autoclass('android.provider.Telephony')
# Define the URI for the SMS inbox
inbox_uri = Uri.parse("content://sms/inbox")
# inbox_uri = Uri.parse("content://sms/sent")


# Get the content resolver for the current context
content_resolver = activity.getContentResolver()
class SMSReaderApp:
    def get_message(cursor):
        print(
            cursor.getString(cursor.getColumnIndex('_id')),
            cursor.getString(cursor.getColumnIndex('address')),
            cursor.getString(cursor.getColumnIndex('body'))
        )
        # Query the SMS inbox

    def fetch_messages():
        cursor = content_resolver.query(
            inbox_uri,
            ['_id', 'address', 'body', 'type', 'read'],
            None, None,
            None)
        if cursor and cursor.getCount():
            print("cursor count", cursor.getCount())
            cursor.moveToFirst()
            print(cursor)
            print(type(cursor))
            messages = []
            while cursor.moveToNext():
                message = [cursor.getString(cursor.getColumnIndex('_id')),
                           cursor.getString(cursor.getColumnIndex('address')),
                           cursor.getString(cursor.getColumnIndex('body'))]
                messages.append(message)
            print(messages)

    def fetch(self, offset, *args):
        self.fetch_messages()

