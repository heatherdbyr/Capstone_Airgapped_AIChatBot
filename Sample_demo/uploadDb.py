from elasticsearch import Elasticsearch, helpers

# Connect to local Elasticsearch instance

#Elastic configs & start 
ELASTIC_PASSWORD = "PPU90SH8Bt6kF3feQ3YpCqmM"

CLOUD_ID = "First_Deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ1ZDc5MWEyZTE3Mzc0MGQwOThmOTQ1Yjc2OWU5MzhkZCQ5NWI0NDY4YTAyM2Q0YmM0YmFlOWEzNDdhNjA1OGFkNA=="
es = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)
# Sample database
db = {
    "Articles": [
        {
            "article": {
                "Title": "Add an email account to Outlook",
                "Link": "https://support.microsoft.com/en-us/office/add-an-email-account-to-outlook-e9da47c4-9b89-4b49-b945-a204aeea6726",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "With Outlook on your PC, Mac or mobile device, you can:",
                            "sub_content": "Organize your email to focus on the messages that matter most. Manage your calendar to schedule meetings and appointments. Share files from the cloud so everyone always has the latest version. Stay connected and productive wherever you are."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Add an email account",
                            "sub_content": "Open Outlook and select File > Add Account. If you haven't launched Outlook before, you'll see a welcome screen. Enter your email address and select Connect. If your screen looks different, enter your name, email address, and password, and select Next. If prompted, enter your password and select OK. Select Finish."
                        }
                    }
                ]
            }
        },
        {
            "article": {
                "Title": "Create and send email in Outlook",
                "Link": "https://support.microsoft.com/en-us/office/create-and-send-email-in-outlook-19c32deb-08b6-4f90-a211-02bc5f77f360",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Create and send email",
                            "sub_content": "Choose New Email to start a new message. Enter a name or email address in the To, Cc, or Bcc field. If you don't see Bcc, see Show, hide, and view the Bcc box. In Subject, type the subject of the email message. Place the cursor in the body of the email message, and then start typing. After typing your message, choose Send."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Use @mentions to get someone's attention",
                            "sub_content": "In the body of the email message or calendar invite, enter the @ symbol and the first few letters of the contact's first or last name. When Outlook offers you one or more suggestions, choose the contact you want to mention. By default, their full name is included. You can delete a portion of the mention, for example, everything other than the person's first name. The mentioned contact is added to the To line of the email or the meeting invite."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Focused Inbox",
                            "sub_content": "Focused Inbox helps you focus on the emails that matter most. It separates your inbox into two tabs—Focused and Other. If messages aren't sorted the way you like, you can move them and set where to deliver future messages from that sender. Select the Focused or Other tab. Right-click the message you want to move and select Move to Other or Move to Focused. To turn the Focused Inbox on or off: Select View > Show Focused Inbox."
                        }
                    }
                ]
            }
        },
        {
            "article": {
                "Title": "Collaborate in Outlook",
                "Link": "https://support.microsoft.com/en-us/office/collaborate-in-outlook-63bf693d-76d4-410b-89d2-a3b63c729c22",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Share a file to collaborate on attachments",
                            "sub_content": "Select Attach File and choose a file. If the file has a small cloud icon, it's already saved to the cloud, which lets you share and work on it with others. If it doesn't, click the drop-down arrow, hover on Upload, and then select OneDrive. Type a message and select Send."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Set up an online meeting and shared notes",
                            "sub_content": "In the left pane, select the Calendar icon. To set up a meeting attendees can join remotely, select New Teams Meeting. This inserts a link remote attendees can use to join the meeting. To set up a shared space for notes, select Meeting Notes. You can create a new OneNote notebook, or select an existing notebook. A link to the notebook appears in the meeting request."
                        }
                    }
                ]
            }
        }, 
        {
            "article": {
                "Title": "Set up your Outlook mobile app",
                "Link": "https://support.microsoft.com/en-us/office/set-up-your-outlook-mobile-app-a2658b93-ca21-42fb-9f19-a61662f669fe",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Get to your files from anywhere",
                            "sub_content": "Set up the Office apps on your mobile device. Choose your mobile device: iOS, Android. For more info, see Set up Office apps and email on a mobile device."
                        }
                    }
                ]
            }
        }, 
        {
            "article": {
                "Title": "Create, change, or customize a view",
                "Link": "https://support.microsoft.com/en-us/office/create-change-or-customize-a-view-f693f3d9-0037-4fa0-9376-3a57b6337b71#view-types",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Views give you different ways to look at items in a folder.",
                            "sub_content": "Each Outlook folder, such as Inbox and Calendar, allows you to customize your view to change fonts, the organization of items, and many other settings."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Types of views",
                            "sub_content": "There are several different types of views you can choose when creating a new view. These include Table, Timeline, Card, Business Card, People, Day/Week/Month, and Icon views."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Change the font or font size in the message list",
                            "sub_content": "Select View > View Settings. Select Other Settings in the Advanced View Settings box. Select Column Font or Row Font. To change the font size of the message preview, sender name, and subject in the default Inbox view, choose Row Font. Select the font, font style, and size you want, then click OK three times to save your settings and apply your changes."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Change your font or font size in the Reading Pane",
                            "sub_content": "The Reading Pane doesn't allow you to change the default font or font size. However, you can zoom in or zoom out easily. You can also tell Outlook to display all of your email messages in plain text, and have more control over the font size."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Change the font size for messages when composing, replying, or forwarding",
                            "sub_content": "Select File > Options > Mail > Stationery and Fonts. Select the Font button for New mail messages or Replying or forwarding messages to change the default font, font size, and font color when composing or replying to messages. Click OK twice to save your changes."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Remove the dark background",
                            "sub_content": "Go to toolbar and select File, then select Office Account. Under Office Theme, select White or Colorful. For more details about dark mode, see Dark Mode in Outlook."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Move the navigation bar",
                            "sub_content": "For instructions, see Customize the Navigation Bar."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Create a new view",
                            "sub_content": "Sometimes, it's easier to start with a new view rather than modifying an existing view. You can create a new view in any Outlook folder. Click View > Current View> Change View > Manage Views > New. If you want to start from an existing view, in the Manage All Views dialog box, select <Current view settings> and then select Copy. Enter a name for your new view, and then choose the type of view. Under Can be used on, accept the default setting of All Mail and Post folders or choose another option, and then choose OK. In the Advanced View Settings: New View dialog box, choose the options that you want to use, and then choose OK. To use the view immediately, choose Apply View."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Delete a custom view",
                            "sub_content": "You can't delete a predefined view, even if you've changed its settings. On the View tab, in the Current View group, choose Change View > Manage Views. Under Views for folder, select the custom view that you want to remove. Choose Delete, confirm deletion, and then choose OK."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Apply the current view to multiple folders",
                            "sub_content": "On the View tab, in the Current View group, choose Change View > Apply Current View to Other Mail Folders. In the Apply View dialog box, select each folder that you want to apply the view to. (A small check mark appears next to the folder name to indicate it is selected. Select OK."
                        }
                    }
                ]
            }
        }, 
        {
            "article": {
                "Title": "Change how you view your Outlook calendar",
                "Link": "https://support.microsoft.com/en-us/office/change-how-you-view-your-outlook-calendar-a4e0dfd2-89a1-4770-9197-a3e786f4cd8f",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Keep upcoming calendar items visible",
                            "sub_content": "Keep your upcoming appointments and meetings in view by opening the Calendar peek on the right side of your Mail.\n\nRight-click Calendar on the Navigation Bar, and then click Dock the peek.\n\nLearn more about keeping your calendar, appointments, and meetings always in view."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Change to Month view with a Monday start date and show U.S. holidays",
                            "sub_content": "View the Calendar by month to see what you are doing at-a-glance. A common way to view the calendar is by setting the work week to start on a Monday, with U.S. holidays.\n\nClick Calendar.\n\nClick Home > Arrange > Month.\n\nClick the File tab.\n\nClick Options, and then click Calendar.\n\nUnder Work time, for First day of week, select Monday.\n\nUnder Calendar options, for Add holidays to the Calendar, click Add Holidays.\n\nClick United States, and then click OK.\n\nLearn more about adding holidays to your calendar."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Change Work Week view to Sunday-Tuesday with 12-hr days (non-traditional work week)",
                            "sub_content": "If you work a non-traditional work schedule, you can set your Work Week view to only show those working times. For example, if you are a nurse you may only want to view your Sunday – Tuesday, 12-hour shift at the hospital.\n\nClick Calendar.\n\nClick Home > Arrange > Work Week.\n\nClick the File tab.\n\nClick Options, and then click Calendar.\n\nUnder Work time, for Start time, select 6:00 AM.\n\nUnder Work time, for End time, select 6:00 PM.\n\nFor Work week, select Sun, Mon, and Tue and clear any other selected check boxes.\n\nFor First day of week, select Sunday.\n\nClick OK.\n\nTip: To view all your hours during a long shift in the Work Week view, use Zoom in the bottom-right corner of the Calendar to make it smaller."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "View two time zones in the Week view",
                            "sub_content": "When working with partners in different time zones, it’s helpful to see both time zones in the Week view. For example, when I schedule meetings from the New York office (Eastern time zone), I want to view my Australian co-worker's schedule (Brisbane time zone) so I don’t book her during non-working hours.\n\nClick Calendar.\n\nClick Home > Arrange > Week.\n\nRight-click the empty space at the top of the time bar, and then click Change Time Zone on the shortcut menu.\n\nUnder Time zones, type Eastern Time Zone in the Label box.\n\nIn the Time zone list, click (UTC-05:00) Eastern Time (US & Canada).\n\nSelect Show a second time zone.\n\nType Brisbane in the Label box.\n\nIn the Time zone list, click (UTC+ 10:00) Brisbane.\n\nClick OK.\n\nLearn more about how time-zone normalization works."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Looking for something else?",
                            "sub_content": "If you find yourself filtering calendar items or modifying fields, you can easily create a custom view so the information you need is always available.\n\nClick View.\n\nIn the Current View group, click Change View, and then click Manage Views.\n\nClick New.\n\nIn the Name of new view box, type a name for the view.\n\nIn the Type of view box, select a view type.\n\nTo change where the view is available, select an option under Can be used on, and then click OK.\n\nIn the Advanced View Settings: New View dialog box, select the options that you want to use.\n\nWhen you are finished selecting options, click OK.\n\nTo use the view immediately, click Apply View.\n\nLearn more about changing or customizing a view."
                        }
                    }
                ]
            }
        }, 
        {
            "article": {
                "Title": "Keep upcoming appointments and meetings always in view",
                "Link": "https://support.microsoft.com/en-us/office/keep-upcoming-appointments-and-meetings-always-in-view-0e5f30da-c44d-4b96-8fd9-ba5d10db0962",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Dock the Calendar peek to the Outlook window",
                            "sub_content": "When you point to the Calendar icon on the navigation bar, the Calendar peek shows your upcoming appointments and meetings. To always be able to see your upcoming items, dock the Calendar peek to the Outlook window.\n\nClick the icon (highlighted in red in the picture) or right-click the calendar icon on the navigation bar, then select Dock the Peek.\n\nTo close the peek, at the top of the docked Calendar peek, click the close icon.\n\nWhen a peek is docked or not docked it only affects that view. For example, if you’re in Mail and pin the Calendar peek, when you switch to Tasks, the Calendar peek doesn’t appear. You can dock or undock the Calendar peek in each view by clicking the respective icons."
                        }
                    }
                ]
            }
        }, 
        {
            "article": {
                "Title": "Focused Inbox for Outlook",
                "Link": "https://support.microsoft.com/en-us/office/focused-inbox-for-outlook-f445ad7f-02f4-4294-a82e-71d8964e3978#ID0EFH=Windows",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Focused Inbox separates your inbox into two tabs",
                            "sub_content": "Focused Inbox separates your inbox into two tabs—Focused and Other. Your most important email messages are on the Focused tab while the rest remain easily accessible—but out of the way—on the Other tab. In Outlook for Windows, Focused Inbox is available only for Microsoft 365, Exchange, and Outlook.com accounts. If you don't see Focused and Other in your mailbox, you might have a Clutter folder instead. The Focused Inbox REST API provides Microsoft 365 mailbox message classification and training to help users sort their email efficiently. However, this API isn't supported for the Microsoft 365 Shared mailbox. Outlook for Windows currently displays \"Focused Inbox\" hints for shared mailboxes. This is unexpected behavior. Microsoft is aware of the problem, and this article will be updated after changes are complete."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Turn Focused Inbox on",
                            "sub_content": "In Outlook, select the View tab. Select Show Focused Inbox. The Focused and Other tabs will appear at the top of your mailbox. You’ll be informed about email flowing to Other, and you can switch between tabs any time to take a quick look."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Change how your messages get organized",
                            "sub_content": "From your inbox, select the Focused or Other tab, and then right-click the message you want to move. If you're moving from Focused to Other, select Move to Other if you want only the selected message moved. Select Always Move to Other if you want all future messages from the sender to be delivered to the Other tab. If you're moving from Other to Focused, select Move to Focused if you want only the selected message moved. Select Always Move to Focused if you want all future messages from the sender to be delivered to the Focused tab."
                        }
                    }
                ]
            }
        }, 
        {
            "article": {
                "Title": "Turn off Focused Inbox",
                "Link": "https://support.microsoft.com/en-us/office/turn-off-focused-inbox-f714d94d-9e63-4217-9ccb-6cb2986aa1b2",
                "Date": "5 June, 2023",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Note",
                            "sub_content": "If you don't see Focused and Other in your mailbox, you might have a Clutter folder instead. See Use Clutter to sort low-priority messages in Outlook for more information."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "New Outlook for Windows",
                            "sub_content": "Select View > View settings.\n\nIn Mail > Layout, go to the Focused Inbox section and select Don't sort my messages.\n\nThe Focused and Other tabs will disappear from the top of your mailbox."
                        }
                    }
                ]
            }
        }, 
        {
            "article": {
                "Title": "Use Clutter to sort low-priority messages in Outlook",
                "Link": "https://support.microsoft.com/en-us/office/use-clutter-to-sort-low-priority-messages-in-outlook-7b50c5db-7704-4e55-8a1b-dfc7bf1eafa0",
                "Date": "n.d",
                "content": [
                    {
                        "subtitle": {
                            "sub_title": "Introduction",
                            "sub_content": "In Outlook 2016 for Windows, \"Clutter\" can help you filter low-priority email, saving time for your most important messages. If Clutter isn't for you, you can turn if off. The email server keeps track of the email you read and the ones you don't. Once you turn it on, Clutter is automatic. As new email comes in, it takes messages you're most likely to ignore and puts them into the \"Clutter\" folder."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Note",
                            "sub_content": "If you don't see a Clutter folder in your mailbox, you might have the Focused Inbox option. See Focused Inbox for Outlook for more information."
                        }
                    },
                    {
                        "subtitle": {
                            "sub_title": "Important",
                            "sub_content": "If you bought Office 2016 for Windows as a one-time purchase, and you don’t have an Microsoft 365 subscription, you won’t have access to some features, such as Clutter. Going forward, there will be regular updates with new features where you’ll need to have an Microsoft 365 subscription to use them."
                        }
                    }
                ]
            }
        }
    ]
}

# Function to generate Elasticsearch actions
def generate_actions():
    for entry in db["Articles"]:
        article = entry["article"]
        yield {
            "_op_type": "index",
            "_index": "sample_db",
            "_source": {
                "Title": article["Title"],
                "Link": article["Link"],
                "Date": article["Date"],
                "content": article["content"]
            }
        }

# Upload the articles to Elasticsearch
if not es.indices.exists(index="sample_db"):
    es.indices.create(index="sample_db")

helpers.bulk(es, generate_actions())

print("Data uploaded successfully!")