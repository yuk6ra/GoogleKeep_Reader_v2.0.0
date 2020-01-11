import gkeepapi
import re

SECRET_TXT = "Secret.txt"

class Reader(object):
    def __init__(self):
        # find Google Account ID and Password
        with open(SECRET_TXT, "r", encoding="utf-8") as Secret:
            reader = Secret.read().split()
            self.account_id = reader[0]
            self.password = reader[1]

        self.keep = gkeepapi.Keep()

        # pass login
        self.keep.login(self.account_id, self.password)


    def google_keep_searcher(self):

        self.date_type = re.compile(r"""(
            (^\d{4})        # First 4 digits number
            (\D)            # Something other than numbers
            (\d{1,2})       # 1 or 2 digits number
            (\D)            # Something other than numbers
            (\d{1,2})       # 1 or 2 digits number
            )""", re.VERBOSE)

        # find the keyword of query="Test"
        self.note = self.keep.find(query=self.date_type, labels=[self.keep.findLabel('TEST_Label')])
        # indicate the found memos
        # print(self.note)

    def google_keep_reader(self):
        # dict change
        dict = {}
        for note_data in self.note:
            title = note_data.title
            text = note_data.text

            # if you can check the id, you can do this
            # id = note_data.id
            notes = {title: text}
            dict.update(notes)

        # Separate date, content
        for date, content in dict.items():

            # Hit data to "hit_date"
            hit_date = self.date_type.search(date)
            bool_value = bool(hit_date)
            if bool_value is True:
                split = hit_date.groups()
                # Tuple unpacking
                year, month, day = int(split[1]), int(split[3]), int(split[5])

                if year > 3000 or month <= 12 or day <= 31:

                    print(year, month, day)
                    print(content,"\n")
                    # not Japan time zone
                    # print(str(note_data.timestamps.created),"\n")

                else:
                    continue

reader = Reader()
reader.google_keep_searcher()
reader.google_keep_reader()
