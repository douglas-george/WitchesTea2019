from parse import parse


class GadgetMessage():
    def __init__(self):
        self.unparsed_data = ""
        self.data = {}

    def encode(self):
        msg_string = "<GADGET_MESSAGE>\n"
        for dataName in self.data:
            msg_string += "\t<{}>{}</{}>\n".format(dataName, self.data[dataName], dataName)
        msg_string += "</GADGET_MESSAGE>\n"

        return msg_string

    def decode(self, new_data):
        self.unparsed_data += new_data

        string_to_parse = " " + self.unparsed_data + " "

        try:
            _beforeStr, data_str, after_msg_str = parse("{}<GADGET_MESSAGE>{}</GADGET_MESSAGE>{}", string_to_parse)
        except TypeError:
            return False, ""

        while True:
            string_to_parse = " " + data_str + " "

            try:
                _beforeStr, starting_tag, tag_value, closing_tag, after_str = parse("{}<{}>{}</{}>{}", string_to_parse)
            except TypeError:
                if "MESSAGE_ID" not in self.data:
                    return False, after_msg_str.strip()
                else:
                    return True, after_msg_str.strip()

            if starting_tag != closing_tag:
                # corrupt message...
                return False, after_msg_str.strip()

            self.data[starting_tag] = tag_value
            data_str = after_str.strip()


class GadgetHeartbeat(GadgetMessage):
    def __init__(self, gadget_id, heartbeat_id):
        super().__init__()
        self.data["MESSAGE_ID"] = "HEARTBEAT"
        self.data["GADGET_ID"] = str(gadget_id)
        self.data["HEARTBEAT_ID"] = str(heartbeat_id)


if __name__ == "__main__":
    myMsg = GadgetMessage()

    returnStuff = myMsg.decode(newData="<GADGET_MESSAGE><NAME>Doug</NAME><MESSAGE_ID>HEARTBEAT</MESSAGE_ID><RANK>Major</RANK></GADGET_MESSAGE>")

    print(returnStuff)
    print(myMsg.encode())








