import re

class Quote():
    def __init__(self, line):
        line = line.strip()
        line = re.sub("<br[ /]*>", "\\n", line)
        line = re.sub("</?time/?>", "", line)
        line = line.replace("“", "\"")
        line = line.replace("”", "\"")
        #line = line.replace("\"", "\\\"")
        line = line.replace("’", "'")
        self.line = line

        #print(line)
        splits = line.split("|")
        self.time, self.time_str, self.quote, self.title, self.author, self.sfw = splits

        splits = self.quote.lower().split(self.time_str.lower())
        self.quote_start = self.quote[:len(splits[0])]
        self.quote_time = self.quote[len(splits[0]):(len(splits[0])+len(self.time_str))]
        self.quote_end = self.quote[(len(splits[0])+len(self.time_str)):]

        #print(self.time, " - ", self)

        # print(self.quote_start, "***", self.time_str, "***", self.quote_end, sep='')
    def __repr__(self):
        q = {
                "quote_start": self.quote_start,
                "quote_time": self.quote_time,
                "quote_end": self.quote_end,
                "title": self.title,
                "author": self.author,
                "sfw": self.sfw,
        }
        return q.__repr__()
        #return " ".join([self.time, self.time_str, self.quote, self.title, self.author, self.sfw])
    def toDict(self):
        return {
                    "q":(self.quote_start,self.quote_time,self.quote_end)
               }

quotes = []
for line in open("litclock_annotated.csv"):
    quotes.append(Quote(line))

quote_map = {}
for q in quotes:
    if q.time not in quote_map:
        quote_map[q.time] = []
    quote_map[q.time].append(q)

for h in range(24):
    for m in range(60):
        key = f"{h:02d}:{m:02d}"
        back = f"{h:02d}:{m-1:02d}"
        if key not in quote_map:
            quote_map[key] = quote_map[back]

#num_quotes = 1
#print(f"#define NUM_QUOTES {num_quotes}\n")
#print("char* quotes[24][60][NUM_QUOTES][5] = {")
#for h in range(24):
#    print("  {")
#    for m in range(60):
#        key = f"{h:02d}:{m:02d}"   
#        quote_list = quote_map[key]
#        quote_list.sort(key=sort_key)
#        print("    {")
#        for q in quote_list[:num_quotes]:
#            print("""      {{"{:s}", "{:s}", "{:s}", "{:s}", "{:s}"}},""".format(
#                q.quote_start, q.quote_time, q.quote_end, q.title, q.author))
#        print("    },")
#    print("  },")
#
#print("};")

for key, quote_list in quote_map.items():
    key = key.replace(":","_")
    with open(f"times/{key}.txt", "w") as f:
        f.write(str(len(quote_list)));
        f.write('\n')
        for q in quote_list:
            f.write(q.__repr__())
            f.write('\n')

    with open(f"times/{key}.txt", "r") as f:
        print(f.readline())
