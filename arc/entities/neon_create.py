# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

color = self.var_entityparts[0]
colorlist = []
if color == "blue":
    c1, c2, c3, c4, c5 = ['\x1b', '\x1c', '\x1d', '#', '"']
if color == "red":
    c1, c2, c3, c4, c5 = ['\x15', '!', '\x1f', '#', '"']
if color == "white":
    c1, c2, c3, c4, c5 = ['$', '#', '#', '"', '"']
if color == "green":
    c1, c2, c3, c4, c5 = ['\x1a', '\x19', '\x19', '#', '"']
entitylist.append(["neon", (x, y, z), 2, 2, 5, c1, c2, c3, c4, c5])
self.client.sendServerMessage("A %s neon has been created." % color)